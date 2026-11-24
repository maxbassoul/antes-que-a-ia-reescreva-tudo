"""Função de aptidão: módulos dentro do limite."""

# pathlib lida com caminhos de arquivos e pastas
import pathlib

# Pasta src/ do projeto, um nível acima da pasta tests/
RAIZ = pathlib.Path(__file__).parent.parent / "src"
# Máximo de linhas por arquivo: decisão do time,
# revista a cada trimestre
LIMITE = 400
# Arquivos grandes já conhecidos e aceitos por ora
EXCECOES = {"loja/legado/relatorios.py"}


# O pytest roda toda função cujo nome começa com test_
def test_modulos_cabem_numa_leitura():
    grandes = []  # aqui vão os arquivos acima do limite
    # Percorre todos os arquivos .py, em qualquer subpasta
    for arq in RAIZ.rglob("*.py"):
        nome = arq.relative_to(RAIZ).as_posix()
        # Conta as linhas do arquivo
        linhas = len(
            arq.read_text(encoding="utf-8").splitlines()
        )
        if linhas > LIMITE and nome not in EXCECOES:
            grandes.append(f"{nome} ({linhas} linhas)")
    # Se a lista não estiver vazia, o teste falha e
    # a mensagem diz quais arquivos passaram do limite
    assert (
        not grandes
    ), "módulos acima do limite: " + ", ".join(grandes)
