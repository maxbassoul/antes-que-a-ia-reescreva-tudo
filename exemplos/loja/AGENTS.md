# AGENTS.md: loja (exemplo do livro)

Regras críticas (verificadas no CI):
- `loja.pedidos.dominio` não importa as camadas de cima
  (`.importlinter`).
- Pedidos, estoque e faturamento não importam uns aos outros.
- Só `src/loja/http/` fala com a rede
  (`tests/test_cap08_rede_so_por_http.py`).
- Testes em `tests/aceitacao/` só mudam com aprovação do dono.

Quando este arquivo e o código discordarem, siga as convenções do
código e aponte cada inconsistência na resposta final.

Antes de encerrar: `pytest`, `ruff check .` e `lint-imports`.
Decisões: `docs/adr/`. Mapa dos módulos: `MAPA.md`.
