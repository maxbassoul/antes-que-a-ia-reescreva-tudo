"""Verifica um arquivo de instruções (AGENTS.md, CLAUDE.md).

Quatro checagens, todas tiradas do Capítulo 9 do livro:

1. Caracteres invisíveis ou de direção do texto. Em março de 2025,
   a Pillar Security mostrou instruções maliciosas escondidas em
   arquivos de regras com caracteres Unicode invisíveis.
2. Tamanho. Isberg sugere um arquivo raiz de 10 a 20 linhas, só com
   o que vale no projeto inteiro; acima disso, emitimos aviso. O
   limite que falha é decisão do time (--max-linhas).
3. Caminhos citados que não existem. Um arquivo que aponta para o
   que sumiu é obedecido ao pé da letra e produz veredito falso.
4. Frase de precedência. Xu e Wu (2026) mediram o efeito de dizer
   ao agente que siga o código quando arquivo e código discordam.
   A ausência gera aviso, não falha.

Uso: contencao instrucoes AGENTS.md [--max-linhas N] [--raiz DIR]
"""

import pathlib
import re
import unicodedata

# Caracteres que não aparecem na tela ou mudam a direção do texto
INVISIVEIS = set(
    [chr(c) for c in range(0x200B, 0x2010)]  # espaços de largura 0
    + [chr(c) for c in range(0x202A, 0x202F)]  # direção (bidi)
    + [chr(c) for c in range(0x2060, 0x2065)]  # junções invisíveis
    + [chr(c) for c in range(0x2066, 0x206A)]  # isolamento bidi
    + ["﻿", "­", "᠎"]
)
# Bloco de "tags" Unicode, usado para esconder texto
TAGS = range(0xE0000, 0xE0080)

LINHAS_SUGERIDAS = 20  # teto sugerido por Isberg para o raiz

# Caminho entre crases, como `src/loja/http/` ou `MAPA.md`
CAMINHO = re.compile(r"`([\w.\-/]+(?:/|\.\w{1,5}))`")

# Palavras que costumam aparecer na frase de precedência
PRECEDENCIA = re.compile(
    r"(discord|diverg|conflit|disagree|conflict)", re.IGNORECASE
)


def invisiveis(texto: str) -> list[str]:
    """Lista linha e código de cada caractere invisível."""
    achados = []
    for n, linha in enumerate(texto.splitlines(), start=1):
        for ch in linha:
            cod = ord(ch)
            outro = unicodedata.category(ch) == "Cf"
            if ch in INVISIVEIS or cod in TAGS or outro:
                achados.append(f"linha {n}: U+{cod:04X}")
    return achados


def caminhos_ausentes(texto: str, raiz: pathlib.Path) -> list[str]:
    """Caminhos citados entre crases que não existem na raiz."""
    faltam = []
    for caminho in sorted(set(CAMINHO.findall(texto))):
        if "<" in caminho or caminho.startswith("http"):
            continue  # modelo genérico ou endereço da web
        if not (raiz / caminho).exists():
            faltam.append(caminho)
    return faltam


def verificar(
    arquivo: pathlib.Path,
    raiz: pathlib.Path,
    max_linhas: int | None = None,
) -> tuple[list[str], list[str]]:
    """Devolve (erros, avisos) do arquivo de instruções."""
    texto = arquivo.read_text(encoding="utf-8")
    erros, avisos = [], []
    for achado in invisiveis(texto):
        erros.append(f"caractere invisível, {achado}")
    for caminho in caminhos_ausentes(texto, raiz):
        erros.append(f"caminho citado não existe: {caminho}")
    n = len(texto.splitlines())
    if max_linhas is not None and n > max_linhas:
        erros.append(f"{n} linhas, acima do limite de {max_linhas}")
    elif n > LINHAS_SUGERIDAS:
        avisos.append(
            f"{n} linhas; Isberg sugere 10 a 20 no arquivo raiz"
        )
    if not PRECEDENCIA.search(texto):
        avisos.append(
            "sem frase de precedência: diga o que fazer quando "
            "o arquivo e o código discordarem (Cap. 9)"
        )
    return erros, avisos


def main(args: list[str]) -> int:
    """Subcomando `contencao instrucoes ARQUIVO`."""
    if not args:
        print("uso: contencao instrucoes ARQUIVO [--max-linhas N]")
        print("     [--raiz PASTA]")
        return 2
    arquivo = pathlib.Path(args[0])
    raiz = arquivo.parent
    max_linhas = None
    if "--raiz" in args:
        raiz = pathlib.Path(args[args.index("--raiz") + 1])
    if "--max-linhas" in args:
        max_linhas = int(args[args.index("--max-linhas") + 1])
    erros, avisos = verificar(arquivo, raiz, max_linhas)
    for a in avisos:
        print(f"AVISO: {a}")
    for e in erros:
        print(f"ERRO: {e}")
    if erros:
        return 1
    print(f"{arquivo}: sem erros.")
    return 0
