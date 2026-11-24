# Cartões operacionais

Versão de consulta do Apêndice F. Copie para o repositório do time ou
para o modelo de descrição de pull request. A seleção e a ordem dos
itens são do autor; as fontes estão no capítulo indicado.

## Cartão 1: antes de delegar uma tarefa

**A tarefa pode ir para o agente?** (Cap. 12)

- [ ] Ela é pequena e autocontida, a ponto de caber numa fronteira?
- [ ] Já existe critério de teste, de preferência um teste que reproduz o problema?
- [ ] Se ela der errado, alguma barreira pega o erro antes que ele importe? (Isberg, 2026, p. 267)
- [ ] Ela fica fora das áreas em que a autoria final é de pessoas: decisões arquiteturais, efeitos externos (mensagens, publicação, dados de produção), criptografia, saída regulada, sistemas físicos, fronteira de segurança, chaves e segredos e migração de dados de produção? (Isberg, 2026, p. 268-269)

**O plano do agente passa nas três perguntas?** Peça o plano antes
do código.

- [ ] **Localização:** o plano aponta os arquivos e as funções certos?
- [ ] **Escopo:** mexe só no que a tarefa pede, sem "melhorar" o vizinho?
- [ ] **Critério de teste:** diz como saberemos que funcionou?

## Cartão 2: revisão de um pull request de agente

**Antes de chegar a uma pessoa** (Cap. 12)

- [ ] Estilo e regras foram cobrados pelas verificações automáticas? (no estudo de Watanabe e colegas, 23,4% das revisões em PRs de agente tratavam de estilo)
- [ ] O PR tem uma intenção só: uma correção, uma funcionalidade ou uma limpeza?
- [ ] A arrumação veio separada da mudança de comportamento? (Beck, 2023; Horikawa e colegas encontraram 36,6% das refatorações de agentes escondidas em commits que não as mencionavam)

**O que só a pessoa julga**

- [ ] A intenção da mudança é a certa?
- [ ] A mudança respeita a arquitetura e as fronteiras?
- [ ] Ela abre algum risco de segurança?

**Os testes que vieram junto** (Cap. 10)

- [ ] O que cada teste afirma? Uma asserção como `assert resultado is not None` passa com quase qualquer código.
- [ ] Estragando o código de propósito (trocar um sinal, apagar uma linha), o teste falha? O teste frouxo que passa com a solução errada é o erro mais grave (Shinn et al., 2023).
- [ ] Algum teste de aceitação protegido foi alterado? Se foi, o dono aprovou?

**Devolva o PR** quando ele misturar arrumação e comportamento ou for
grande demais para uma revisão; peça a divisão em PRs menores.

## Cartão 3: política de uso de agentes em uma página

Uma linha por pergunta (Cap. 14). Este cartão é referência de
engenharia e não substitui a orientação jurídica sobre a legislação
que alcança a empresa.

1. **Objetivo:** para que usamos agentes, e que medida dirá se funcionou?
2. **Formação:** quem é treinado, e em quê?
3. **Dados:** o que não pode entrar no contexto de um agente? No mínimo, segredos, dados pessoais e código de terceiros sob licença restritiva.
4. **Análise a mais:** que verificação o código gerado recebe? O livro propõe análise de segurança obrigatória no pipeline.
5. **Permissões:** que conteúdo o agente lê e com que permissões age? Tudo o que vem de fora é tratado como não confiável.
6. **Declaração:** o uso é marcado nos commits, para que se saiba depois de onde veio cada mudança?

Acrescente quem pode alterar os arquivos de instrução e como essas
alterações são revisadas (Cap. 9).

## Cartão 4: formação de engenheiros juniores

A ordem é a do Capítulo 14; a duração de cada etapa fica a critério
do time.

1. **Diagnóstico:** o júnior lê, depura e explica código antes de pedir que um agente o escreva. Osmani (2025) sugere praticar sem a IA, como num dia inteiro sem assistente, e depurar sozinho os erros do código gerado antes de pedir a correção ao modelo.
2. **Revisão:** revisa PRs de agente com um colega experiente ao lado, usando o Cartão 2.
3. **Delegação:** começa a delegar, primeiro revisando planos com o Cartão 1, depois com tarefas cada vez maiores.
