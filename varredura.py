from indice_invertido import normalizar_palavras

def _normalizar_termo(palavra):
    # Aplica à consulta a mesma regra usada no índice.
    # Retorna None se a consulta não tiver exatamente uma palavra
    termos = normalizar_palavras(palavra)
    if len(termos) != 1:
        return None
    return termos[0]

def varrer(texto, palavra):
    # Busca simples: percorre todas as linhas a cada chamada.
    termo = _normalizar_termo(palavra)
    if termo is None:
        return []

    resultado = []
    for numero, linha in enumerate(texto.splitlines(), start=1):
        if termo in normalizar_palavras(linha):
            resultado.append(numero)

    return resultado

def varrer_e(texto, palavras):
    # Linhas que contêm TODAS as palavras.
    if not palavras:
        return []

    termos = [_normalizar_termo(p) for p in palavras]
    if None in termos:
        return []

    resultado = []
    for numero, linha in enumerate(texto.splitlines(), start=1):
        palavras_linha = set(normalizar_palavras(linha))
        if all(termo in palavras_linha for termo in termos):
            resultado.append(numero)

    return resultado

def varrer_ou(texto, palavras):
    # Linhas que contêm PELO MENOS UMA das palavras.
    termos = [_normalizar_termo(p) for p in palavras]
    termos = [t for t in termos if t is not None]
    if not termos:
        return []

    resultado = []
    for numero, linha in enumerate(texto.splitlines(), start=1):
        palavras_linha = set(normalizar_palavras(linha))
        if any(termo in palavras_linha for termo in termos):
            resultado.append(numero)

    return resultado

if __name__ == "__main__":
    # Teste de equivalência: varredura e índice devem dar o mesmo resultado.
    from indice_invertido import construir_indice, buscar, buscar_e, buscar_ou

    texto = (
        "Python é uma linguagem de programação\n"
        "Estruturas de dados são fundamentais\n"
        "\n"
        "Python possui diversas estruturas de dados.\n"
        "Algoritmos utilizam boas estruturas!\n"
        "Programação em (Python) é interessante"
    )
    indice = construir_indice(texto)

    simples = ["python", "Estruturas", "programação", "java", "", "dados,"]
    combinadas = [
        ["python", "estruturas"],
        ["python", "dados", "estruturas"],
        ["java", "python"],
        ["programação", "é"],
        [],
    ]

    for p in simples:
        assert varrer(texto, p) == buscar(indice, p), p

    for ps in combinadas:
        assert varrer_e(texto, ps) == buscar_e(indice, ps), ps
        assert varrer_ou(texto, ps) == buscar_ou(indice, ps), ps

    print("Equivalência OK: varredura e índice retornam os mesmos resultados.")