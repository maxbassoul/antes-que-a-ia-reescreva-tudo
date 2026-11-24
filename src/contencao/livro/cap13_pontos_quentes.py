"""Pontos quentes: arquivos grandes que mudam muito."""

import collections  # contador pronto
import pathlib  # caminhos de arquivos e pastas
import subprocess  # roda outros programas, como o git

# Pede ao git a lista de arquivos alterados em cada
# commit dos últimos seis meses (um por linha)
log = subprocess.run(
    [
        "git",
        "log",
        "--since=6 months ago",
        "--name-only",
        "--format=",
    ],
    capture_output=True,
    text=True,
    check=True,
).stdout
# Conta quantas vezes cada arquivo Python mudou
mudancas = collections.Counter(
    linha
    for linha in log.splitlines()
    if linha.endswith(".py")
)

ranking = []
for caminho, vezes in mudancas.items():
    arq = pathlib.Path(caminho)
    # ignora arquivos já removidos
    if arq.exists():
        linhas = len(
            arq.read_text(encoding="utf-8").splitlines()
        )
        # Nota = mudanças x tamanho: grande e mexido
        # com frequência é onde dói mais
        ranking.append(
            (vezes * linhas, vezes, linhas, caminho)
        )

# Mostra os dez de nota mais alta
for nota, vezes, linhas, caminho in sorted(
    ranking, reverse=True
)[:10]:
    print(
        f"{nota:8d} {vezes:3d} mudanças {linhas:5d} linhas"
        f" {caminho}"
    )
