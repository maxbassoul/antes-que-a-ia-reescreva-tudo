# Antes que a IA Reescreva Tudo: material complementar

Ferramentas, cartões, roteiros e diagramas do livro **Antes que a IA
Reescreva Tudo**, de Diego Marques de Carvalho, para conter a deriva
arquitetural em repositórios onde agentes de IA escrevem código.

<img src="assets/qrcode.png" alt="Código QR com o endereço deste repositório" width="140">

O livro concentra os princípios, as evidências e os critérios de
decisão. Este repositório guarda o que muda depressa demais para o
papel: os scripts testados, o comando que os reúne e as versões
prontas das verificações.

## Por onde começar

1. Leia o [roteiro de adoção](docs/roteiro-de-adocao.md): três fases,
   do diagnóstico à governança, com o artefato de cada passo.
2. Instale as ferramentas e rode a triagem no seu repositório:

   ```sh
   pip install "git+https://github.com/maxbassoul/antes-que-a-ia-reescreva-tudo"
   contencao              # lista os subcomandos
   contencao triagem .    # triagem de dez minutos (Cap. 5)
   ```

3. Use os [cartões](docs/cartoes.md) no dia a dia: antes de delegar,
   ao revisar, para escrever a política de uso e formar juniores.

## O que tem aqui

| Pasta ou arquivo | O que é | No livro |
|---|---|---|
| [`src/contencao/livro/`](src/contencao/livro/) | Cópias exatas dos scripts dos capítulos | Caps. 4, 5, 6, 9, 10, 12, 13 e 15 |
| `contencao` | Comando único que roda esses scripts | — |
| `contencao catraca` | Linha de base de violações: barra só as novas, gira quando algo é corrigido, falha em exceção vencida | Cap. 11 |
| `contencao instrucoes` | Verifica AGENTS.md ou CLAUDE.md: caracteres invisíveis, caminhos que não existem, tamanho, frase de precedência | Cap. 9 |
| [`exemplos/loja/`](exemplos/loja/) | O projeto `loja` do livro, com funções de aptidão, contrato do import-linter, testes de aceitação, ADR, AGENTS.md e MAPA.md | Caps. 5 a 13 |
| [`docs/roteiro-de-adocao.md`](docs/roteiro-de-adocao.md) | Roteiro em três fases | Apêndice E |
| [`docs/cartoes.md`](docs/cartoes.md) | Quatro cartões operacionais | Apêndice F |
| [`docs/pipeline-em-camadas.md`](docs/pipeline-em-camadas.md) | As quatro camadas de verificação | Apêndice G |
| [`docs/fluxogramas.md`](docs/fluxogramas.md) | Cinco fluxogramas de decisão | Caps. 9, 11, 12 e 13 |
| [`docs/checklist-diagnostico.md`](docs/checklist-diagnostico.md) | Checklist de diagnóstico da deriva | Apêndice A |
| [`docs/modelos/`](docs/modelos/) | Modelos de AGENTS.md e ADR, e os comandos de mudanças qualificadas | Apêndices B e C, Cap. 1 |
| [`.github/workflows/verificacao.yml`](.github/workflows/verificacao.yml) | Pipeline que roda as camadas 2 e 3 sobre a `loja` | Apêndice G |

## Subcomandos

| Comando | O que faz | Cap. |
|---|---|---|
| `contencao raras src/meupacote` | Dependências raras entre pacotes | 4 |
| `contencao triagem .` | Triagem de dez minutos | 5 |
| `contencao localidade src/` | Quantos módulos cada commit atravessa | 6 |
| `contencao mapa src/meupacote` | Gera o MAPA.md | 9 |
| `contencao check-testes origin/main` | Falha se a mudança tocar testes protegidos | 10 |
| `contencao check-pr origin/main` | Alerta para PR grande ou com muitos módulos | 12 |
| `contencao pontos-quentes` | Arquivos grandes que mudam muito | 13 |
| `contencao custo dados.csv ...` | Custo por mudança entregue, por módulo | 15 |
| `contencao catraca registrar\|verificar ARQ` | Catraca de violações | 11 |
| `contencao instrucoes AGENTS.md` | Higiene do arquivo de instruções | 9 |

Os scripts do livro seguem a estrutura `src/<pacote>/<módulo>/` e
usam os limites descritos nos capítulos (por exemplo, 400 linhas por
PR e dois módulos). Esses números são decisões de time, não valores
validados por pesquisa: comece com alertas que não bloqueiam e
ajuste com os seus dados. Para mudar um limite, copie o script do
capítulo e edite a constante no topo.

## Como contribuir

Correções são bem-vindas por pull request. Os arquivos em
`src/contencao/livro/` precisam continuar idênticos aos do livro; uma
mudança neles vai para a próxima edição e passa pela aprovação do
autor (`.github/CODEOWNERS`).

## Licença e citação

O código está sob a licença MIT ([`LICENSE`](LICENSE)); os textos e
diagramas, sob CC BY 4.0 ([`LICENSE-CONTEUDO.md`](LICENSE-CONTEUDO.md)).
Os dois permitem qualquer uso, desde que a fonte seja citada:

> CARVALHO, Diego Marques de. **Antes que a IA reescreva tudo**.
> Material complementar disponível em:
> <https://github.com/maxbassoul/antes-que-a-ia-reescreva-tudo>.
