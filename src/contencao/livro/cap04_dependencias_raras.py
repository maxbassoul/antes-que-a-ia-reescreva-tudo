"""Lista dependências raras entre pacotes (suspeitas)."""

import ast  # lê código Python como uma árvore
import collections  # dicionários prontos
import pathlib  # caminhos de arquivos e pastas
import sys  # argumentos da linha de comando

raiz = pathlib.Path(sys.argv[1])  # ex.: src/loja
# Quantas partes do nome formam um pacote:
# loja.pedidos, loja.estoque... -> 2 partes
nivel = 2
# Para cada par (origem, destino), os arquivos que
# criam essa dependência
pares = collections.defaultdict(set)


# Devolve os nomes completos que uma linha de import
# traz para dentro do arquivo
def alvos(no: ast.AST, partes: list[str]) -> list[str]:
    if isinstance(no, ast.Import):  # import x.y
        return [a.name for a in no.names]
    if not isinstance(no, ast.ImportFrom):
        return []  # não é uma linha de import
    base = no.module.split(".") if no.module else []
    if no.level:  # relativo: 'from ..estoque import x'
        # cada ponto sobe uma pasta a partir do arquivo
        pacote = partes[:-1]
        base = pacote[: len(pacote) - no.level + 1] + base
    return [".".join(base + [a.name]) for a in no.names]


# O nome pertence ao nosso projeto?
def interno(nome: str) -> bool:
    # 'lojavirtual' não é 'loja'
    return nome == raiz.name or nome.startswith(
        raiz.name + "."
    )


# Percorre cada arquivo .py e registra as importações
# que saem do seu pacote para outro pacote do projeto
for arq in raiz.rglob("*.py"):
    # src/loja/pedidos/servico.py -> loja, pedidos, ...
    partes = list(
        arq.relative_to(raiz.parent).with_suffix("").parts
    )
    origem = ".".join(partes[:nivel])
    arvore = ast.parse(arq.read_text(encoding="utf-8"))
    for no in ast.walk(arvore):
        for alvo in alvos(no, partes):
            destino = ".".join(alvo.split(".")[:nivel])
            if interno(alvo) and destino != origem:
                pares[(origem, destino)].add(
                    arq.as_posix()
                )

# Mostra primeiro as dependências que aparecem em
# menos arquivos
for (origem, destino), arquivos in sorted(
    pares.items(), key=lambda p: len(p[1])
):
    # rara: aparece em poucos arquivos
    if len(arquivos) <= 2:
        print(f"{origem} -> {destino}: {sorted(arquivos)}")
