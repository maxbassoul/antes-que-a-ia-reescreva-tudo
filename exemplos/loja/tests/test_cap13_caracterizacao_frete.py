"""Antes de juntar duas cópias, fixe o que fazem."""

# Decimal faz contas exatas com dinheiro
from decimal import Decimal

import pytest  # ferramenta que roda os testes


# As duas cópias que o agente espalhou (simplificadas aqui)
# Frete: tarifa base por estado (UF) mais R$ 2,50 por
# quilo acima do primeiro
def frete_carrinho(peso_kg, uf):
    base = (
        Decimal("12.00")
        if uf == "SP"
        else Decimal("18.00")
    )
    return base + Decimal("2.50") * max(0, peso_kg - 1)


# Mesma regra, escrita de outro jeito
def frete_pedido(peso_kg, uf):
    base = (
        Decimal("18.00")
        if uf != "SP"
        else Decimal("12.00")
    )
    return base + Decimal("2.5") * max(peso_kg - 1, 0)


# A versão única que vai substituí-las
def calcular_frete(peso_kg: int, uf: str) -> Decimal:
    if peso_kg <= 0:
        raise ValueError("peso deve ser positivo")
    base = (
        Decimal("12.00")
        if uf == "SP"
        else Decimal("18.00")
    )
    return base + Decimal("2.50") * (peso_kg - 1)


# Exemplos de entrada (peso, estado) usados nos testes
CASOS = [(1, "SP"), (3, "SP"), (1, "BA"), (10, "RS")]


# parametrize: roda o mesmo teste uma vez por caso
# Passo 1: as duas cópias dão o mesmo resultado?
@pytest.mark.parametrize("peso, uf", CASOS)
def test_copias_concordam_entre_si(peso, uf):
    assert frete_carrinho(peso, uf) == frete_pedido(
        peso, uf
    )


# Passo 2: a versão única repete esse resultado?
@pytest.mark.parametrize("peso, uf", CASOS)
def test_versao_unica_preserva_o_comportamento(peso, uf):
    assert calcular_frete(peso, uf) == frete_carrinho(
        peso, uf
    )


# Peso zero ou negativo: as cópias cobravam a tarifa
# base, e a versão única recusa. Decisão do time.
@pytest.mark.parametrize("peso", [0, -1])
def test_borda_muda_de_proposito(peso):
    assert frete_carrinho(peso, "SP") == Decimal("12.00")
    # pytest.raises: o teste passa se surgir o erro
    with pytest.raises(ValueError):
        calcular_frete(peso, "SP")
