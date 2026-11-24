"""Quantos módulos cada commit recente atravessa?"""

import collections  # contadores e dicionários prontos
import subprocess  # roda outros programas, como o git
import sys  # argumentos da linha de comando

# Pasta onde ficam os módulos (padrão: src/)
prefixo = sys.argv[1] if len(sys.argv) > 1 else "src/"
# Quantas partes do caminho formam um módulo:
# src/loja/pedidos -> 3 partes
nivel = 3
# Pede ao git os 200 últimos commits; cada commit
# aparece como "@código" seguido dos arquivos alterados
log = subprocess.run(
    [
        "git",
        "log",
        "-n",
        "200",
        "--name-only",
        "--format=@%h",
    ],
    capture_output=True,
    text=True,
    check=True,
).stdout

# Para cada commit, o conjunto de módulos que ele tocou
commits = collections.defaultdict(set)
atual = None
for linha in log.splitlines():
    if linha.startswith("@"):  # começou um novo commit
        atual = linha[1:]
    elif linha.startswith(prefixo):  # arquivo em src/
        partes = linha.split("/")
        # só conta arquivos dentro da pasta de um
        # módulo; src/loja/__init__.py fica de fora
        if len(partes) > nivel:
            commits[atual].add("/".join(partes[:nivel]))

# Quantos commits tocaram 1 módulo, 2 módulos, ...
distribuicao = collections.Counter(
    len(m) for m in commits.values()
)
for n, qtd in sorted(distribuicao.items()):
    print(f"{qtd:4d} commits tocaram {n} módulo(s)")
# Quais grupos de módulos mudam juntos com frequência
pares = collections.Counter(
    tuple(sorted(m))
    for m in commits.values()
    if len(m) > 1
)
for grupo, qtd in pares.most_common(5):  # os 5 maiores
    print(f"{qtd:4d}x juntos: {', '.join(grupo)}")
