# ADR-0012: divisão do módulo de relatórios adiada

- Situação: aceita
- Data: 2026-11-23

## Contexto
No livro, o módulo `loja/legado/relatorios.py` passa do limite de
tamanho de arquivo combinado pelo time (teste do Capítulo 11). Neste
exemplo o arquivo é curto: a exceção existe para mostrar o mecanismo.

## Decisão
A divisão fica para depois da migração dos relatórios. Até lá, o
arquivo é uma exceção com motivo e prazo (2027-03-31) em
`tests/test_cap11_excecoes_com_prazo.py`.

## Consequências
Quando o prazo vencer, o teste falha e o time decide de novo:
dividir o arquivo ou renovar a exceção com um motivo novo.
