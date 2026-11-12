# Planejamento — Mini-projeto: Índice invertido para busca textual

**Disciplina:** Estruturas de Dados — Bacharelado em Sistemas de Informação (IFAL / Campus Maceió)
**Aluno:** Gabriel Frederico de Araujo
**Repositório:** https://github.com/Gabriel-1812/indice-invertido

---

## 1. Visão geral

Construir um programa em Python que lê um texto com várias linhas, monta um **dicionário palavra → conjunto de linhas** (o índice invertido) e responde consultas simples, **E** (interseção) e **OU** (união) — e depois **provar com medições** que isso é mais rápido do que varrer o texto a cada consulta.

### Como a nota é distribuída (e onde investir energia)

| Critério | Pontos | O que isso significa na prática |
|---|---|---|
| Construção correta do índice | 35 | As 6 regras de normalização (seção 4) precisam estar 100% certas. É aqui que os **testes reservados** do professor vão pegar. |
| Consultas simples, E e OU | 35 | Retornar **listas ordenadas**, sem modificar o índice, tratando palavras inexistentes. |
| Experimentos e análise | 20 | Tabelas com medições honestas + respostas às 6 perguntas. |
| GitHub, organização, diário | 10 | Commits que contam a história, README claro, diário de bordo. |

---

## 2. Estrutura do repositório

```
indice-invertido/
├── README.md                 # O que é o projeto + como executar
├── indice_invertido.py       # As 4 funções obrigatórias (+ funções auxiliares)
├── main.py                   # Programa interativo para fazer consultas
├── varredura.py              # Estratégia 2: busca sem índice (percorre o texto)
├── experimentos.py           # Mede tempos e gera os números das tabelas
├── testes.py                 # Testes do enunciado + seus próprios testes
├── dados/
│   └── dom_casmurro.txt      # Texto base dos experimentos
├── docs/
│   ├── relatorio.md          # Tabelas, respostas às questões e análise
│   └── diario_de_bordo.md    # Registro do uso de IA
└── .gitignore
```

### 2.1 Para que serve cada entregável

**`indice_invertido.py` — o coração do projeto**
- Contém as funções `construir_indice(texto)`, `buscar(indice, palavra)`, `buscar_e(indice, palavras)` e `buscar_ou(indice, palavras)`.
- Manter **nomes e parâmetros idênticos**, **nada de `input()` nem `print()`** dentro dessas funções.
- Funções auxiliares, ex.: uma função que normaliza/separa as palavras de uma linha. Isso facilita testar e reaproveitar na varredura.

**`main.py` — o "programa para executar as consultas"**
- É a interface com o usuário: lê um arquivo de texto, constrói o índice e deixa a pessoa digitar consultas (ex.: `python`, `python E dados`, `python OU dados`).
- Aqui sim pode ter `input()` e `print()`.
- Precisa ter `if __name__ == "__main__":` para não executar nada quando for importado.

**`varredura.py` — a estratégia de comparação**
- Busca sequencial linha por linha **a cada consulta**, sem índice.
- **Mesma regra** do índice. Se as duas estratégias tratam pontuação/maiúsculas de forma diferente, a comparação de tempo é injusta e os resultados podem divergir.
- Dica de verificação: para as mesmas consultas, varredura e índice devem retornar **o mesmo resultado**. Use isso como teste.

**`experimentos.py` — gera os números**
- Monta o texto grande, define a lista fixa de consultas, mede com `time.perf_counter()` e calcula a mediana de pelo menos 3 execuções.
- Não mede leitura de arquivo nem `print`.

**`testes.py` — sua rede de segurança**
- Os `assert`s do enunciado + os seus, cobrindo os casos que os testes reservados vão cobrir (seção 4).
- Rodar com `python testes.py` ou com pytest se tiver instalado.

**`README.md` — a porta de entrada**
- Explica o projeto em 2–3 linhas, versão do Python, como rodar `main.py`, `testes.py` e `experimentos.py`, e onde estão o relatório e o diário.
- Teste: uma pessoa que nunca viu o projeto consegue rodar tudo só lendo o README?

**`docs/relatorio.md` — o relatório breve**
- Tabelas dos dois experimentos, respostas às 6 questões, análise dos resultados e configuração da máquina usada. Modelo na seção 7.

**`docs/diario_de_bordo.md` — registro do uso de IA**
- Exigência do professor: registrar consultas relevantes à IA, o que foi orientado e **como você verificou**. Modelo na seção 6.
- Não é para ser longo; é para ser honesto e mostrar que você usou IA para aprender, não para copiar.

**Histórico de commits**
- O professor quer ver a **evolução real**. Um único commit "projeto pronto" é sinal de alerta. Detalhes na seção 5.

---

## 3. Fases de desenvolvimento (com marcas de parada)

Cada fase termina num ponto onde você pode parar, fazer commit e voltar outro dia sem se perder. Estimativas são de tempo focado.

### Fase 0 — Preparação (≈ 30 min)
- [x] Criar o repositório no GitHub e clonar localmente.
- [x] Criar a estrutura de pastas, `README.md` esqueleto, `.gitignore` (ignorar `__pycache__/`, `.venv/` e os arquivos de texto gigantes gerados nos experimentos).
- [x] Criar `docs/diario_de_bordo.md` já com o modelo — e registrar esta primeira conversa.
- [x] Copiar os testes do enunciado para `testes.py` (vão falhar, é normal).

**Pronto quando:** o repo existe, tem estrutura e o primeiro commit.
⏸️ **Marca de parada 0**

### Fase 1 — Normalização das palavras (≈ 1h)
- [x] Escrever uma função auxiliar que recebe **uma linha** e devolve as palavras já tratadas.
- Tratamento feito retornando palavras separadas em minúsculo, mantendo acentos e removendo pontuações (. , ! ? ; : - ... —)
- [x] Testar essa função isoladamente com frases cheias de pontuação, maiúsculas e acentos.

**Pronto quando:** `"Python, Programação! e AÇÃO."` vira as palavras esperadas, com acento preservado.
⏸️ **Marca de parada 1**

### Fase 2 — `construir_indice` (≈ 1h)
- [x] Percorrer as linhas com numeração começando em 1.
- [x] Usar a função da Fase 1 e montar o dicionário palavra → conjunto.
- [x] Testes 1 do enunciado passando.
- [x] Testes próprios: texto vazio, linhas vazias no meio, palavra repetida na mesma linha, mesma palavra com maiúscula/minúscula.
- Função retorna um dicionário: {'palavra1' : {1,5}, 'palavra2': {5,0}}. palavra com as linhas que ela aparece.

**Pronto quando:** todos os testes de construção passam.
⏸️ **Marca de parada 2**

### Fase 3 — Consultas `buscar`, `buscar_e`, `buscar_ou` (≈ 1h30)
- [x] `buscar`: palavra inexistente → `[]`; retorno sempre **lista ordenada**.
- [x] `buscar_e` com interseção e `buscar_ou` com união, aceitando 2 ou mais palavras.
- [x] Decidir e documentar: a palavra **pesquisada** também é normalizada? (o usuário digita `Python` — deve achar `python`?)
- [x] Decidir e documentar: o que acontece com lista de palavras vazia? E com uma palavra inexistente no meio de um E?
- [x] **Teste de não-modificação do índice:** guarde uma cópia do índice antes das consultas e compare depois. ⚠️ Existem operações de conjunto que alteram o próprio conjunto — se você aplicar uma delas direto no conjunto que está dentro do índice, quebra a regra sem perceber.

**Pronto quando:** testes 2 e 3 do enunciado + seus testes de borda passam, e o índice sai intacto.
⏸️ **Marca de parada 3** — aqui você já garantiu a base dos 70 pontos.

### Fase 4 — Programa de consultas `main.py` (≈ 1h)
- [x] Ler um arquivo (caminho padrão ou informado), construir o índice uma vez.
- [x] Loop de consultas: interpretar `palavra`, `a E b E c`, `a OU b`; comando para sair.
- [x] Mensagens amigáveis para consulta vazia ou formato inválido.
- [x] Atualizar o README com "como executar".

**Pronto quando:** dá para demonstrar o exemplo do enunciado (as 5 linhas sobre Python) ao vivo.
⏸️ **Marca de parada 4**

### Fase 5 — Busca por varredura `varredura.py` (≈ 1h)
- [x] Implementar busca simples, E e OU percorrendo o texto a cada chamada.
- [x] Reaproveitar a mesma normalização.
- [x] Teste de equivalência: para várias consultas, varredura e índice retornam exatamente o mesmo resultado.

**Pronto quando:** o teste de equivalência passa.
⏸️ **Marca de parada 5**

### Fase 6 — Experimentos (≈ 2h)
- [x] Baixar *Dom Casmurro* (Project Gutenberg, domínio público) para `dados/`. Decidir se remove o cabeçalho/rodapé de licença do Gutenberg e anotar.
- [x] Gerar versões maiores concatenando o texto (ex.: ×1, ×10, ×50) **por script**, sem commitar os arquivos gigantes.
- [x] Montar uma lista fixa de consultas (palavras que existem e que não existem; misture simples/E/OU ou fixe um tipo — e documente). Use `random.seed(...)` se sortear, para ser reproduzível.
- [x] Experimento 1: construção do índice, 1.000 buscas por varredura, 1.000 buscas com índice.
- [x] Experimento 2: 1, 10, 100, 1.000 consultas — varredura vs (construção + consultas).
- [x] Cada medição ao menos 3 vezes, registrar a **mediana** (`statistics.median`).
- [x] Garantir que leitura do arquivo e `print` estão **fora** do trecho cronometrado.
- [x] Salvar a saída (ex.: imprimir tabela em Markdown pronta para colar no relatório).

**Pronto quando:** você tem as duas tabelas preenchidas e consegue apontar o "ponto de virada" do Experimento 2.
⏸️ **Marca de parada 6**

### Fase 7 — Relatório (≈ 1h30)
- [x] Preencher `docs/relatorio.md` seguindo o modelo da seção 7.
- [x] Responder as 6 questões **com suas palavras** e ligando aos seus números.
- [x] Revisar README e diário.

⏸️ **Marca de parada 7**

### Fase 8 — Revisão final e preparação para a avaliação individual (≈ 1h)
- [x] Rodar tudo do zero num terminal novo seguindo apenas o README.
- [x] Conferir o checklist da seção 8.
- [x] **Treinar a defesa:** explicar em voz alta cada função, linha por linha, e por que usou dict e set.
- [x] **Treinar modificações sem IA** (o professor vai pedir uma pequena mudança). Exemplos para praticar sozinho:
  - adicionar uma consulta `NÃO` (linhas que não contêm a palavra);
  - contar quantas vezes a palavra aparece em cada linha;
  - ignorar uma lista de palavras irrelevantes ("de", "e", "a");
  - mudar a regra de acento (passar a tratar "programacao" e "programação" como iguais).

**Total estimado:** ≈ 10–11h de trabalho focado. Distribua em blocos curtos; a Marca 3 é a prioridade absoluta.

---

## 4. Armadilhas — o que os testes reservados vão cobrar

O enunciado avisa: textos vazios, palavras repetidas, pontuação, maiúsculas/minúsculas e palavras inexistentes. Transforme cada regra em pelo menos um teste seu:

| Regra do enunciado | Pergunta que seu teste deve responder |
|---|---|
| Linhas começam em 1 | A primeira linha aparece como `1`, não `0`? |
| Maiúsculas = minúsculas | `"Python"` e `"PYTHON"` caem na mesma chave? |
| Pontuação fora | `"dados."`, `"dados,"` e `"(dados)"` viram `"dados"`? |
| Sem linha repetida | Palavra 3× na mesma linha → linha aparece uma vez? |
| Acentos preservados | `"é"` e `"e"` são chaves **diferentes**? Cuidado com funções que removem acento sem você perceber. |
| Linhas vazias contam | Em `"a\n\nb"`, `b` está na linha 3? |
| Texto vazio | `construir_indice("")` não quebra e retorna `{}`? |
| Palavra inexistente | `buscar` retorna `[]`, não erro nem `None`? |
| Retorno ordenado | O retorno é `list`, não `set`, e está em ordem crescente? |
| Índice intacto | Depois de várias consultas, o índice é igual ao de antes? |

> Lembrete do enunciado: passar nos testes fornecidos não garante que está correto.

---

## 5. Commits — como mostrar a "evolução real"

**Regra prática:** um commit por passo que funciona. Cada marca de parada = pelo menos um commit.

**Padrão de mensagem** (simples e consistente, em português):
```
tipo: descrição curta no imperativo
```
Tipos: `feat` (funcionalidade), `test` (testes), `fix` (correção), `docs` (README/relatório/diário), `chore` (estrutura, gitignore).

**Exemplo de histórico saudável:**
```
chore: cria estrutura inicial do projeto
docs: adiciona modelo do diário de bordo
test: adiciona testes do enunciado
feat: implementa normalização de palavras
test: cobre pontuação, maiúsculas e acentos
feat: implementa construir_indice
fix: considera linhas vazias na numeração
feat: implementa buscar, buscar_e e buscar_ou
test: garante que consultas não modificam o índice
feat: cria programa interativo de consultas
feat: implementa busca por varredura
test: verifica equivalência entre varredura e índice
feat: adiciona script de experimentos
docs: registra resultados no relatório
docs: finaliza README com instruções de execução
```

**Evite:** commits gigantes com tudo junto, mensagens como "update" / "aaa" / "agora vai", e subir arquivos de texto enormes.

Os commits `fix:` são **bons** para a nota: mostram que você testou, achou erro e corrigiu.

---

## 6. Diário de bordo — modelo

Arquivo: `docs/diario_de_bordo.md`. Registre só as consultas relevantes (não toda conversa).

```markdown
# Diário de bordo — Uso de IA

Ferramenta usada: Claude (Anthropic)
Regra seguida: IA usada para estudar conceitos, entender erros e sugerir testes.
Nenhuma solução completa foi copiada.

## Registro

### 2026-11-12 — Planejamento do projeto
- **O que perguntei:** como organizar o projeto e o que cada entregável deveria conter.
- **O que a IA orientou:** estrutura do repositório, fases com marcas de parada,
  lista de casos de borda para testar, padrão de commits.
- **O que eu fiz com isso:** criei o repositório e a estrutura de pastas; adaptei
  a lista de casos de borda para meus testes.
- **Como verifiquei:** conferi cada item contra o enunciado do professor.

### AAAA-MM-DD — <assunto>
- **O que perguntei:**
- **O que a IA orientou:**
- **O que eu fiz com isso:**
- **Como verifiquei:**  (ex.: escrevi um teste, rodei, li a documentação do Python)
```

Bons motivos para registrar: dúvida conceitual (ex.: complexidade de `set` em Python), erro que você não entendeu, pedido de casos de teste, revisão de código que **você** escreveu.

---

## 7. Relatório — modelo

Arquivo: `docs/relatorio.md`.

```markdown
# Relatório — Índice invertido

## 1. Ambiente
- Máquina / processador / RAM:
- Sistema operacional:
- Versão do Python:

## 2. Decisões de implementação
- Como trato pontuação, hífen, apóstrofo e números:
- A palavra pesquisada é normalizada?
- Comportamento com lista de palavras vazia:

## 3. Metodologia dos experimentos
- Texto usado e tamanho (linhas / palavras distintas / multiplicador):
- Como as consultas foram escolhidas:
- Nº de repetições e uso da mediana:
- O que ficou fora da medição (leitura de arquivo, print):

## 4. Experimento 1 — Tempo de busca
| Medição | Tempo (ms) |
|---|---|
| Construção do índice | |
| 1.000 buscas por varredura | |
| 1.000 buscas com índice | |

## 5. Experimento 2 — Vantagem da indexação
| Qtde de consultas | Varredura completa (ms) | Construção + consultas (ms) |
|---|---|---|
| 1 | | |
| 10 | | |
| 100 | | |
| 1.000 | | |

(Opcional: gráfico simples dessas duas colunas.)

## 6. Respostas às questões
1. Qual estratégia foi mais rápida? Em quais situações?
2. A partir de aproximadamente quantas consultas a indexação passou a ser vantajosa?
3. Vantagem de usar conjuntos em vez de listas:
4. Complexidade esperada da busca de uma chave em dicionário Python:
5. Complexidade da construção do índice e de união/interseção:
6. Principal desvantagem da indexação quanto à memória:

## 7. Análise e conclusão
```

**Como responder bem:** cada resposta deve juntar **teoria** (complexidade, como hash funciona) com **seus dados** ("na minha medição, com X linhas, a indexação compensou a partir de ~N consultas"). Nas questões 4 e 5, diferencie caso médio e pior caso, e diga do que depende o custo (nº de linhas, nº de palavras, tamanho dos conjuntos).

---

## 8. Checklist final antes de entregar

**Código**
- [x] `indice_invertido.py` com os 4 nomes e parâmetros exatos.
- [x] Nenhum `input()`/`print()` nas 4 funções.
- [x] Buscas retornam `list` ordenada; inexistente → `[]`.
- [x] Índice não é modificado pelas consultas.
- [x] `python testes.py` roda sem erros.

**Experimentos**
- [x] Mesmas consultas e mesmo texto nas duas estratégias.
- [x] Mediana de ≥ 3 execuções.
- [x] Leitura de arquivo e `print` fora da medição.

**Repositório**
- [x] README permite rodar tudo do zero.
- [x] Relatório com as 2 tabelas e as 6 respostas.
- [x] Diário de bordo atualizado.
- [x] Histórico com vários commits coerentes.
- [x] Sem arquivos gigantes nem `__pycache__` no repo.

**Avaliação individual**
- [x] Consigo explicar cada função sem olhar anotações.
- [x] Consigo justificar dict (tabela hash) e set (sem duplicatas, interseção/união eficientes).
- [x] Pratiquei pelo menos 2 modificações sem IA.

---

## 9. Desafios opcionais (só depois da Marca 7)

Frase exata, índice posicional, múltiplos arquivos ou ranking. Não valem pontos na tabela de avaliação — só faça se o resto estiver entregue e revisado. Uma entrega sólida vale mais que um extra pela metade.

---

## 10. Sobre o uso de IA neste projeto

O enunciado é explícito: IA pode ser usada para **estudar conceitos, esclarecer dúvidas, entender erros e sugerir testes**; **não** pode copiar soluções completas, e a avaliação individual é **sem IA** (explicar o código e modificá-lo na hora). Se houver alguma orientação do professor diferente do PDF, vale confirmar com ele e registrar no diário.

Forma recomendada de usar a IA durante o projeto: escrever o código você mesmo, e pedir revisão do que escreveu, explicação de erros e ideias de casos de teste.
