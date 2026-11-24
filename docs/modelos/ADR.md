# ADR-0007: Cálculo financeiro em um único módulo

Status: aceita            Data: 2026-11-18
Proposta por: agente (sessão de 17/11), revisada por
  Ana (arquitetura) e Paulo (financeiro)
Substitui: nenhuma        Substituída por: -
Contexto:
  Encontramos quatro implementações de juros de mora,
  com arredondamentos diferentes.
Decisão:
  Todo cálculo de juros, multa e arredondamento fica em
  dominio/calculo/. Outros módulos chamam essa API.
Consequências:
  + Uma fonte de verdade; testes concentrados.
  - Migrar as três cópias existentes (cerca de 2 sprints).
Verificação:
  Regra de dependência no CI (make arch-check).
