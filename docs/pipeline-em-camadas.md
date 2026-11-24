# Pipeline em camadas

Versão de consulta do Apêndice G. A divisão em quatro camadas é do
autor; os comandos são os que aparecem nos capítulos. O arquivo
[`.github/workflows/verificacao.yml`](../.github/workflows/verificacao.yml)
implementa as camadas 2 e 3 sobre o projeto de exemplo.

## Camada 1: ganchos do agente

Antes e depois de cada uso de ferramenta pelo agente, com retorno em
segundos. Um gancho antes da ferramenta pode bloquear um comando
proibido e devolver o motivo; um gancho depois da edição pode formatar
ou verificar o arquivo alterado (Cap. 11). A configuração depende da
ferramenta de agente que o time usa; consulte a documentação dela.

## Camada 2: verificação local

Antes de o agente declarar a tarefa pronta, como comando listado no
arquivo de instruções (Cap. 9):

```sh
ruff check .                          # estilo e defeitos simples
lint-imports                          # direção das dependências
mypy --strict src/loja/<fronteira>    # tipos nas fronteiras
pytest                                # testes e funções de aptidão
contencao mapa src/loja && git diff --exit-code MAPA.md
contencao instrucoes AGENTS.md        # higiene do arquivo
```

## Camada 3: portão do pull request

A cada envio ao PR, com retorno em minutos: os comandos da camada 2,
porque o agente pode não tê-los rodado, mais

```sh
contencao check-testes origin/main    # testes protegidos (Cap. 10)
contencao check-pr origin/main        # tamanho e módulos (Cap. 12)
ruff check . --output-format concise --exit-zero --quiet > v.txt
contencao catraca verificar v.txt     # só violações novas (Cap. 11)
```

Acrescente uma lista de dependências aprovadas, contra pacotes
inventados por modelos (Cap. 11), e um analisador de segurança, como
o Semgrep.

## Camada 4: governança

O arquivo `CODEOWNERS` chama o dono de contratos, testes de
aceitação, pipeline e arquivo de instruções, e as regras de proteção
do ramo exigem a aprovação dele (Cap. 14). Exceções vencidas fazem a
verificação falhar (Cap. 11). O painel junta vazão, carga de revisão
e custo por mudança (Caps. 4 e 15).

## Mudar uma convenção sem deixar duas gerações

No primeiro PR, a regra e a verificação mudam juntas, e o código
antigo vira lista de pendências (a catraca serve para isso). Nos PRs
seguintes, o agente migra em lotes pequenos, separados de qualquer
mudança funcional. No último, com a lista zerada, a exceção sai da
verificação (Cap. 8).
