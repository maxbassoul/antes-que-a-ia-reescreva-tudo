"""Cálculo de frete por peso e estado."""

from decimal import Decimal

TAXA_UF = {"SP": Decimal("1.0"), "BA": Decimal("1.4")}


def calcular_frete(peso_kg: int, uf: str) -> Decimal:
    """Tarifa base mais valor por quilo, ajustada pelo estado."""
    if peso_kg <= 0:
        raise ValueError("peso deve ser positivo")
    taxa = TAXA_UF.get(uf, Decimal("1.2"))
    return (Decimal(10) + Decimal(2) * peso_kg) * taxa
