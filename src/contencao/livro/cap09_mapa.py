"""Gera MAPA.md: resumo por módulo e nomes públicos."""

import ast  # lê código Python como uma árvore
import pathlib  # caminhos de arquivos e pastas
import sys  # argumentos da linha de comando

raiz = pathlib.Path(sys.argv[1])  # ex.: src/loja
# Linhas do mapa, começando pelo título
linhas = [f"# Mapa de {raiz.name}", ""]

# Um pacote Python é uma pasta com __init__.py
for pacote in sorted(
    p
    for p in raiz.iterdir()
    if (p / "__init__.py").exists()
):
    arvore = ast.parse(
        (pacote / "__init__.py").read_text(
            encoding="utf-8"
        )
    )
    # A docstring (texto entre aspas triplas no topo
    # do __init__.py) é o resumo do pacote; fica só a
    # primeira linha
    resumo = (
        ast.get_docstring(arvore) or "SEM DESCRIÇÃO"
    ).splitlines()[0]
    linhas.append(f"## {pacote.name}: {resumo}")
    for arq in sorted(pacote.glob("*.py")):
        if arq.name == "__init__.py":
            continue  # já foi lido acima
        nos = ast.parse(
            arq.read_text(encoding="utf-8")
        ).body
        # Funções e classes cujo nome não começa com _
        # (em Python, _ indica uso interno)
        publicos = [
            n.name
            for n in nos
            if isinstance(
                n, (ast.FunctionDef, ast.ClassDef)
            )
            and not n.name.startswith("_")
        ]
        linhas.append(
            f"- `{arq.name}`: "
            f"{', '.join(publicos) or '(nada público)'}"
        )
    linhas.append("")

# Grava o mapa no arquivo e também mostra na tela
pathlib.Path("MAPA.md").write_text(
    "\n".join(linhas), encoding="utf-8"
)
print("\n".join(linhas))
