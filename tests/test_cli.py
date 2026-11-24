"""Testes do comando único, inclusive scripts do livro."""

import pathlib
import subprocess

from contencao import cli

EXEMPLO = (
    pathlib.Path(__file__).parent.parent / "exemplos" / "loja"
)


def git(pasta, *args):
    subprocess.run(
        ["git", *args], cwd=pasta, check=True, capture_output=True
    )


def repositorio(tmp_path):
    """Repositório git mínimo com um teste de aceitação."""
    git(tmp_path, "init", "-q", "-b", "main")
    git(tmp_path, "config", "user.email", "a@b.c")
    git(tmp_path, "config", "user.name", "Teste")
    pasta = tmp_path / "tests" / "aceitacao"
    pasta.mkdir(parents=True)
    (pasta / "test_ac.py").write_text("def test_a():\n    pass\n")
    git(tmp_path, "add", ".")
    git(tmp_path, "commit", "-q", "-m", "base")
    git(tmp_path, "branch", "base")
    return tmp_path


def test_ajuda_lista_subcomandos(capsys):
    assert cli.main([]) == 0
    saida = capsys.readouterr().out
    for nome in [*cli.SCRIPTS, *cli.NOVAS]:
        assert nome in saida


def test_subcomando_desconhecido():
    assert cli.main(["nao-existe"]) == 2


def test_scripts_do_livro_existem():
    for arquivo, *_ in cli.SCRIPTS.values():
        assert (cli.LIVRO / arquivo).is_file()


def test_mapa_do_exemplo_esta_atualizado(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert cli.main(["mapa", str(EXEMPLO / "src" / "loja")]) == 0
    gerado = (tmp_path / "MAPA.md").read_text(encoding="utf-8")
    versionado = (EXEMPLO / "MAPA.md").read_text(encoding="utf-8")
    assert gerado == versionado


def test_check_testes_pega_teste_movido(tmp_path, monkeypatch):
    repo = repositorio(tmp_path)
    git(repo, "checkout", "-q", "-b", "mudanca")
    (repo / "tests" / "outros").mkdir()
    git(
        repo,
        "mv",
        "tests/aceitacao/test_ac.py",
        "tests/outros/test_ac.py",
    )
    git(repo, "commit", "-q", "-m", "move")
    monkeypatch.chdir(repo)
    assert cli.main(["check-testes", "base"]) == 1


def test_check_testes_passa_sem_mudanca_protegida(
    tmp_path, monkeypatch
):
    repo = repositorio(tmp_path)
    git(repo, "checkout", "-q", "-b", "mudanca")
    (repo / "README.md").write_text("oi\n")
    git(repo, "add", ".")
    git(repo, "commit", "-q", "-m", "doc")
    monkeypatch.chdir(repo)
    assert cli.main(["check-testes", "base"]) == 0
