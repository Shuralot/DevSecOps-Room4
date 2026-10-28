# DAST — ZAP no pipeline (Módulo 4)

## Como o gate funciona

O workflow é o [`.github/workflows/dast.yml`](../.github/workflows/dast.yml) e o check obrigatório se chama **`DAST - ZAP Baseline`**. Ele executa, nesta ordem:

1. **Build** da imagem a partir do `Dockerfile` do produto.
2. **Sobe a TaskFlow dentro do runner** em `127.0.0.1:5000`. O runtime é restrito (`--read-only`, `--cap-drop=ALL`, `no-new-privileges`), a chave é efêmera e o debug fica desligado (`TASKFLOW_DEBUG=0`).
3. **Espera ativa** com `curl` em `/login` por até 60 s. Se a app não responder, o job falha. Sem essa etapa, o ZAP atacaria o nada e o relatório sairia "limpo".
4. **ZAP Baseline (passivo)** com `.zap/rules.tsv`.
5. **ZAP Full Scan (ativo)**, limitado a 10 min. O baseline só observa respostas e não injeta payloads, então é o scan ativo que prova o XSS refletido.
6. Os **relatórios HTML/JSON/MD** de cada scan são publicados como artefato (`zap-baseline-report` e `zap-full-scan-report`).

**Política do gate (`.zap/rules.tsv`):**
- O ZAP roda com `-I`: alerta **WARN** aparece no relatório mas não bloqueia.
- Qualquer regra marcada **FAIL** devolve exit code 1, e o `fail_action: true` deixa o check vermelho.
- Não existe `continue-on-error` em nenhum passo.
- Nenhuma regra está como IGNORE. As rebaixadas para WARN têm justificativa na 3ª coluna do arquivo.

**Trade-off:** com `-I`, um alerta novo que não esteja na lista de FAIL não bloqueia o merge, só aparece no relatório. Escolhemos isso para o gate não ficar vermelho por alertas informativos (10111, 10112, 10109), mas as categorias que importam (injeção, headers, cookies, CSRF, debug) estão explicitamente como FAIL.

## Correções feitas

| Falha | Correção | Onde |
|---|---|---|
| XSS armazenado (título/descrição) | Templates Jinja2 `.html` com autoescape e nenhum `\| safe` | `templates/tasks.html` |
| XSS refletido no **parâmetro `q`** (Encontro 9) | `q` volta na tela ("Resultados para: …") e no `value=` do input, sempre escapado | `templates/tasks.html`, rota `/tasks` |
| XSS refletido na **mensagem de erro do login** (Encontro 9) | A mensagem ecoa o usuário digitado, escapado; o tamanho é limitado a 100 caracteres | `templates/login.html`, rota `/login` |
| Endpoint **`/debug/info`** | Rota removida (o teste garante 404); debug só com `TASKFLOW_DEBUG=1`, **desligado por padrão** | `app.py` |
| Headers de segurança ausentes | `after_request` com CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy, Permissions-Policy, COOP/CORP e `Cache-Control: no-store` | `app.py` |

Os testes de regressão ficam em `tests/test_security.py`: `test_login_error_and_search_escape_xss`, `test_debug_off_by_default_and_security_headers` e `test_csrf_required_and_debug_removed`.

## Achados antes × depois (execução local com a mesma imagem do ZAP do CI)

As evidências estão em [`docs/evidencias/atividade-2/`](evidencias/atividade-2/).

| # | Alerta ZAP (ID) | OWASP Top 10 2021 | Antes (Atividade 1) | XSS reintroduzido (`\| safe`) | Depois |
|---|---|---|---|---|---|
| 1 | Cross Site Scripting (Reflected) **40012**, `POST /login`, parâmetro `username` | **A03 Injection** | — | **FAIL** | PASS |
| 2 | Content Security Policy Header Not Set **10038** | A05 Security Misconfiguration | **FAIL** ×5 | PASS | PASS |
| 3 | Missing Anti-clickjacking Header **10020** | A05 Security Misconfiguration | **FAIL** ×3 | PASS | PASS |
| 4 | X-Content-Type-Options Header Missing **10021** | A05 Security Misconfiguration | **FAIL** ×3 | PASS | PASS |
| 5 | Information Disclosure / Debug (`/debug/info`) **10023** | A05 Security Misconfiguration | PASS (já removido na Atividade 1) | PASS | PASS |
| 6 | Absence of Anti-CSRF Tokens **10202** | A01 Broken Access Control | PASS (Flask-WTF) | PASS | PASS |
| 7 | HTTP Only Site **10106** / Cookie sem Secure **10011** | A02 Cryptographic Failures | WARN | WARN | WARN (justificado: runner sem TLS) |
| 8 | User Controllable HTML Element Attribute **10031** | A03 Injection (potencial) | WARN | WARN | WARN (justificado: valor escapado) |

Resultado do gate:

| Execução | Resultado | Gate |
|---|---|---|
| Antes, baseline | `FAIL-NEW: 3` | 🔴 vermelho |
| XSS reintroduzido, full scan | `FAIL-NEW: 1` (40012) | 🔴 vermelho, **merge bloqueado** |
| Depois, baseline | `FAIL-NEW: 0` | 🟢 verde |
| Depois, full scan | `FAIL-NEW: 0` | 🟢 verde |

O payload que o ZAP usou no XSS refletido foi `</p><scrIpt>alert(1);</scRipt><p>`, injetado no campo `username` do login.

## Roteiro da demo (PR que reverte a correção)

1. Crie a branch `demo/xss-regressao` a partir da `main` já com esta atividade.
2. Em `templates/login.html`, troque `{{ error }}` por `{{ error | safe }}`.
3. Abra o PR. O check **`DAST - ZAP Baseline`** fica vermelho no passo *ZAP Full Scan* com `FAIL-NEW: Cross Site Scripting (Reflected) [40012]`, e o merge fica bloqueado.
4. Baixe o artefato `zap-full-scan-report` e mostre o alerta.
5. Reverta para `{{ error }}`, faça push e o check volta a ficar verde.
