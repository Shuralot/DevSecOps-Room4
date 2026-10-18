# Hardening e evidências

Verificações locais em 17/10/2026; base do grupo no commit 0875fdf1e0d6de5b4fe3ef20fb75646235238343. Os arquivos em evidencias/ são saídas reais ou projeções de campos dos relatórios, sem resultados inventados. Confira resumo.json para as contagens.

## Seis falhas do Dockerfile

1. python:latest substituído por Python 3.12.13 Alpine 3.23, fixado também pelo digest do índice OCI.
2. Processo executa com UID/GID 10001, sem root.
3. Instalação exige hashes de todas as dependências transitivas em requirements.txt.
4. Removido ADMIN_PASSWORD da imagem. TASKFLOW_SECRET_KEY é recebido em runtime; a senha de usuário é digitada no comando create-user, sem eco.
5. Gunicorn substitui o servidor Flask de desenvolvimento.
6. Debug não é habilitado; flags de runtime tornam a raiz somente leitura, removem capabilities, impedem novos privilégios e limitam recursos.

A porta 5000 foi mantida: o problema era o servidor de desenvolvimento, não o número da porta. O banco persiste no volume /app/data, único caminho de dados gravável, além do tmpfs /tmp.

## Comparação real

Trivy 0.69.3 foi executado com filtro HIGH,CRITICAL na imagem original construída de codigo/app-exemplo/ e na imagem corrigida. O comando original usa python:latest; por isso, o resultado de reconstruções futuras pode variar. history-before.txt e trivy-before.csv registram esta execução. A imagem original só foi construída e analisada, não exposta como serviço.

A primeira candidata Debian slim manteve vulnerabilidades do SO. Uma candidata Alpine reduziu os pacotes, mas ainda tinha 10 achados HIGH corrigíveis em OpenSSL, libuuid e SQLite. A versão final atualiza os pacotes com apk upgrade --no-cache. O scan final retornou exit code 0 e nenhum HIGH/CRITICAL. A atualização do SO é uma escolha explícita: mantém o digest da base fixado, mas os pacotes resolvidos no build variam conforme o repositório Alpine; revisar e reconstruir regularmente. Não foi usada .trivyignore nem --ignore-unfixed.

Semgrep encontrou 10 achados no app original e zero no código entregue, usando p/python, p/flask e p/security-audit. O material vulnerável em codigo/ fica fora do alvo de produção e fora da imagem; seu scan de referência é feito separadamente.

Gitleaks 8.30.1 analisou 22 commits e não encontrou segredos com as regras padrão. Na execução Windows houve avisos do conversor Git de DOCX; o gate do CI roda em Linux. Nenhuma allowlist foi adicionada porque não houve finding. Os valores didáticos antigos continuam conhecidos no material e histórico; novos achados exigem triagem específica.

Lint aprovado, seis testes de segurança aprovados e pip-audit sem vulnerabilidades conhecidas. A imagem corrigida foi construída com instalação por hashes e respondeu HTTP 200 em /login usando Gunicorn, UID/GID 10001, read-only e cap-drop ALL.

## Reproduzir

```bash
docker build -t taskflow:baseline codigo/app-exemplo
docker build -t taskflow:hardened .
docker history --no-trunc taskflow:baseline
docker history --no-trunc taskflow:hardened
trivy image --severity HIGH,CRITICAL --exit-code 1 taskflow:hardened
trivy image --severity HIGH,CRITICAL --format json taskflow:baseline
```

Para analisar o original com Semgrep, copiar codigo/app-exemplo/app.py para uma pasta temporária fora do repositório, entrar nessa pasta e executar os três rulesets. Isso evita a exclusão intencional do material de referência pela .semgrepignore do produto.

## Pendências verificáveis

Execuções reais no GitHub Actions, proteção da main, PR com merge bloqueado, acesso do professor e repositório privado ainda dependem de publicação e configuração pelo proprietário.

Hardening de SO/Lynis precisa ser executado em uma VM Linux de laboratório autorizada, não no Windows nem em um container fingindo auditar o host. Na VM: instalar Lynis, executar sudo lynis audit system, registrar versão e saídas /var/log/lynis.log e /var/log/lynis-report.dat em docs/evidencias/ após revisar dados sensíveis; aplicar correções pertinentes e comparar nova auditoria. Não foram produzidos resultados de Lynis nesta máquina.

## Triagem do Gitleaks no PR

O Gitleaks 8.24.3 do GitHub encontrou três ocorrências de GPG_KEY nos metadados da imagem oficial Python, reproduzidos nos relatórios. O valor é um identificador público de chave para verificação de assinaturas, não material privado de autenticação. .gitleaksignore aceita somente os três fingerprints específicos do commit 759df1, sem desativar a regra generic-api-key e sem excluir arquivos inteiros. Novos achados continuam reprovando o gate.
