"""Reserva de estoque por código de produto."""


def reservar(saldo: dict[str, int], sku: str, qtd: int) -> None:
    """Baixa a quantidade do saldo; recusa saldo negativo."""
    if saldo.get(sku, 0) < qtd:
        raise ValueError("estoque insuficiente")
    saldo[sku] -= qtd
