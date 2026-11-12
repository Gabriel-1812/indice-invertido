"""
EXPERIMENTOS 
índice invertido x busca por varredura.

Uso (na pasta do projeto):
    python experimentos.py          # usa o texto original (x1)
    python experimentos.py 5        # usa o texto repetido 5 vezes

Texto base: "O Cortiço", de Aluísio Azevedo (Project Gutenberg, eBook #69187),
salvo em dados/o_cortico.txt.

Regras seguidas (enunciado):
- mesmo texto e mesmas consultas nas duas estratégias;
- cada medição repetida REPETICOES vezes, registrando a mediana;
- leitura de arquivo, montagem das consultas e print ficam FORA da medição.
"""

import os
import platform
import random
import statistics
import sys
import time

from indice_invertido import construir_indice, buscar
from varredura import varrer

PASTA = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(PASTA, "dados", "o_cortico.txt")
SAIDA = os.path.join(PASTA, "docs", "resultados_experimentos.md")

REPETICOES = 3            # mínimo exigido pelo enunciado
TOTAL_CONSULTAS = 1000
PROPORCAO_INEXISTENTES = 0.1   # 10% das consultas são palavras que não existem
SEMENTE = 42                   # garante que as consultas sejam sempre as mesmas
QUANTIDADES_EXP2 = [1, 10, 100, 1000]


# ---------------------------------------------------------------
# Preparação (nada aqui é cronometrado)
# ---------------------------------------------------------------

def carregar_texto(caminho):
    """Lê o arquivo e remove o cabeçalho e o rodapé de licença do Gutenberg."""
    with open(caminho, "r", encoding="utf-8-sig") as arquivo:
        texto = arquivo.read()

    linhas = texto.splitlines()
    inicio, fim = 0, len(linhas)
    for i, linha in enumerate(linhas):
        if linha.startswith("*** START OF"):
            inicio = i + 1
        elif linha.startswith("*** END OF"):
            fim = i
            break

    return "\n".join(linhas[inicio:fim]).strip("\n")


def gerar_consultas(indice, quantidade, semente):
    """Lista fixa de palavras: a maioria existe no texto, algumas não."""
    gerador = random.Random(semente)

    qtd_inexistentes = int(quantidade * PROPORCAO_INEXISTENTES)
    qtd_existentes = quantidade - qtd_inexistentes

    vocabulario = sorted(indice)  # ordenado para o sorteio ser reproduzível
    existentes = gerador.choices(vocabulario, k=qtd_existentes)
    inexistentes = [f"inexistente{i}" for i in range(qtd_inexistentes)]

    consultas = existentes + inexistentes
    gerador.shuffle(consultas)
    return consultas


# ---------------------------------------------------------------
# Medição
# ---------------------------------------------------------------

def medir(funcao):
    """Executa a função REPETICOES vezes e retorna a mediana em milissegundos."""
    tempos = []
    for _ in range(REPETICOES):
        inicio = time.perf_counter()
        funcao()
        fim = time.perf_counter()
        tempos.append((fim - inicio) * 1000)
    return statistics.median(tempos)


def consultas_por_varredura(texto, consultas):
    for palavra in consultas:
        varrer(texto, palavra)


def consultas_com_indice(indice, consultas):
    for palavra in consultas:
        buscar(indice, palavra)


def construcao_mais_consultas(texto, consultas):
    indice = construir_indice(texto)
    for palavra in consultas:
        buscar(indice, palavra)


# ---------------------------------------------------------------
# Programa principal
# ---------------------------------------------------------------

def formatar_ms(valor):
    return f"{valor:,.3f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    multiplicador = int(sys.argv[1]) if len(sys.argv) > 1 else 1

    if not os.path.exists(ARQUIVO):
        print(f"Arquivo não encontrado: {ARQUIVO}")
        print("Baixe 'O Cortiço' em https://www.gutenberg.org/ebooks/69187 "
              "(Plain Text UTF-8) e salve como dados/o_cortico.txt")
        return

    base = carregar_texto(ARQUIVO)
    texto = "\n".join([base] * multiplicador)

    indice = construir_indice(texto)
    consultas = gerar_consultas(indice, TOTAL_CONSULTAS, SEMENTE)

    # Conferência: as duas estratégias precisam dar o mesmo resultado.
    for palavra in consultas[:50]:
        assert varrer(texto, palavra) == buscar(indice, palavra), palavra

    qtd_linhas = len(texto.splitlines())
    qtd_palavras = sum(len(linhas) for linhas in indice.values())

    print(f"Texto: O Cortiço x{multiplicador}")
    print(f"Linhas: {qtd_linhas} | Palavras distintas: {len(indice)}")
    print(f"Consultas: {TOTAL_CONSULTAS} (semente {SEMENTE}, "
          f"{int(PROPORCAO_INEXISTENTES * 100)}% inexistentes)")
    print(f"Repetições por medição: {REPETICOES} (mediana)\n")

    # ---------------- Experimento 1 ----------------
    print("Executando Experimento 1...")
    t_construcao = medir(lambda: construir_indice(texto))
    t_varredura = medir(lambda: consultas_por_varredura(texto, consultas))
    t_indice = medir(lambda: consultas_com_indice(indice, consultas))

    # ---------------- Experimento 2 ----------------
    print("Executando Experimento 2...")
    exp2 = []
    for n in QUANTIDADES_EXP2:
        parte = consultas[:n]
        t_var = medir(lambda: consultas_por_varredura(texto, parte))
        t_idx = medir(lambda: construcao_mais_consultas(texto, parte))
        exp2.append((n, t_var, t_idx))

    ponto_virada = next((n for n, tv, ti in exp2 if ti < tv), None)

    # ---------------- Saída ----------------
    linhas_saida = [
        "# Resultados dos experimentos",
        "",
        "## Ambiente",
        f"- Sistema operacional: {platform.system()} {platform.release()}",
        f"- Processador: {platform.processor() or platform.machine()}",
        f"- Python: {platform.python_version()}",
        "",
        "## Configuração",
        f"- Texto: O Cortiço (Project Gutenberg #69187), sem cabeçalho/rodapé de licença, x{multiplicador}",
        f"- Linhas: {qtd_linhas}",
        f"- Palavras distintas: {len(indice)}",
        f"- Total de pares (palavra, linha) no índice: {qtd_palavras}",
        f"- Consultas: {TOTAL_CONSULTAS} buscas simples, sorteadas com semente {SEMENTE}; "
        f"{int(PROPORCAO_INEXISTENTES * 100)}% são palavras inexistentes",
        f"- Cada medição executada {REPETICOES} vezes; registrada a mediana",
        "- Fora da medição: leitura do arquivo, montagem das consultas e print",
        "",
        "## Experimento 1 — Tempo de busca",
        "",
        "| Medição | Tempo (ms) |",
        "|---|---:|",
        f"| Construção do índice | {formatar_ms(t_construcao)} |",
        f"| {TOTAL_CONSULTAS} buscas por varredura | {formatar_ms(t_varredura)} |",
        f"| {TOTAL_CONSULTAS} buscas com índice | {formatar_ms(t_indice)} |",
        "",
        "## Experimento 2 — Vantagem da indexação",
        "",
        "| Qtde de consultas | Varredura completa (ms) | Construção + consultas (ms) |",
        "|---:|---:|---:|",
    ]
    for n, tv, ti in exp2:
        linhas_saida.append(f"| {n} | {formatar_ms(tv)} | {formatar_ms(ti)} |")

    linhas_saida.append("")
    if ponto_virada:
        linhas_saida.append(
            f"Ponto de virada: a indexação passou a compensar a partir de {ponto_virada} "
            f"consulta(s) entre as quantidades testadas."
        )
    else:
        linhas_saida.append("Ponto de virada: a indexação não compensou nas quantidades testadas.")

    relatorio = "\n".join(linhas_saida) + "\n"
    print()
    print(relatorio)

    with open(SAIDA, "w", encoding="utf-8") as arquivo:
        arquivo.write(relatorio)
    print(f"Resultados salvos em {SAIDA}")


if __name__ == "__main__":
    main()
