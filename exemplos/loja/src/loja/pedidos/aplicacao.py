"""Casos de uso de pedidos: orquestram o domínio."""

from decimal import Decimal

from loja.pedidos.dominio import Item, Pedido


def criar_pedido(itens: list[tuple[str, int, str]]) -> Pedido:
    """Cria um pedido a partir de (sku, quantidade, preço)."""
    pedido = Pedido()
    for sku, quantidade, preco in itens:
        pedido.adicionar(Item(sku, quantidade, Decimal(preco)))
    return pedido
