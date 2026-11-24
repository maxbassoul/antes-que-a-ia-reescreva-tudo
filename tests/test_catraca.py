"""Testes da catraca: só barra o que é novo."""

import datetime
import json

from contencao import catraca

HOJE = datetime.date(2026, 11, 23)


def escrever(tmp_path, nome, linhas):
    arq = tmp_path / nome
    arq.write_text("\n".join(linhas) + "\n", encoding="utf-8")
    return str(arq)


def test_normalizar_tira_linha_e_coluna():
    assert catraca.normalizar("src/a.py:12:5: F401 x") == (
        "src/a.py: F401 x"
    )


def test_violacao_antiga_passa_e_nova_falha(tmp_path):
    base = tmp_path / ".catraca.json"
    antes = escrever(tmp_path, "a.txt", ["src/a.py:1:1: F401 os"])
    assert catraca.registrar(antes, base) == 0
    # A antiga mudou de linha: continua aceita
    mesma = escrever(tmp_path, "b.txt", ["src/a.py:9:1: F401 os"])
    assert catraca.verificar(mesma, base, HOJE) == 0
    nova = escrever(
        tmp_path,
        "c.txt",
        ["src/a.py:9:1: F401 os", "src/b.py:2:1: F841 x"],
    )
    assert catraca.verificar(nova, base, HOJE) == 1


def test_copia_extra_da_mesma_violacao_e_nova(tmp_path):
    base = tmp_path / ".catraca.json"
    um = escrever(tmp_path, "a.txt", ["src/a.py:1:1: F401 os"])
    catraca.registrar(um, base)
    dois = escrever(
        tmp_path,
        "b.txt",
        ["src/a.py:1:1: F401 os", "src/a.py:7:1: F401 os"],
    )
    assert catraca.verificar(dois, base, HOJE) == 1


def test_correcao_gira_a_catraca(tmp_path):
    base = tmp_path / ".catraca.json"
    antes = escrever(
        tmp_path, "a.txt", ["src/a.py:1:1: F401 os", "src/b.py: E1"]
    )
    catraca.registrar(antes, base)
    depois = escrever(tmp_path, "b.txt", ["src/b.py: E1"])
    assert catraca.verificar(depois, base, HOJE) == 0
    dados = json.loads(base.read_text(encoding="utf-8"))
    assert list(dados["violacoes"]) == ["src/b.py: E1"]


def test_excecao_vigente_aceita_e_vencida_falha(tmp_path):
    base = tmp_path / ".catraca.json"
    dados = {
        "violacoes": {},
        "excecoes": [
            {
                "violacao": "src/c.py: F401 sys",
                "motivo": "ADR-0012",
                "prazo": "2027-03-31",
            }
        ],
    }
    base.write_text(json.dumps(dados), encoding="utf-8")
    arq = escrever(tmp_path, "a.txt", ["src/c.py:3:1: F401 sys"])
    assert catraca.verificar(arq, base, HOJE) == 0
    depois = datetime.date(2027, 4, 1)
    assert catraca.verificar(arq, base, depois) == 1


def test_excecao_sem_motivo_falha(tmp_path):
    base = tmp_path / ".catraca.json"
    dados = {
        "violacoes": {},
        "excecoes": [
            {"violacao": "x", "motivo": " ", "prazo": "2030-01-01"}
        ],
    }
    base.write_text(json.dumps(dados), encoding="utf-8")
    arq = escrever(tmp_path, "a.txt", [])
    assert catraca.verificar(arq, base, HOJE) == 1
