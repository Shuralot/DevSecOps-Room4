import re
import secrets

import pytest
from werkzeug.security import check_password_hash, generate_password_hash

from app import create_app, get_db, init_db

# Credencial efêmera dos testes; não é uma conta da aplicação.
TEST_PASSWORD = secrets.token_urlsafe(24)


@pytest.fixture
def app(tmp_path):
    # Cada teste tem um SQLite temporário e dois usuários para verificar isolamento.
    app = create_app({"TESTING": True, "SECRET_KEY": secrets.token_hex(32),
                      "DATABASE": str(tmp_path / "test.db"), "SESSION_COOKIE_SECURE": False})
    with app.app_context():
        init_db()
        db = get_db()
        for username in ("alice", "bob"):
            db.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                       (username, generate_password_hash(TEST_PASSWORD)))
        db.execute("INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                   (2, "private-bob-task", "confidential"))
        db.commit()
    return app


def token(client, path="/login"):
    html = client.get(path).get_data(as_text=True)
    return re.search(r'name="csrf_token" value="([^"]+)"', html).group(1)


def login(client, username="alice", password=None):
    return client.post("/login", data={"username": username, "password": password or TEST_PASSWORD,
                                       "csrf_token": token(client)})


def test_login_and_password_hash(app):
    client = app.test_client()
    assert login(client).status_code == 302
    assert client.get("/tasks").status_code == 200
    with app.app_context():
        password = get_db().execute("SELECT password FROM users WHERE username = ?",
                                    ("alice",)).fetchone()[0]
        assert password != TEST_PASSWORD
        assert check_password_hash(password, TEST_PASSWORD)


def test_sql_injection_does_not_authenticate(app):
    client = app.test_client()
    assert login(client, "' OR 1=1 --", "incorrect").status_code == 200
    assert client.get("/tasks").status_code == 302


def test_search_isolates_users(app):
    # Uma tentativa de SQLi não pode revelar a tarefa do outro usuário.
    client = app.test_client()
    login(client)
    response = client.get("/tasks", query_string={"q": "' OR 1=1 --"})
    assert response.status_code == 200
    assert b"private-bob-task" not in response.data
    assert b"private-bob-task" not in client.get("/tasks").data


def test_task_xss_escaped(app):
    # O conteúdo é salvo, mas deve voltar como texto escapado, sem executar HTML.
    client = app.test_client()
    login(client)
    result = client.post("/tasks/new", data={"csrf_token": token(client, "/tasks/new"),
                         "title": "<script>alert(1)</script>", "description": "<b>unsafe</b>"})
    assert result.status_code == 302
    html = client.get("/tasks").get_data(as_text=True)
    assert "<script>" not in html
    assert "&lt;script&gt;" in html
    assert "&lt;b&gt;unsafe&lt;/b&gt;" in html


def test_csrf_required_and_debug_removed(app):
    client = app.test_client()
    assert client.post("/login", data={"username": "alice"}).status_code == 400
    assert client.get("/debug/info").status_code == 404
    assert app.debug is False


def test_missing_secret_fails(monkeypatch):
    monkeypatch.delenv("TASKFLOW_SECRET_KEY", raising=False)
    with pytest.raises(RuntimeError):
        create_app()
