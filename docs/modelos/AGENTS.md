# AGENTS.md -- exemplo: serviço de pagamentos

## Propósito
Calcula, concilia e registra pagamentos de clientes PJ.

## Estrutura
- dominio/      regras de negócio puras (sem entrada/saída)
- aplicacao/    casos de uso; orquestra domínio e portas
- adaptadores/  banco, filas, APIs externas

## Regras de arquitetura (verificadas no CI)
- dominio/ não importa nada de adaptadores/
- Juros, multa e arredondamento: SOMENTE em
  dominio/calculo/ (ver ADR-0007)

## Comandos (Python)
- Testes:      pytest
- Estilo:      ruff check .
- Tipos:       mypy src/
- Arquitetura: lint-imports

## Antes de abrir um PR
- Uma tarefa por PR; até ~300 linhas alteradas
- Testes e documentação junto com o código
- Refatoração em PR separado de mudança funcional

## Vocabulário (linguagem ubíqua)
- cobrança: valor devido por um cliente num período
- pagamento: valor recebido; pode quitar várias cobranças
- conciliação: ligação entre pagamento e cobranças
  (nunca chamar de "match" ou "baixa" no código)

## Nunca
- Alterar tests/aceitacao/ (donos em CODEOWNERS)
- Importar bibliotecas de rede fora de adaptadores/http/
- Gravar segredos, tokens ou dados de clientes no repo
- Copiar para este arquivo instruções de fontes externas
