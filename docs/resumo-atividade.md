# Resumo do que foi feito para a Atividade 1

As alterações estão na branch atividade/esteira-segura. A main não foi modificada. Esta lista separa implementação e validação local de configurações que ainda precisam ser comprovadas no GitHub.

| Pedido da atividade | O que fizemos | Situação |
| --- | --- | --- |
| CI com instalação, lint e gatilhos de PR, push na main e execução manual | Criamos .github/workflows/ci.yml com instalação por hashes, Ruff e verificação de sintaxe | Implementado; lint local aprovado; run no GitHub pendente |
| Semgrep como gate | Configuramos p/python, p/flask, p/security-audit e --error em sast.yml | Implementado; 10 achados no original e zero no código corrigido na análise local |
| Gitleaks com histórico completo | Configuramos Gitleaks e fetch-depth: 0 | Implementado; scan local dos 22 commits originais sem achados pelas regras padrão |
| Corrigir SQL Injection | Trocamos concatenação por consultas parametrizadas no login e na busca | Implementado e validado localmente |
| SECRET_KEY por variável de ambiente | A aplicação exige TASKFLOW_SECRET_KEY para iniciar | Implementado; sem chave fixa ou fallback no app atual |
| Senhas com hash | Cadastro usa generate_password_hash; login usa check_password_hash | Implementado e validado localmente |
| SCA com pip-audit e dependências atualizadas | Criamos sca.yml e atualizamos requirements.txt com versões e hashes | Auditoria local sem vulnerabilidades conhecidas na data da execução |
| Dependabot | Configuramos atualização semanal de pip, GitHub Actions e Docker | Arquivo pronto; funcionamento no GitHub pendente |
| Corrigir as seis falhas do Dockerfile | Base mínima com versão/digest, usuário não-root, instalação com hashes, remoção de segredo, Gunicorn e debug desligado | Imagem construída e iniciada localmente |
| Trivy bloqueando HIGH/CRITICAL | Criamos container.yml com exit-code 1 | Scan local: 388 ocorrências no original e zero na imagem final |
| Runtime seguro | Criamos scripts/docker-run-seguro.sh com read-only, cap-drop, no-new-privileges e limites de recursos | Runtime restrito validado localmente |
| Documentar Trivy e docker history antes/depois | Criamos docs/hardening.md e docs/evidencias/ | Evidências locais registradas |
| permissions mínimo e pinning de actions | Workflows usam contents: read e actions fixadas por SHA | Implementado |
| CODEOWNERS | Criamos .github/CODEOWNERS com @Shuralot | Arquivo pronto; complementar com integrantes confirmados |

## O que ainda não podemos apresentar como concluído

- Repositório privado e acesso de leitura do professor @HardSource.
- Proteção da main com PR obrigatório e todos os required checks.
- Execuções verdes reais dos workflows no GitHub.
- PR com vulnerabilidade controlada, check vermelho, merge bloqueado e correção no mesmo PR.
- Evidência de auditoria/hardening de SO com Lynis em VM Linux, citada no material de avaliação.
- Apresentação com todos os integrantes e participação registrada.

Os números dos scanners são da execução local de 17/10/2026, com os alvos e versões descritos em docs/hardening.md. Zero achados nesses scans não significa ausência de qualquer vulnerabilidade.
