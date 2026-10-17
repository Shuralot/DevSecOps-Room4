"""TaskFlow com consultas parametrizadas, hashing e proteção CSRF."""

import os
import sqlite3
from pathlib import Path

import click
from flask import Flask, current_app, g, redirect, render_template, request, session, url_for
from flask_wtf.csrf import CSRFProtect
from werkzeug.security import check_password_hash, generate_password_hash


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def init_db():
    Path(current_app.config["DATABASE"]).parent.mkdir(parents=True, exist_ok=True)
    get_db().executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL
        );
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            title TEXT NOT NULL,
            description TEXT,
            done INTEGER DEFAULT 0
        );
    """)
    get_db().commit()


def create_app(test_config=None):
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("TASKFLOW_SECRET_KEY"),
        DATABASE=os.environ.get("TASKFLOW_DATABASE", "instance/taskflow.db"),
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        SESSION_COOKIE_SECURE=os.environ.get("TASKFLOW_HTTPS", "1") == "1",
        MAX_CONTENT_LENGTH=64 * 1024,
    )
    if test_config:
        app.config.update(test_config)
    if not app.config["SECRET_KEY"]:
        raise RuntimeError("Defina TASKFLOW_SECRET_KEY antes de iniciar.")
    CSRFProtect(app)

    @app.teardown_appcontext
    def close_connection(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        click.echo("Banco inicializado; nenhum usuário padrão foi criado.")

    @app.cli.command("create-user")
    @click.argument("username")
    @click.password_option()
    def create_user(username, password):
        if len(password) < 12:
            raise click.ClickException("Use uma senha com pelo menos 12 caracteres.")
        db = get_db()
        try:
            db.execute(
                "INSERT INTO users (username, password) VALUES (?, ?)",
                (username, generate_password_hash(password)),
            )
            db.commit()
        except sqlite3.IntegrityError as exc:
            raise click.ClickException("Usuário já existe.") from exc
        click.echo("Usuário criado.")

    @app.route("/")
    def index():
        return redirect(url_for("tasks" if "user_id" in session else "login"))

    @app.route("/login", methods=["GET", "POST"])
    def login():
        error = None
        if request.method == "POST":
            user = get_db().execute(
                "SELECT * FROM users WHERE username = ?",
                (request.form.get("username", ""),),
            ).fetchone()
            if user and check_password_hash(user["password"], request.form.get("password", "")):
                session.clear()
                session["user_id"] = user["id"]
                session["username"] = user["username"]
                return redirect(url_for("tasks"))
            error = "Usuário ou senha inválidos."
        return render_template("login.html", error=error)

    @app.route("/logout", methods=["POST"])
    def logout():
        session.clear()
        return redirect(url_for("login"))

    @app.route("/tasks")
    def tasks():
        if "user_id" not in session:
            return redirect(url_for("login"))
        rows = get_db().execute(
            "SELECT * FROM tasks WHERE user_id = ? AND title LIKE ?",
            (session["user_id"], "%" + request.args.get("q", "") + "%"),
        ).fetchall()
        return render_template("tasks.html", tasks=rows)

    @app.route("/tasks/new", methods=["GET", "POST"])
    def new_task():
        if "user_id" not in session:
            return redirect(url_for("login"))
        if request.method == "POST":
            title = request.form.get("title", "").strip()
            if not title or len(title) > 200:
                return "Título obrigatório, com até 200 caracteres.", 400
            db = get_db()
            db.execute(
                "INSERT INTO tasks (user_id, title, description) VALUES (?, ?, ?)",
                (session["user_id"], title, request.form.get("description", "")),
            )
            db.commit()
            return redirect(url_for("tasks"))
        return render_template("new.html")

    return app
