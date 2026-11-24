"""Aceitação: o comportamento que o time protege."""

from decimal import Decimal

import pytest

from loja.pedidos.aplicacao import criar_pedido


def test_total_soma_preco_vezes_quantidade():
    pedido = criar_pedido([("A1", 2, "10.00"), ("B2", 1, "5.50")])
    assert pedido.total() == Decimal("25.50")


def test_pedido_vazio_nao_pode_ser_pago():
    pedido = criar_pedido([])
    with pytest.raises(ValueError):
        pedido.pagar()
