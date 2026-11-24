"""Todo teste precisa afirmar alguma coisa."""

import ast  # lê código Python como uma árvore
import pathlib  # caminhos de arquivos e pastas

# salve na raiz de tests/: rglob percorre as subpastas
TESTES = pathlib.Path(__file__).parent
# Funções comuns (def) e assíncronas (async def)
FUNCOES = (ast.FunctionDef, ast.AsyncFunctionDef)


# A função contém alguma verificação?
def afirma(func: ast.AST) -> bool:
    for no in ast.walk(func):
        if isinstance(no, ast.Assert):  # um assert
            return True
        # pytest.raises e self.assertEqual também verificam
        if isinstance(no, ast.Attribute):
            if no.attr.startswith(("raises", "assert")):
                return True
    return False


def test_todo_teste_tem_assercao():
    vazios = []  # testes que não verificam nada
    for arq in TESTES.rglob("test_*.py"):
        texto = arq.read_text(encoding="utf-8")
        for no in ast.walk(ast.parse(texto)):
            if not isinstance(no, FUNCOES):
                continue  # não é função: pula
            # só interessam as funções de teste
            if no.name.startswith("test_"):
                if not afirma(no):
                    vazios.append(f"{arq.name}::{no.name}")
    assert not vazios, f"Sem asserção: {vazios}"
