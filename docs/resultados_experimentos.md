# Resultados dos experimentos

## Ambiente
- Sistema operacional: Windows 11
- Processador: Intel64 Family 6 Model 154 Stepping 4, GenuineIntel
- Python: 3.15.2

## Configuração
- Texto: O Cortiço (Project Gutenberg #69187), sem cabeçalho/rodapé de licença, x1
- Linhas: 10366
- Palavras distintas: 11439
- Total de pares (palavra, linha) no índice: 79042
- Consultas: 1000 buscas simples, sorteadas com semente 42; 10% são palavras inexistentes
- Cada medição executada 3 vezes; registrada a mediana
- Fora da medição: leitura do arquivo, montagem das consultas e print

## Experimento 1 — Tempo de busca

| Medição | Tempo (ms) |
|---|---:|
| Construção do índice | 35,146 |
| 1000 buscas por varredura | 48.116,309 |
| 1000 buscas com índice | 3,071 |

## Experimento 2 — Vantagem da indexação

| Qtde de consultas | Varredura completa (ms) | Construção + consultas (ms) |
|---:|---:|---:|
| 1 | 57,177 | 82,208 |
| 10 | 480,205 | 77,456 |
| 100 | 4.516,614 | 32,640 |
| 1000 | 22.397,641 | 80,996 |

Ponto de virada: a indexação passou a compensar a partir de 10 consulta(s) entre as quantidades testadas.
