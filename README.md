# TaskFlow — atividade 1 do grupo Room4

Aplicação baseada em diegobuarquebr/taskflow_pos_2026. A pasta codigo/ mantém material didático vulnerável; não é copiada para a imagem. A implementação entregue é app.py com templates/.

## Executar localmente

Python 3.12. No PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --require-hashes -r requirements.txt
$env:TASKFLOW_SECRET_KEY = python -c "import secrets; print(secrets.token_hex(32))"
$env:TASKFLOW_HTTPS = '0'
flask --app 'app:create_app()' init-db
flask --app 'app:create_app()' create-user aluno
flask --app 'app:create_app()' run --host 127.0.0.1 --port 5000
```

A senha é solicitada sem eco e precisa ter 12 caracteres. Não há conta ou senha padrão. O servidor Flask é apenas para desenvolvimento local; a imagem usa Gunicorn. Cookie Secure é padrão; TASKFLOW_HTTPS=0 só é usado no laboratório via HTTP em localhost.

Para o banco original com senhas em texto puro, faça backup fora do Git e crie um banco novo para este laboratório. init-db não converte senhas existentes: recrie os usuários pelo comando create-user. Nunca versione banco, .env ou saída contendo segredos.

## Testes e scanners

```bash
python -m pip install pytest==9.1.1 ruff==0.17.1 pip-audit==2.10.1 pip-tools==7.6.2
ruff check app.py tests
pytest -q
pip-audit --require-hashes -r requirements.txt
pip-compile --upgrade --generate-hashes --strip-extras -o requirements.txt requirements.in
```

Execute Semgrep em Linux/WSL ou container:

```bash
python -m pip install semgrep
semgrep scan --config=p/python --config=p/flask --config=p/security-audit --error .
gitleaks git . --redact
```

.semgrepignore exclui somente material didático codigo/ e ambiente virtual; o código entregue é analisado. Gitleaks analisa o histórico completo, incluindo codigo/. Na execução inicial local, Gitleaks 8.30.1 não encontrou segredos com as regras padrão: isso não prova ausência de senhas didáticas, conhecidas pela leitura do código. Não foi criada allowlist sem achados. Se o scanner do CI detectar os segredos históricos didáticos, registrar o fingerprint/commit específico e a justificativa em .gitleaks.toml; nunca excluir uma regra inteira.

## Container

```bash
docker build -t taskflow:hardened .
trivy image --severity HIGH,CRITICAL --exit-code 1 taskflow:hardened
export TASKFLOW_SECRET_KEY="$(python -c 'import secrets; print(secrets.token_hex(32))')"
bash scripts/docker-run-seguro.sh
docker exec -it taskflow-seguro flask --app 'app:create_app()' create-user aluno
```

Em PowerShell, defina as variáveis conforme o exemplo local e execute o script em WSL/Git Bash, ou adapte as flags ao terminal. O banco fica no volume taskflow-dados; a raiz é somente leitura. A aplicação escuta apenas no endereço local do host. Para servir via HTTPS, configure proxy e mantenha o cookie Secure habilitado.

## Workflows e bloqueio

Os quatro workflows executam em PR, push na main e manualmente em Actions → workflow → Run workflow.

- CI: instalação com hashes, lint, compilação e testes de regressão.
- SAST e segredos: Semgrep e Gitleaks, ambos com falha bloqueante.
- SCA: pip-audit reprova vulnerabilidades nas dependências.
- Container: build, Trivy HIGH/CRITICAL e inicialização do Gunicorn em runtime restrito.

Checks a exigir na proteção da main: `CI - build lint testes`, `SAST - Semgrep`, `Segredos - Gitleaks`, `SCA - pip-audit`, `Container - build e Trivy`.

O Dependabot abre PRs semanais para pip, actions e imagem base; os gates verificam cada PR. Dependabot não substitui o pip-audit. Actions são fixadas por SHA; a base Docker é fixada por versão e digest. requirements.txt fixa todas as dependências e seus hashes. Após atualização via Dependabot, revisar requirements.in e regenerar o lock se necessário.

## Situação e evidências

Consulte docs/hardening.md, docs/configuracao-github.md e docs/apresentacao.md. Um YAML pronto não comprova execução verde nem bloqueio de merge. Os links reais de runs e PRs devem ser registrados após publicação.

Apoio de IA foi utilizado na implementação e revisão. Cada integrante deve executar, revisar e ser capaz de explicar as decisões que apresentar. Registre nomes e participação real em docs/apresentacao.md.
