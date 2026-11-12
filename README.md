# Índice invertido para busca textual

Mini-projeto da disciplina de Estruturas de Dados (Bacharelado em Sistemas de Informação, IFAL Campus Maceió).

O programa lê um texto com várias linhas, constrói um **índice invertido** (dicionário `palavra -> conjunto de linhas`) e responde consultas simples, **E** (interseção) e **OU** (união) sem percorrer o texto a cada busca.

## Requisitos

- Python 3.10 ou superior
- Nenhuma biblioteca externa

## Estrutura

| Arquivo | Conteúdo |
|---|---|
| `indice_invertido.py` | Funções obrigatórias: `construir_indice`, `buscar`, `buscar_e`, `buscar_ou` |
| `main.py` | Programa interativo de consultas |
| `testes.py` | Testes do enunciado e casos de borda |
| `varredura.py` | Busca por varredura completa (sem índice) |
| `experimentos.py` | Medição de desempenho das duas estratégias |
| `dados/` | Textos usados nas consultas e nos experimentos |
| `docs/relatorio.md` | Tabelas, respostas às questões e análise |
| `docs/diario_de_bordo.md` | Registro do uso de IA |

## Como executar

Na pasta do projeto:

```bash
# Rodar os testes
python testes.py

# Programa interativo de consultas (lê dados/teste.txt)
python main.py
```

### Formato das consultas

| Tipo | Exemplo |
|---|---|
| Simples | `python` |
| E (todas as palavras) | `python E dados` ou `python E dados E algoritmos` |
| OU (pelo menos uma) | `python OU dados` |

- Os operadores `E` e `OU` não diferenciam maiúsculas e minúsculas e não podem ser misturados na mesma consulta.
- Digite `0` para sair.
- Limitação: em consultas combinadas, a palavra `e` é interpretada como operador.

## Regras de normalização

- Maiúsculas e minúsculas são equivalentes.
- Palavra = sequência de letras (com ou sem acento) e/ou dígitos; pontuação, aspas, parênteses, hífen e barra funcionam como separadores (`guarda-chuva` vira `guarda` e `chuva`).
- Acentos são preservados (`é` e `e` são palavras diferentes).
- Linhas vazias contam na numeração, que começa em 1.
