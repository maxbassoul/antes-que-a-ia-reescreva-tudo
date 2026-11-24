"""Comando único `contencao`, com um subcomando por ferramenta.

Os subcomandos que vêm do livro rodam o script do capítulo sem
mudar uma linha dele: o comando só monta os argumentos e chama o
arquivo, como se você tivesse digitado `python script.py ...`.
"""

import pathlib
import runpy
import sys

from contencao import catraca, instrucoes

# Pasta com as cópias exatas dos scripts do livro
LIVRO = pathlib.Path(__file__).parent / "livro"

# subcomando: (arquivo do livro, capítulo, o que faz, uso)
SCRIPTS = {
    "raras": (
        "cap04_dependencias_raras.py",
        4,
        "dependências raras entre pacotes (suspeitas)",
        "PASTA_DO_PACOTE (ex.: src/loja)",
    ),
    "triagem": (
        "cap05_triagem.py",
        5,
        "triagem de dez minutos do repositório",
        "[PASTA] (padrão: .)",
    ),
    "localidade": (
        "cap06_localidade.py",
        6,
        "quantos módulos cada commit recente atravessa",
        "[PREFIXO] (padrão: src/)",
    ),
    "mapa": (
        "cap09_mapa.py",
        9,
        "gera MAPA.md com resumo e nomes públicos",
        "PASTA_DO_PACOTE (ex.: src/loja)",
    ),
    "check-testes": (
        "cap10_testes_protegidos.py",
        10,
        "falha se a mudança tocar testes protegidos",
        "[BASE] (padrão: origin/main)",
    ),
    "check-pr": (
        "cap12_tamanho_pr.py",
        12,
        "alerta para PR grande demais ou com muitos módulos",
        "[BASE] (padrão: origin/main)",
    ),
    "pontos-quentes": (
        "cap13_pontos_quentes.py",
        13,
        "arquivos grandes que mudam muito",
        "",
    ),
    "custo": (
        "cap15_custo.py",
        15,
        "custo por mudança entregue, por módulo",
        "CSV PRECO_MIL_TOKENS PRECO_MINUTO_CI CUSTO_HORA",
    ),
}

# Ferramentas novas do repositório (não estão no livro)
NOVAS = {
    "catraca": (catraca.main, "linha de base de violações (Cap. 11)"),
    "instrucoes": (
        instrucoes.main,
        "verifica o AGENTS.md ou CLAUDE.md (Cap. 9)",
    ),
}


def ajuda() -> str:
    """Texto de ajuda com todos os subcomandos."""
    linhas = ["uso: contencao SUBCOMANDO [ARGUMENTOS]", ""]
    linhas.append("Scripts do livro (cópia exata):")
    for nome, (_, cap, desc, uso) in SCRIPTS.items():
        linhas.append(f"  {nome:15} Cap. {cap:2}  {desc}")
        if uso:
            linhas.append(f"  {'':15}          args: {uso}")
    linhas.append("")
    linhas.append("Ferramentas do repositório:")
    for nome, (_, desc) in NOVAS.items():
        linhas.append(f"  {nome:15} {desc}")
    return "\n".join(linhas)


def main(argv: list[str] | None = None) -> int:
    """Ponto de entrada do comando `contencao`."""
    args = sys.argv[1:] if argv is None else argv
    if not args or args[0] in ("-h", "--help", "ajuda"):
        print(ajuda())
        return 0
    nome, resto = args[0], args[1:]
    if nome in NOVAS:
        return NOVAS[nome][0](resto)
    if nome not in SCRIPTS:
        print(f"subcomando desconhecido: {nome}\n")
        print(ajuda())
        return 2
    arquivo = LIVRO / SCRIPTS[nome][0]
    # O script do livro lê sys.argv; montamos como na linha
    # de comando e restauramos depois
    antigo = sys.argv
    sys.argv = [str(arquivo), *resto]
    try:
        runpy.run_path(str(arquivo), run_name="__main__")
    except SystemExit as fim:  # o script pode chamar sys.exit
        codigo = fim.code
        return codigo if isinstance(codigo, int) else 1
    finally:
        sys.argv = antigo
    return 0


if __name__ == "__main__":
    sys.exit(main())
