"""Triagem: o repositório é amigável a agentes?"""

import pathlib  # caminhos de arquivos e pastas
import sys  # argumentos da linha de comando

# Pasta a examinar: a indicada no comando ou a atual (.)
raiz = pathlib.Path(
    sys.argv[1] if len(sys.argv) > 1 else "."
)

# 1) Existe arquivo de instruções? De que tamanho?
for nome in ("AGENTS.md", "CLAUDE.md"):
    arq = raiz / nome
    if arq.exists():
        linhas = len(
            arq.read_text(encoding="utf-8").splitlines()
        )
        print(f"{nome}: {linhas} linhas")

# 2) Quantos arquivos de teste o projeto tem?
testes = list(raiz.rglob("test_*.py"))
print(f"arquivos de teste: {len(testes)}")

# 3) Há regras de dependência configuradas para o
#    import-linter em algum destes arquivos?
regras = [
    p
    for p in (
        "pyproject.toml",
        "setup.cfg",
        ".importlinter",
    )
    if (raiz / p).exists()
    and "importlinter"
    in (raiz / p).read_text(encoding="utf-8")
]
print(f"regras de dependência em: {regras or 'nenhuma'}")

# 4) Quais são os maiores arquivos Python? Monta pares
#    (linhas, arquivo), ignorando o ambiente virtual
#    (.venv), e ordena do maior para o menor
tamanhos = sorted(
    (
        (
            len(
                p.read_text(encoding="utf-8").splitlines()
            ),
            p,
        )
        for p in raiz.rglob("*.py")
        if ".venv" not in p.parts
    ),
    reverse=True,
)
print("maiores arquivos Python:")
for linhas, caminho in tamanhos[:10]:  # só os dez maiores
    print(f"  {linhas:6d}  {caminho.relative_to(raiz)}")
