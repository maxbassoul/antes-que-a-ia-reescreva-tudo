"""Custo por mudança entregue, por módulo."""

import collections  # contadores e dicionários prontos
import csv  # lê planilhas salvas em CSV
import sys  # argumentos da linha de comando

# Uso: python custo.py mudancas.csv PRECO_TOKENS
#      PRECO_CI CUSTO_HORA
# Valores do seu contrato e da sua folha; não há padrão.
# moeda por mil tokens
PRECO_MIL_TOKENS = float(sys.argv[2])
# moeda por minuto de pipeline
PRECO_MINUTO_CI = float(sys.argv[3])
# custo de uma hora de pessoa
CUSTO_HORA = float(sys.argv[4])

custo = collections.defaultdict(float)  # soma por módulo
entregues = collections.Counter()  # mudanças em produção
# Cada linha do CSV é uma mudança, com o módulo, os
# tokens, os minutos de pipeline e as horas de pessoas
with open(sys.argv[1], encoding="utf-8") as f:
    for m in csv.DictReader(f):
        # custo = tokens + pipeline + horas de pessoas
        custo[m["modulo"]] += (
            int(m["tokens"]) / 1000 * PRECO_MIL_TOKENS
            + int(m["minutos_ci"]) * PRECO_MINUTO_CI
            + (
                float(m["horas_revisao"])
                + float(m["horas_retrabalho"])
            )
            * CUSTO_HORA
        )
        # conta 1 se a mudança chegou à produção
        entregues[m["modulo"]] += (
            m["chegou_a_producao"] == "sim"
        )

# Ordena do módulo mais caro por mudança ao mais barato
for modulo in sorted(
    custo, key=lambda k: -custo[k] / max(entregues[k], 1)
):
    n = entregues[modulo]
    # sem nenhuma entrega, o custo por mudança é infinito
    por_mudanca = custo[modulo] / n if n else float("inf")
    print(
        f"{modulo:12s} {n:3d} entregues  "
        f"custo por mudança: {por_mudanca:10.2f}"
    )
