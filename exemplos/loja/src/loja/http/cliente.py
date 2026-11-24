"""Cliente HTTP único da loja (Capítulo 8)."""

import urllib.request


def buscar(url: str, tempo_limite: float = 5.0) -> bytes:
    """Faz um GET e devolve o corpo da resposta."""
    with urllib.request.urlopen(url, timeout=tempo_limite) as r:
        return r.read()
