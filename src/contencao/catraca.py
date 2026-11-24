"""Catraca: aceita as violações de hoje e barra só as novas.

Padrão descrito por Isberg (2026) e discutido no Capítulo 11 do
livro. A ferramenta não sabe o que é uma violação: ela recebe a
saída de qualquer verificador (ruff, mypy, lint-imports, Semgrep),
uma violação por linha, e compara com a linha de base guardada em
`.catraca.json`, que fica versionada no repositório.

Uso:
  ruff check . --output-format concise > violacoes.txt
  contencao catraca registrar violacoes.txt   # cria a base
  contencao catraca verificar violacoes.txt   # no pipeline

Regras:
- violação nova (que não está na base) faz o comando falhar;
- violação corrigida sai da base sozinha: a catraca só gira para o
  lado de melhorar;
- exceções têm motivo e prazo; prazo vencido faz o comando falhar.
"""

import collections
import datetime
import json
import pathlib
import re
import sys
from typing import Any

# Conteúdo do .catraca.json: violações e exceções
Dados = dict[str, Any]

BASE_PADRAO = pathlib.Path(".catraca.json")

# Números de linha e coluna mudam quando alguém edita o arquivo
# acima da violação; tirá-los evita alarme falso. Ex.: o trecho
# "src/a.py:12:5: F401" vira "src/a.py: F401".
POSICAO = re.compile(r":\d+(?::\d+)?(?=[:\s]|$)")


def normalizar(linha: str) -> str:
    """Tira posição e espaços extras de uma linha de violação."""
    return " ".join(POSICAO.sub("", linha).split())


def ler_violacoes(arquivo: str) -> collections.Counter[str]:
    """Conta as violações do arquivo (ou da entrada, com '-')."""
    if arquivo == "-":
        texto = sys.stdin.read()
    else:
        texto = pathlib.Path(arquivo).read_text(encoding="utf-8")
    linhas = (normalizar(x) for x in texto.splitlines())
    # Counter guarda quantas vezes cada violação aparece: uma
    # segunda cópia da mesma violação no mesmo arquivo é nova
    return collections.Counter(x for x in linhas if x)


def carregar(base: pathlib.Path) -> Dados:
    """Lê a linha de base; devolve uma vazia se não existir."""
    if not base.exists():
        return {"violacoes": {}, "excecoes": []}
    dados: Dados = json.loads(base.read_text(encoding="utf-8"))
    return dados


def salvar(base: pathlib.Path, dados: Dados) -> None:
    """Grava a base em ordem estável, para diffs legíveis."""
    dados["violacoes"] = dict(sorted(dados["violacoes"].items()))
    texto = json.dumps(dados, ensure_ascii=False, indent=2)
    base.write_text(texto + "\n", encoding="utf-8")


def excecoes_validas(
    dados: Dados, hoje: datetime.date
) -> tuple[set[str], list[str]]:
    """Separa exceções em vigor das vencidas ou sem motivo."""
    vigentes: set[str] = set()
    problemas: list[str] = []
    for exc in dados.get("excecoes", []):
        motivo = exc.get("motivo", "").strip()
        prazo = datetime.date.fromisoformat(exc["prazo"])
        if not motivo:
            problemas.append(f"exceção sem motivo: {exc}")
        elif prazo < hoje:
            problemas.append(
                f"exceção vencida em {prazo}: {exc['violacao']}"
            )
        else:
            vigentes.add(normalizar(exc["violacao"]))
    return vigentes, problemas


def registrar(arquivo: str, base: pathlib.Path) -> int:
    """Cria ou substitui a linha de base com as violações de hoje."""
    dados = carregar(base)
    dados["violacoes"] = dict(ler_violacoes(arquivo))
    salvar(base, dados)
    total = sum(dados["violacoes"].values())
    print(f"Linha de base registrada: {total} violações.")
    return 0


def verificar(
    arquivo: str,
    base: pathlib.Path,
    hoje: datetime.date | None = None,
) -> int:
    """Falha com violação nova ou exceção vencida; gira a catraca."""
    hoje = hoje or datetime.date.today()
    dados = carregar(base)
    antes: collections.Counter[str] = collections.Counter(
        dados["violacoes"]
    )
    agora = ler_violacoes(arquivo)
    vigentes, problemas = excecoes_validas(dados, hoje)
    # Novas: aparecem mais vezes agora do que na base
    novas = [
        v
        for v, n in (agora - antes).items()
        for _ in range(n)
        if v not in vigentes
    ]
    # Corrigidas: estavam na base e sumiram (ou diminuíram)
    corrigidas = antes - agora
    if corrigidas:
        dados["violacoes"] = dict(antes - corrigidas)
        salvar(base, dados)
        n = sum(corrigidas.values())
        print(f"A catraca girou: {n} violação(ões) saíram da base.")
        print("Inclua o .catraca.json atualizado no commit.")
    for v in novas:
        print(f"NOVA: {v}")
    for p in problemas:
        print(f"PRAZO: {p}")
    if novas or problemas:
        print("Falha: corrija o código ou registre a exceção com")
        print("motivo e prazo no .catraca.json (Capítulo 11).")
        return 1
    print("Nenhuma violação nova.")
    return 0


def main(args: list[str]) -> int:
    """Subcomando `contencao catraca registrar|verificar ARQ`."""
    if len(args) < 2 or args[0] not in ("registrar", "verificar"):
        print("uso: contencao catraca registrar|verificar ARQUIVO")
        print("     [--base CAMINHO]  (ARQUIVO '-' lê da entrada)")
        return 2
    base = BASE_PADRAO
    if "--base" in args:
        base = pathlib.Path(args[args.index("--base") + 1])
    if args[0] == "registrar":
        return registrar(args[1], base)
    return verificar(args[1], base)
