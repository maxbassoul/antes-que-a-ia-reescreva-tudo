# Fluxogramas de decisão

Versões em Mermaid das figuras do livro. O GitHub desenha os
diagramas direto na página. A ordem das perguntas é do autor; os
critérios vêm dos capítulos indicados.

## Delegar ou manter com pessoas (Cap. 12)

```mermaid
flowchart TD
  I[Tarefa candidata] --> Q1{Decisão arquitetural, efeito externo<br/>ou área de autoria humana?}
  Q1 -- sim --> A1[Manter com pessoas;<br/>o agente pode preparar rascunho]
  Q1 -- não --> Q2{Já existe teste que diz<br/>quando está pronta?}
  Q2 -- não --> A2[Escrever o teste primeiro] --> Q2
  Q2 -- sim --> Q3{Cabe numa fronteira e<br/>tem uma intenção só?}
  Q3 -- não --> A3[Dividir em tarefas menores] --> Q3
  Q3 -- sim --> Q4{Se der errado,<br/>o erro custa caro?}
  Q4 -- sim --> A4[Delegar com revisão do plano]
  Q4 -- não --> F[Delegar]
```

## Duplicação proposital ou deriva (Caps. 6 e 13)

```mermaid
flowchart TD
  I[Lógica repetida em dois lugares] --> Q1{Cópias em lados diferentes<br/>de uma fronteira declarada?}
  Q1 -- não: deriva --> C1
  Q1 -- sim --> Q2{Cada lado evolui sozinho, ou<br/>as cópias devem mudar juntas?}
  Q2 -- evoluir sozinho --> A2[Duplicação proposital:<br/>registrar a decisão]
  Q2 -- mudar juntas: deriva --> C1[1. Teste roda as cópias<br/>com as mesmas entradas]
  C1 --> Q3{As cópias concordam?}
  Q3 -- não --> A3[Divergência é pergunta<br/>de negócio: o time decide] --> C2
  Q3 -- sim --> C2[2. Módulo único com contrato explícito]
  C2 --> C3[3. Verificação que impede a volta das cópias]
  C3 --> C4[Trocar as chamadas, uma por PR,<br/>e apagar as cópias]
```

## Quando a verificação barra um PR (Cap. 11)

```mermaid
flowchart TD
  I[A verificação falhou no PR] --> Q1{O código viola a regra<br/>como ela foi pensada?}
  Q1 -- não --> A1[Falso positivo: reescrever<br/>a regra com mais precisão]
  Q1 -- sim --> Q2{Neste caso, obedecer custa<br/>mais do que desobedecer?}
  Q2 -- sim --> A2[Exceção ao lado da regra,<br/>com motivo e prazo]
  A2 --> V[Prazo vencido: a verificação<br/>falha e o time decide de novo]
  Q2 -- não --> F[Corrigir o código]
```

## Roteiro de resgate (Cap. 13)

```mermaid
flowchart TD
  A0[Escolher uma única área pelo histórico] --> Q1{Há testes que fixam<br/>o comportamento atual?}
  Q1 -- não --> A1[Testes de caracterização;<br/>código novo por Sprout ou Wrap Method] --> Q2
  Q1 -- sim --> Q2{O sistema pode continuar<br/>funcionando enquanto muda?}
  Q2 -- não --> A2[Reescrever, só depois de mudar o processo<br/>e revisar o que o antigo fazia bem]
  Q2 -- sim --> B1[Fachada isola a parte degradada]
  B1 --> B2[Parte nova cresce ao lado,<br/>atrás da mesma fachada]
  B2 --> B3[Antigo removido no prazo<br/>do registro de decisão]
```

## Arquivo de instruções e código discordam (Cap. 9)

```mermaid
flowchart TD
  I[O agente aponta uma inconsistência] --> Q1{Qual lado mostra o<br/>padrão que o time quer?}
  Q1 -- o código --> A1[Corrigir o arquivo de instruções,<br/>com teste ao lado da regra]
  Q1 -- o arquivo --> B1[Mudar regra e verificação no mesmo PR;<br/>código antigo vira pendência]
  B1 --> B2[Varredura de migração pelo agente,<br/>em PRs pequenos e separados]
  B2 --> B3[Lista zerada: a exceção sai da verificação]
```
