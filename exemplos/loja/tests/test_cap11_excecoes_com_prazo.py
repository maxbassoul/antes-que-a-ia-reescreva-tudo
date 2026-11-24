"""Exceções à regra de tamanho, com motivo e prazo."""

import datetime  # datas, para conferir os prazos
import pathlib  # caminhos de arquivos e pastas

# Pasta src/ do projeto, um nível acima de tests/
RAIZ = pathlib.Path(__file__).parent.parent / "src"
LIMITE = 400  # máximo de linhas por arquivo
EXCECOES = {
    # arquivo: (motivo registrado, prazo da exceção)
    "loja/legado/relatorios.py": (
        "ADR-0012: divisão adiada até a migração",
        datetime.date(2027, 3, 31),
    ),
}


# Teste 1: nenhuma exceção pode estar vencida
def test_excecoes_tem_prazo_valido():
    hoje = datetime.date.today()
    # Junta as exceções cujo prazo já passou
    vencidas = [
        f"{arq} (venceu em {prazo})"
        for arq, (_, prazo) in EXCECOES.items()
        if prazo < hoje
    ]
    assert (
        not vencidas
    ), "renove com novo motivo ou corrija: " + ", ".join(
        vencidas
    )


# Teste 2: fora das exceções, ninguém passa do limite
def test_limite_respeitado_fora_das_excecoes():
    # Arquivos .py com mais linhas que o limite e que
    # não estão na lista de exceções
    grandes = [
        arq.relative_to(RAIZ).as_posix()
        for arq in RAIZ.rglob("*.py")
        if len(
            arq.read_text(encoding="utf-8").splitlines()
        )
        > LIMITE
        and arq.relative_to(RAIZ).as_posix()
        not in EXCECOES
    ]
    assert (
        not grandes
    ), f"acima de {LIMITE} linhas: {grandes}"
