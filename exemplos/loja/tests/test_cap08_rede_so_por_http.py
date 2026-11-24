"""Função de aptidão: só loja.http fala com a rede."""

import ast  # lê código Python como uma árvore
import pathlib  # caminhos de arquivos e pastas

# Pasta do pacote, a partir da pasta tests/
RAIZ = (
    pathlib.Path(__file__).parent.parent / "src" / "loja"
)
# Bibliotecas que acessam a rede diretamente
PROIBIDOS = (
    "requests",
    "httpx",
    "urllib.request",
    "http.client",
)
# Único lugar autorizado a usá-las
PERMITIDO = RAIZ / "http"


# Nomes completos de tudo o que um arquivo importa
def importados(arq: pathlib.Path) -> set[str]:
    # 'from http import client' vira 'http' e 'http.client'
    nomes: set[str] = set()
    arvore = ast.parse(arq.read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        if isinstance(no, ast.Import):  # import x
            nomes |= {a.name for a in no.names}
        elif isinstance(no, ast.ImportFrom) and no.module:
            if no.level:  # import relativo: é do projeto
                continue
            nomes.add(no.module)  # from x import y
            nomes |= {
                f"{no.module}.{a.name}" for a in no.names
            }
    return nomes


def proibido(nome: str) -> bool:
    # 'requests.exceptions' também conta como 'requests'
    return any(
        nome == p or nome.startswith(p + ".")
        for p in PROIBIDOS
    )


# Lista, em ordem, os nomes proibidos de um arquivo
def infracoes(arq: pathlib.Path) -> list[str]:
    return sorted(
        n for n in importados(arq) if proibido(n)
    )


# O teste: nenhum arquivo fora de loja/http/ importa
# bibliotecas de rede
def test_rede_so_pelo_modulo_http():
    infratores = [
        f"{arq.relative_to(RAIZ)}: {infracoes(arq)}"
        for arq in RAIZ.rglob("*.py")
        if PERMITIDO not in arq.parents and infracoes(arq)
    ]
    # A mensagem de falha diz ao agente o que fazer
    assert not infratores, "use loja.http: " + "; ".join(
        infratores
    )
