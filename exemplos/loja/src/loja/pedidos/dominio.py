"""Agregado Pedido: as regras ficam no código."""

# dataclass gera automaticamente o construtor da classe
from dataclasses import dataclass

# Decimal faz contas exatas com dinheiro (sem os
# arredondamentos estranhos de números com vírgula)
from decimal import Decimal


# frozen=True: depois de criado, o item não muda mais
@dataclass(frozen=True)
class Item:
    sku: str  # código do produto
    quantidade: int
    preco: Decimal

    # Roda logo após a criação: recusa itens inválidos
    def __post_init__(self) -> None:
        if self.quantidade <= 0:
            raise ValueError(
                "quantidade deve ser positiva"
            )
        if self.preco < 0:
            raise ValueError("preço não pode ser negativo")


class Pedido:
    """Raiz do agregado: toda mudança passa por aqui."""

    def __init__(self) -> None:
        # nasce vazio e não pago: estado inicial válido.
        # O sublinhado (_itens) avisa: uso interno
        self._itens: list[Item] = []
        self._pago = False

    # @property: permite ler pedido.itens como um campo
    @property
    def itens(self) -> tuple[Item, ...]:
        # cópia imutável: quem está fora só lê
        return tuple(self._itens)

    @property
    def pago(self) -> bool:
        return self._pago

    def adicionar(self, item: Item) -> None:
        # pré-condição: pedido pago não muda
        if self._pago:
            raise ValueError(
                "pedido pago não aceita itens"
            )
        antes = len(self._itens)
        self._itens.append(item)
        # pós-condição: exatamente um item a mais
        # (assert é uma conferência interna)
        assert len(self._itens) == antes + 1

    def total(self) -> Decimal:
        # Soma preço x quantidade de cada item
        return sum(
            (i.preco * i.quantidade for i in self._itens),
            Decimal(0),
        )

    def pagar(self) -> None:
        # invariante do agregado: não se paga pedido vazio
        if not self._itens:
            raise ValueError(
                "pedido vazio não pode ser pago"
            )
        self._pago = True
