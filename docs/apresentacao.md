# Roteiro da apresentação da Atividade 1

Duração: aproximadamente 10 minutos. Foco exclusivo nos requisitos da atividade. Mostrar repositório, PRs e Actions; não depender de slides. Dividir os blocos entre os integrantes reais; todos precisam falar.

## Preparação obrigatória antes de apresentar

1. Abrir e revisar o PR da branch atividade/esteira-segura; obter runs verdes e integrar as correções após revisão do grupo.
2. Configurar a proteção da main e os checks obrigatórios conforme docs/configuracao-github.md. Confirmar privacidade e acesso do professor.
3. Criar uma branch separada de demonstração a partir da main corrigida. Introduzir uma SQL Injection controlada no login, confirmar que o Semgrep a identifica e abrir PR. Não integrar a falha na main.
4. Guardar os links do run vermelho e da prova de merge bloqueado. Corrigir a consulta no mesmo PR e guardar o run verde. Ensaiar esse processo.
5. Deixar as abas do PR, Actions, código e evidências abertas. A execução pode demorar: usar links reais previamente preparados para mostrar vermelho e verde dentro do tempo, além da demonstração ao vivo pedida pelo enunciado. Não simular um bloqueio que ainda não foi configurado.

## 0:00 a 1:00 — Contexto e objetivo

Mostrar: página inicial do repositório.

Fala sugerida: “Nossa atividade foi transformar a TaskFlow em uma aplicação protegida por uma esteira de CI. O objetivo é impedir que alterações com falhas entrem na main. Dividimos o trabalho entre aplicação, pipelines, hardening e documentação.”

Apresentar os nomes e os papéis reais. Usar docs/resumo-atividade.md como checklist.

## 1:00 a 5:00 — Demonstração do gate em PR

Mostrar: PR da demonstração, log do Semgrep, merge bloqueado e depois execução corrigida.

Sequência:

1. Mostrar a consulta concatenando entrada do usuário no PR de demonstração.
2. Abrir Actions e apontar o finding do Semgrep e o check vermelho.
3. Voltar ao PR e mostrar o bloqueio causado pelos required checks da main.
4. Mostrar a correção usando placeholders e parâmetros separados.
5. Mostrar o commit corretivo e a execução verde no mesmo PR.

Fala sugerida: “O Semgrep detecta a construção insegura da consulta. O --error faz o job falhar; a regra da main exige esse check aprovado e impede o merge. Corrigimos o código, sem desligar o scanner. Esse é o shift-left: identificar e corrigir antes da integração.”

Ponto para explicar: pipeline vermelho e bloqueio de merge são coisas distintas. A ferramenta reprova; a proteção da branch impede integrar.

## 5:00 a 7:00 — Antes e depois

Mostrar: docs/hardening.md, docs/evidencias/resumo.json e os arquivos de histórico da imagem.

Fala sugerida: “No scan local registrado, o Semgrep encontrou 10 achados na aplicação original e zero no código corrigido. O Trivy registrou 388 ocorrências HIGH/CRITICAL na imagem original e zero na imagem final. Atualizamos dependências e pacotes do sistema, reduzimos a imagem e mantivemos o gate ativo.”

Apontar que a imagem atual não inclui ADMIN_PASSWORD em ENV e usa Gunicorn com usuário não-root. Informar que os números são ocorrências do scan de 17/10/2026, não uma garantia permanente nem uma contagem de CVEs únicas.

## 7:00 a 9:00 — Decisões técnicas exigidas

Mostrar, nesta ordem:

- app.py: login com consulta parametrizada; criação e verificação de hash; TASKFLOW_SECRET_KEY recebida do ambiente.
- sast.yml: --error e fetch-depth: 0.
- sca.yml e dependabot.yml: auditoria bloqueante e proposta automática de atualizações.
- Dockerfile e container.yml: versão/digest, hashes, USER e Trivy com exit-code 1.

Fala sugerida: “Separar parâmetros da instrução SQL impede que a entrada altere a consulta. O banco guarda hash de senha; a chave de sessão entra pelo ambiente. As dependências são auditadas e atualizadas por PR. O container roda sem root e o Trivy reprova HIGH/CRITICAL.”

Decisão concreta para discutir: “A base inicialmente testada ainda tinha achados do sistema operacional. Escolhemos uma base mínima Alpine e atualizamos seus pacotes. Isso zerou os HIGH/CRITICAL daquela execução sem suprimir CVEs. Como os pacotes do SO mudam, reconstrução e nova auditoria continuam necessárias.”

## 9:00 a 10:00 — Aprendizado e participação

Mostrar: regras da main e README.

Fala sugerida: “O principal aprendizado foi que executar scanners não basta: precisamos corrigir as falhas e exigir os checks na main. Também documentamos evidências reproduzíveis para justificar as decisões.”

Cada integrante confirma sua contribuição real. Citar pendências que ainda existirem, sem declarar etapas não executadas como concluídas.

## Perguntas para ensaiar

| Pergunta | Resposta curta |
| --- | --- |
| O que impede o merge? | A proteção da main exigindo os status checks. |
| Para que serve --error? | Faz o Semgrep reprovar quando encontra achados. |
| Por que fetch-depth: 0? | Permite verificar segredos no histórico completo. |
| Por que hash de senha? | A autenticação verifica o hash sem guardar a senha original. |
| Por que placeholders no SQL? | Mantêm valores do usuário separados da instrução SQL. |
| O Dependabot bloqueia o merge sozinho? | Não; ele propõe atualizações. Os gates e regras da main controlam a integração. |
| O que exit-code 1 faz no Trivy? | Reprova o job quando encontra vulnerabilidades nas severidades configuradas. |
| Zero HIGH/CRITICAL significa segurança total? | Não; é o resultado daquele alvo, filtro, versão e base de vulnerabilidades. |

## Links a preencher com evidências reais

- PR da demonstração:
- Run vermelho:
- Prova de merge bloqueado:
- Commit corretivo e run verde:
- Integrantes e contribuições:
