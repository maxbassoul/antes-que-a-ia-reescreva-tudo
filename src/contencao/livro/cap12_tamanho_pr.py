"""Alerta para pull requests grandes demais."""

import subprocess  # roda outros programas, como o git
import sys  # argumentos e código de saída

# Ramo de comparação: o indicado no comando ou o main
BASE = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
# combinado pelo time; revise com os seus dados
MAX_LINHAS = 400
# quantos módulos de src/loja/ uma mudança pode tocar
MAX_MODULOS = 2
# o pacote do exemplo: src/loja/<módulo>/...
PACOTE = ["src", "loja"]

# Pede ao git, para cada arquivo alterado, as linhas
# adicionadas e removidas (separadas por tabulação).
# --no-renames: arquivo movido aparece como removido
# num lugar e criado no outro, sem o formato a => b
saida = subprocess.run(
    [
        "git",
        "diff",
        "--numstat",
        "--no-renames",
        f"{BASE}...HEAD",
    ],
    capture_output=True,
    text=True,
    check=True,
).stdout
linhas, modulos = 0, set()
for registro in saida.splitlines():
    adicionadas, removidas, caminho = registro.split("\t")
    # "-" indica arquivo binário
    if adicionadas != "-":
        linhas += int(adicionadas) + int(removidas)
    # src/loja/pedidos/x.py -> o módulo é "pedidos"
    partes = caminho.split("/")
    if partes[:2] == PACOTE and len(partes) > 3:
        modulos.add(partes[2])

print(
    f"{linhas} linhas alteradas em {len(modulos)} "
    f"módulo(s): {sorted(modulos)}"
)
# Passou de um dos limites: avisa e sai com código 1,
# que o pipeline entende como falha
if linhas > MAX_LINHAS or len(modulos) > MAX_MODULOS:
    print(
        "Divida em pull requests menores, um por intenção."
    )
    sys.exit(1)
