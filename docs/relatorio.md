# Relatório — Índice invertido para busca textual

Mini-projeto de Estruturas de Dados — Bacharelado em Sistemas de Informação (IFAL Campus Maceió).

## 1. Ambiente

| Item | Valor |
|---|---|
| Processador | Intel64 Family 6 Model 154 (Intel Core de 12ª geração, Alder Lake) |
| Sistema operacional | Windows 11 |
| Versão do Python | 3.15.2 |

As medições foram feitas no computador de uso diário, com outros programas abertos ao mesmo tempo (VS Code, navegador, Teams).

## 2. Decisões de implementação

- **Estrutura do índice:** um dicionário (`dict`) em que cada chave é uma palavra e cada valor é um conjunto (`set`) com os números das linhas em que ela aparece.
- **Normalização:** feita pela função `normalizar_palavras`, usada tanto na construção do índice quanto nas consultas e na varredura. Assim as três partes seguem sempre a mesma regra.
  - O texto é convertido para minúsculas.
  - Uma palavra é uma sequência de letras (com ou sem acento) e/ou dígitos, extraída com a expressão regular `[^\W_]+`.
  - Pontuação, aspas, parênteses, hífen e barra funcionam como separadores. Por exemplo, `guarda-chuva` vira `guarda` e `chuva`.
  - Os acentos são preservados: `é` e `e` são palavras diferentes.
- **Numeração das linhas:** começa em 1, e as linhas vazias também contam.
- **Consultas:**
  - A palavra pesquisada passa pela mesma normalização, então `Python,` encontra `python`.
  - As buscas sempre retornam uma lista ordenada, e uma palavra inexistente retorna `[]`.
  - `buscar_e` e `buscar_ou` aceitam duas ou mais palavras; uma lista vazia retorna `[]`.
  - Nenhuma consulta altera o índice. As operações de conjunto criam conjuntos novos (`&` e `|`) em vez de modificar os conjuntos guardados.

## 3. Metodologia dos experimentos

- **Texto:** *O Cortiço*, de Aluísio Azevedo ([Project Gutenberg #69187](https://www.gutenberg.org/ebooks/69187), domínio público).
  - O cabeçalho e o rodapé de licença do Gutenberg são removidos antes das medições.
  - Resultado: 10.366 linhas, 11.439 palavras distintas e 79.042 pares (palavra, linha) no índice.
- **Consultas:** 1.000 buscas simples, as mesmas para as duas estratégias.
  - Foram sorteadas do vocabulário do texto com semente fixa (`random.Random(42)`), para o experimento ser reproduzível.
  - 10% das consultas são palavras inexistentes.
  - No Experimento 2 são usadas as primeiras 1, 10, 100 e 1.000 consultas dessa lista.
- **Medição:**
  - Os tempos foram medidos com `time.perf_counter()`.
  - Cada medição foi executada 3 vezes e foi registrada a mediana (`statistics.median`).
  - A leitura do arquivo, a montagem das consultas e o `print` ficam fora do trecho medido.
- **Conferência:** antes de medir, o script verifica que a varredura e o índice retornam o mesmo resultado para as consultas.

## 4. Experimento 1 — Tempo de busca

| Medição | Tempo (ms) |
|---|---:|
| Construção do índice | 35,146 |
| 1.000 buscas por varredura | 48.116,309 |
| 1.000 buscas com índice | 3,071 |

## 5. Experimento 2 — Vantagem da indexação

| Qtde de consultas | Varredura completa (ms) | Construção do índice + consultas (ms) |
|---:|---:|---:|
| 1 | 57,177 | 82,208 |
| 10 | 480,205 | 77,456 |
| 100 | 4.516,614 | 32,640 |
| 1.000 | 22.397,641 | 80,996 |

## 6. Respostas às questões

**1. Qual estratégia foi mais rápida? Em quais situações?**

O índice invertido foi muito mais rápido em quase todos os cenários. Com o índice pronto, 1.000 buscas levaram cerca de 3 ms, contra cerca de 48.000 ms da varredura, uma diferença de aproximadamente 15.000 vezes.

A varredura só venceu quando foi feita **uma única consulta** (57,2 ms contra 82,2 ms). Nesse caso, construir o índice custa mais do que percorrer o texto uma vez, porque a construção também percorre o texto inteiro e ainda monta o dicionário e os conjuntos.

**2. A partir de aproximadamente quantas consultas a indexação passou a ser vantajosa?**

Entre as quantidades testadas, a partir de **10 consultas**: 77,5 ms com índice contra 480,2 ms com varredura.

Como uma varredura custa entre 22 e 57 ms e a construção do índice entre 33 e 82 ms nesta máquina, o ponto de virada real fica em torno de **2 consultas** (por exemplo, 82 ÷ 57 ≈ 1,4 e 35 ÷ 22 ≈ 1,6). Depois disso, cada nova consulta com índice custa quase nada (cerca de 0,003 ms), enquanto cada varredura soma dezenas de milissegundos.

**3. Qual é a vantagem de utilizar conjuntos em vez de listas para armazenar as linhas?**

- **Sem duplicatas automaticamente.** Se uma palavra aparece várias vezes na mesma linha, `add` não repete o número da linha. Com lista, seria preciso testar `if linha not in lista`, que custa O(k).
- **Pertinência em O(1) no caso médio**, porque o `set` também é uma tabela hash. Na lista, verificar se um elemento está presente é O(k).
- **Interseção e união prontas e eficientes** (`&` e `|`). Elas são justamente as operações das consultas E e OU. Com listas, seria preciso comparar elementos com laços aninhados (O(k·m)) ou ordenar antes.

**4. Qual é a complexidade esperada da busca de uma chave em um dicionário Python?**

**O(1) no caso médio.** O dicionário é uma tabela hash: o Python calcula o hash da palavra e vai direto à posição correspondente, sem percorrer as outras chaves.

No pior caso, quando muitas chaves colidem, a busca pode chegar a O(n), mas isso é raro graças à boa função de hash e ao redimensionamento automático da tabela.

O `buscar` completo também ordena o resultado, então custa O(1 + k log k), em que k é o número de linhas da palavra. É por isso que 1.000 buscas levaram só cerca de 3 ms.

**5. Qual é a complexidade da construção do índice e das operações de união e interseção?**

- **Construção:** O(N) no caso médio, em que N é o número total de palavras do texto (ou de caracteres, considerando a normalização). Cada palavra é normalizada uma vez e inserida no dicionário e no conjunto em O(1) médio.
- **Interseção** (`A & B`): O(min(|A|, |B|)) no caso médio. O Python percorre o conjunto menor e testa cada elemento no maior.
- **União** (`A | B`): O(|A| + |B|), porque todos os elementos dos dois conjuntos são copiados para o resultado.
- **Ordenação do resultado:** como as buscas retornam listas ordenadas, ainda há um custo de O(k log k), em que k é o tamanho do resultado.

**6. Qual é a principal desvantagem da indexação em relação ao consumo de memória?**

O índice precisa ficar inteiro na memória e ocupa bem mais espaço que o próprio texto. Cada palavra distinta vira uma chave com sua própria string, e cada par (palavra, linha) vira um elemento de conjunto. Além disso, as tabelas hash do `dict` e de cada `set` reservam espaço extra vazio para manter as operações em O(1).

Numa medição aproximada com `sys.getsizeof`, o texto de *O Cortiço* tem cerca de 470 KB e o índice ocupa cerca de 7 MB, ou seja, aproximadamente **15 vezes mais memória**. Esse é o preço da troca: gasta-se memória e um custo inicial de construção para ganhar velocidade nas consultas.

## 7. Análise e conclusão

Os experimentos confirmam a teoria:

- **A varredura cresce linearmente** com o número de consultas: de 57,2 ms (1 consulta) para 480,2 ms (10), 4.516,6 ms (100) e 22.397,6 ms (1.000). O tempo cresce aproximadamente na mesma proporção do número de consultas (de 1 para 100 consultas subiu cerca de 80 vezes; de 100 para 1.000, cerca de 5 vezes, por causa da variação discutida abaixo), porque cada consulta percorre e normaliza o texto inteiro, custando O(N).
- **O índice tem custo quase fixo:** a coluna "construção + consultas" ficou entre 33 e 82 ms em todas as quantidades, sem crescer com o número de consultas. Quase todo o tempo é da construção, feita uma única vez; as consultas, em O(1) médio cada, são desprezíveis em comparação.

Por isso, o índice invertido compensa sempre que o mesmo texto recebe mais de duas consultas. Esse é o caso típico de mecanismos de busca, em que um documento é indexado uma vez e consultado muitas vezes. A varredura só faz sentido para uma consulta isolada, ou quando a memória é muito limitada, já que não guarda nenhuma estrutura extra.

**Variação das medições.** Os tempos variaram bastante entre execuções. Por exemplo, 1.000 varreduras levaram 48.116 ms no Experimento 1 e 22.398 ms no Experimento 2, com as mesmas consultas. A causa provável é o ambiente: o Windows ajusta a frequência do processador (modo de energia e aquecimento) e havia outros programas abertos disputando a CPU. Usar a mediana de 3 execuções reduz, mas não elimina, esse efeito. Mesmo assim, a diferença entre as estratégias, de milhares de vezes, é muito maior que essa variação, então a conclusão não muda.

Outra limitação dos experimentos é que eles usam apenas buscas simples. Consultas E e OU somariam o custo das operações de conjunto, mas manteriam a mesma conclusão, porque a varredura continuaria percorrendo o texto inteiro a cada consulta.
