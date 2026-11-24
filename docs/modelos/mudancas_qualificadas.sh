# 1) Integrações (merges) feitas entre 6 e 2 semanas
#    atrás, uma por linha
git log --merges --since=6.weeks --until=2.weeks --oneline
# 2) Reversões das últimas 6 semanas: o git revert
#    começa a mensagem com a palavra "Revert"
git log --since=6.weeks --grep=Revert --oneline
