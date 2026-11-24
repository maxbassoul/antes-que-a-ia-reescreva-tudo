"""Entrada de pedidos: traduz dados externos em casos de uso."""

from loja.pedidos.aplicacao import criar_pedido


def total_do_pedido(dados: list[dict[str, str]]) -> str:
    """Recebe itens como texto e devolve o total como texto."""
    itens = [
        (d["sku"], int(d["quantidade"]), d["preco"])
        for d in dados
    ]
    return str(criar_pedido(itens).total())
