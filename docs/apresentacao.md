# Apresentação e demonstração

Duração aproximada: 10 minutos. Registrar nomes e funções reais antes da entrega.

- 1 minuto: integrantes e papéis; explicar o problema da TaskFlow original.
- 4 minutos: PR com falha, gate vermelho e merge bloqueado; correção no mesmo PR, checks verdes. Mostrar a aba Actions e a regra da main.
- 2 minutos: Trivy, Semgrep e docker history antes/depois, com saídas reais.
- 2 minutos: consultas parametrizadas, hash de senha, segredo em runtime, isolamento de usuário e container não-root. Explicar por que ignore genérico não é correção.
- 1 minuto: aprendizado e participação de cada pessoa.

## Preparar a demonstração

Após integrar a esteira corrigida e proteger main, criar uma branch de demonstração. Introduzir temporariamente em app.py uma consulta SQL concatenando entrada do usuário; executar Semgrep e confirmar o finding antes de abrir o PR. Não usar credenciais reais. Não integrar a falha na main.

Abrir PR, aguardar os checks, capturar o erro e o botão de merge bloqueado. Remover a alteração no mesmo PR; aguardar a execução verde. Registrar os links abaixo. O finding de Semgrep pode variar por regra; ensaiar a detecção antes da apresentação.

## Evidências pendentes

- PR da demonstração: a preencher com o link real.
- Run vermelho: a preencher.
- Evidência de bloqueio de merge: a preencher.
- Commit corretivo e run verde: a preencher.
- Participação de cada integrante: a preencher com fatos reais.

## Questões para ensaio

Por que um pipeline vermelho sozinho não impede merge? O que fetch-depth: 0 muda? Por que um hash não é uma senha criptografada reversível? Por que a mesma query usa placeholders para user_id e busca? O que --require-hashes verifica? Onde o SQLite escreve com --read-only? Por que o digest da imagem precisa de atualização? Como tratar uma CVE sem correção, com justificativa específica e acordo do grupo?
