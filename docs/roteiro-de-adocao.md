# Roteiro de adoção

Versão de consulta do Apêndice E do livro. A ordem segue as quatro
partes do livro, lidas como ciclo: diagnosticar, combinar princípios
e conter a deriva, governar e voltar a medir. Os prazos são sugestão
do autor; ajuste ao tamanho do time.

## Fase 1: diagnosticar (semanas 1 e 2)

| Passo | Artefato | Pronto quando |
|---|---|---|
| 1. Pôr no painel as mudanças em produção há mais de 14 dias sem reversão e a carga por revisor, ao lado da contagem de PRs | [`modelos/mudancas_qualificadas.sh`](modelos/mudancas_qualificadas.sh) (Cap. 1); painel (Cap. 4) | Cada medida de vazão tem uma de contrapeso ao lado |
| 2. Classificar os comentários de revisão de 20 PRs recentes | Categorias comportamento, estrutura, forma e escopo (Cap. 1) | O resultado foi discutido na retrospectiva |
| 3. Rodar a triagem do repositório | `contencao triagem`, `contencao raras`, `contencao localidade`, `contencao pontos-quentes` (Caps. 5, 4, 6 e 13) | Há uma lista curta de suspeitas, levada a quem conhece a arquitetura |
| 4. Preencher o checklist de diagnóstico | [checklist-diagnostico.md](checklist-diagnostico.md) | Cada item está marcado em um dos três níveis |

A fase termina com uma escolha: uma única área do sistema para
começar (Cap. 13).

## Fase 2: conter a deriva (semanas 3 a 8)

| Passo | Artefato | Pronto quando |
|---|---|---|
| 5. Enxugar o arquivo de instruções: regras críticas no topo, frase de precedência do código, teste ao lado de cada regra | [`modelos/AGENTS.md`](modelos/AGENTS.md); `contencao instrucoes` (Caps. 8 e 9) | Toda regra tem verificação ou foi cortada |
| 6. Registrar a decisão arquitetural que mais gera dúvida | [`modelos/ADR.md`](modelos/ADR.md) | O registro está no repositório e o arquivo de instruções aponta para ele |
| 7. Verificar as fronteiras da área escolhida | [`.importlinter` do exemplo](../exemplos/loja/.importlinter) (Cap. 11); `mypy --strict` nas fronteiras (Cap. 7) | Uma importação proibida faz o pipeline falhar |
| 8. Proteger os testes de aceitação | `contencao check-testes` (Cap. 10) | Mover ou alterar um teste protegido exige aprovação |
| 9. Montar as camadas de verificação, com exceções que vencem ou catraca no legado | [pipeline-em-camadas.md](pipeline-em-camadas.md); `contencao catraca` (Cap. 11) | Violação nova falha; as antigas estão listadas com motivo e prazo |
| 10. Mudar o fluxo das tarefas delegadas | [Cartões 1 e 2](cartoes.md); `contencao check-pr` (Cap. 12) | Os PRs de agente da área chegam com plano revisado e passam pelo cartão de revisão |

## Fase 3: governar (até o fim do trimestre)

| Passo | Artefato | Pronto quando |
|---|---|---|
| 11. Dar donos aos arquivos sensíveis | [`CODEOWNERS` do exemplo](../exemplos/loja/.github/CODEOWNERS) (Cap. 14) | Contratos, testes de aceitação e instruções só mudam com aprovação do dono |
| 12. Escrever a política de uso de agentes | [Cartão 3](cartoes.md#cartão-3-política-de-uso-de-agentes-em-uma-página) | As seis perguntas têm resposta aprovada pelo time |
| 13. Organizar a formação dos juniores | [Cartão 4](cartoes.md#cartão-4-formação-de-engenheiros-juniores) | Cada júnior tem a sua etapa combinada e um colega experiente ao lado |
| 14. Medir o custo por mudança | `contencao custo` (Cap. 15) | Há uma comparação antes e depois de uma fronteira ou regra nova |
| 15. Levar o resgate à segunda área | [Fluxograma de resgate](fluxogramas.md#roteiro-de-resgate-cap-13) | A primeira área está estável e a segunda foi escolhida pelos dados |

No fim do trimestre o ciclo recomeça pela Fase 1, com dados
próprios: toda medida usada como meta tende a perder o valor de
medida (Cap. 4, a partir de Goodhart, na formulação de Strathern,
1997).
