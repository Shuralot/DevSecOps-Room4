# Configuração do GitHub

Verificação inicial: Shuralot/DevSecOps-Room4 estava público; a conexão fabalmeida tinha somente leitura. Estas configurações ainda não foram aplicadas por este trabalho.

1. O proprietário deve conceder escrita a fabalmeida, caso queira publicar as mudanças por esta sessão.
2. Settings → General → Danger Zone → Change visibility: tornar privado conforme o enunciado. Verificar antes se o plano permite proteção de branches em repositório privado; se não permitir, alinhar uma solução com o professor. Não trocar o requisito por um repositório público sem autorização dele.
3. Settings → Collaborators: adicionar HardSource com Read. A granularidade disponível depende do tipo de conta/repositório; se não houver Read para colaborador de repositório pessoal, usar uma organização com papel Read ou alinhar com o professor.
4. Publicar a branch atividade/esteira-segura e abrir PR para main.
5. Após a primeira execução dos workflows, Settings → Rules → Rulesets (ou Branches → protection): proteger main; exigir PR, revisão de CODEOWNERS, resolução de conversas, checks abaixo e branch atualizada. Bloquear force push e exclusão; não cadastrar bypass rotineiro.
6. Checks: CI - build lint testes; SAST - Semgrep; Segredos - Gitleaks; SCA - pip-audit; Container - build e Trivy. Confirmar os nomes na execução real antes de selecioná-los.
7. CODEOWNERS começa com Shuralot, proprietário do repositório. Incluir os outros membros somente depois de confirmar seus usuários e acesso de escrita. Uma revisão precisa vir de outra pessoa, diferente do autor do PR.
8. Demonstrar que um PR com gate vermelho realmente não pode ser integrado, inclusive pela conta usada na apresentação.

Não forneça tokens ou senhas no chat, em commits ou em YAML. Os scanners não precisam de um PAT pessoal. GITHUB_TOKEN é emitido pelo GitHub Actions.
