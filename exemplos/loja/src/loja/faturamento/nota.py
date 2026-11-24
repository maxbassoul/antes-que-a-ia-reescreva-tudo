"""Valor da nota a partir do total e do frete."""

from decimal import Decimal


def valor_da_nota(total: Decimal, frete: Decimal) -> Decimal:
    """Soma o total dos itens ao frete."""
    return total + frete
