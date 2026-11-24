# Checklist de diagnóstico da deriva

Versão de consulta do Apêndice A. Marque cada item como **não** (a
prática não existe), **em parte** ou **sim**.

- [ ] Há uma linha no painel com mudanças em produção sem reversão, além da contagem de pull requests? (Caps. 1 e 4)
- [ ] Sabemos que fração dos comentários de revisão trata de estrutura e forma, e não de comportamento? (Cap. 1)
- [ ] As regras de negócio críticas têm uma única implementação? (Caps. 1 e 2)
- [ ] Existem dependências entre módulos que ninguém sabe justificar? (Cap. 2)
- [ ] Há arquivos com mais de mil linhas que cresceram nos últimos seis meses? (Caps. 2 e 3)
- [ ] O repositório tem um arquivo de instrução versionado e atualizado? (Cap. 9)
- [ ] As decisões arquiteturais importantes estão registradas, com justificativa? (Cap. 9)
- [ ] Alguma regra de arquitetura é verificada automaticamente no pipeline? (Cap. 11)
- [ ] Os pull requests feitos com agentes têm limite de tamanho e de escopo? (Cap. 12)
- [ ] O painel do time combina medidas estruturais, de fluxo e de percepção? (Cap. 4)
- [ ] Registramos, para tarefas típicas, tokens, passos e resultado do agente por módulo? (Caps. 4 e 15)
- [ ] Sabemos que pares de módulos mudam juntos com frequência? (Cap. 6)
- [ ] Cada módulo esconde uma decisão que conseguimos dizer numa frase? (Cap. 6)
- [ ] Os testes de aceitação ficam numa pasta protegida, que o agente não altera sem aprovação? (Cap. 10)
- [ ] Cada correção pedida a um agente começa por um teste que reproduz o problema? (Cap. 10)
- [ ] Sabemos quais arquivos grandes mudam com mais frequência? (Cap. 13)
- [ ] Refatorações vêm em pull requests separados das mudanças funcionais? (Caps. 12 e 13)
- [ ] Os arquivos sensíveis (instruções, contratos de arquitetura, testes) têm donos com aprovação obrigatória? (Cap. 14)
- [ ] Existe uma política de uso de agentes que diga quem pode alterar os arquivos de instrução? (Cap. 14)
