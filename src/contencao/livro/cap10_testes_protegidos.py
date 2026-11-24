"""Falha se a mudança tocar testes protegidos."""

import os  # lê variáveis de ambiente
import subprocess  # roda outros programas, como o git
import sys  # argumentos e código de saída

# Ramo de comparação: o indicado no comando ou o main
BASE = sys.argv[1] if len(sys.argv) > 1 else "origin/main"
# a especificação do time: pastas que o agente não
# pode alterar sem aprovação humana
PROTEGIDOS = ("tests/aceitacao/",)

# Lista os arquivos alterados desde o ramo base.
# --no-renames: arquivo movido aparece como removido
# no lugar antigo e criado no novo; sem isso, quem
# tirasse um teste da pasta protegida passaria
alterados = subprocess.run(
    [
        "git",
        "diff",
        "--name-only",
        "--no-renames",
        f"{BASE}...HEAD",
    ],
    capture_output=True,
    text=True,
    check=True,
).stdout.splitlines()
# Fica só com os que estão nas pastas protegidas
tocados = [
    a for a in alterados if a.startswith(PROTEGIDOS)
]

# A aprovação vem de uma variável que só uma pessoa
# revisora liga no pipeline (TESTES_APROVADOS=sim)
if tocados and os.environ.get("TESTES_APROVADOS") != "sim":
    print("Testes de aceitação alterados; peça revisão:")
    print("\n".join(f"  {a}" for a in tocados))
    sys.exit(1)  # código 1: o pipeline marca falha
print("Nenhum teste protegido alterado sem aprovação.")
