# Índice invertido para busca textual

Mini-projeto da disciplina de Estruturas de Dados (Bacharelado em Sistemas de Informação, IFAL Campus Maceió).

O programa lê um texto com várias linhas, constrói um **índice invertido** (dicionário `palavra -> conjunto de linhas`) e responde consultas simples, **E** (interseção) e **OU** (união) sem percorrer o texto a cada busca. O projeto também compara o desempenho do índice com uma busca por varredura completa.

## Requisitos

- Python 3.10 ou superior (testado com Python 3.15 no Windows 11)
- Nenhuma biblioteca externa

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `indice_invertido.py` | Funções obrigatórias: `construir_indice`, `buscar`, `buscar_e`, `buscar_ou` |
| `main.py` | Programa interativo de consultas |
| `testes.py` | Testes do enunciado e casos de borda |
| `varredura.py` | Busca por varredura completa (sem índice) + teste de equivalência |
| `experimentos.py` | Medição de desempenho das duas estratégias |
| `dados/teste.txt` | Texto pequeno usado pelo programa de consultas |
| `dados/o_cortico.txt` | Texto base dos experimentos |
| `docs/relatorio.md` | Relatório: tabelas, respostas às questões e análise |
| `docs/resultados_experimentos.md` | Saída gerada pelo `experimentos.py` |
| `docs/diario_de_bordo.md` | Registro do uso de IA |
| `docs/planejamento-indice-invertido.md` | Planejamento das fases do projeto |
| `docs/comando-mini-projeto-hash.pdf` | Enunciado do mini-projeto |

## Como executar

Todos os comandos devem ser executados na pasta do projeto.

### 1. Testes

```bash
python testes.py       # deve exibir "Todos os testes passaram."
python varredura.py    # deve exibir "Equivalência OK..."
```

### 2. Programa de consultas

```bash
python main.py
```

O programa lê `dados/teste.txt`, constrói o índice e aguarda consultas:

| Tipo | Exemplo | Resultado |
|---|---|---|
| Simples | `python` | linhas que contêm a palavra |
| E | `python E dados` | linhas que contêm **todas** as palavras |
| OU | `python OU dados` | linhas que contêm **pelo menos uma** das palavras |

- Aceita duas ou mais palavras: `python E dados E algoritmos`.
- Os operadores `E` e `OU` não diferenciam maiúsculas e minúsculas e não podem ser misturados na mesma consulta.
- Digite `0` para sair.
- Limitação: em consultas combinadas, a palavra `e` é interpretada como operador.

### 3. Experimentos

```bash
python experimentos.py      # texto original (leva cerca de 2 minutos)
python experimentos.py 5    # opcional: texto repetido 5 vezes
```

O resultado é impresso no terminal e salvo em `docs/resultados_experimentos.md`.

## Regras de normalização

- Maiúsculas e minúsculas são equivalentes.
- Palavra = sequência de letras (com ou sem acento) e/ou dígitos; pontuação, aspas, parênteses, hífen e barra funcionam como separadores (`guarda-chuva` vira `guarda` e `chuva`).
- Acentos são preservados (`é` e `e` são palavras diferentes).
- Linhas vazias contam na numeração, que começa em 1.
- As consultas passam pela mesma normalização (`Python,` encontra `python`).

## Experimentos

- **Texto:** *O Cortiço*, de Aluísio Azevedo ([Project Gutenberg #69187](https://www.gutenberg.org/ebooks/69187), domínio público), com 10.366 linhas e 11.439 palavras distintas. O cabeçalho e o rodapé de licença do Gutenberg são removidos pelo script.
- **Consultas:** 1.000 buscas simples sorteadas com semente fixa (42); 10% são palavras inexistentes.
- **Medição:** cada medição é repetida 3 vezes e a mediana é registrada; leitura de arquivo e `print` ficam fora do tempo medido.

### Principais resultados

| Medição | Tempo (ms) |
|---|---:|
| Construção do índice | 35,1 |
| 1.000 buscas por varredura | 48.116,3 |
| 1.000 buscas com índice | 3,1 |

- O índice foi cerca de **15.000 vezes mais rápido** nas consultas.
- A varredura só vence quando é feita **uma única consulta**; a indexação compensa a partir de cerca de 2 consultas.
- Em troca, o índice ocupa cerca de 15 vezes mais memória que o texto.

A análise completa e as respostas às questões estão em [`docs/relatorio.md`](docs/relatorio.md).

## Uso de inteligência artificial

O uso de IA ao longo do projeto está registrado em [`docs/diario_de_bordo.md`](docs/diario_de_bordo.md).
