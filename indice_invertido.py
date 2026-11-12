import re

def construir_indice(texto): 
# Recebe um texto com várias linhas. 
# Retorna um dicionário: palavra -> conjunto de linhas. 
    dicionario = {}
    linhas = texto.splitlines()
    for numero, linha in enumerate(linhas, start = 1):
        palavras = normalizar_palavras(linha)
        
        for palavra in palavras:
            if palavra not in dicionario:
                dicionario[palavra] = set()
            dicionario[palavra].add(numero)

    return dicionario

def buscar(indice, palavra): 
# Retorna uma lista ordenada com as linhas da palavra. 
    # Normaliza a consulta com a mesma regra usada na construção do índice.
    termos = normalizar_palavras(palavra)

    # A busca simples aceita exatamente uma palavra.
    if len(termos) != 1:
        return []

    palavra = termos[0]

    if palavra not in indice:
        resultado = []
    else:
        resultado = sorted(indice[palavra])

    return resultado

def buscar_e(indice, palavras):
# Retorna as linhas que contêm TODAS as palavras. 
    if not palavras:
        return []

    indices_palavras = []
    for palavra in palavras:
        indices_palavras.append(buscar(indice, palavra))

    resultado = set(indices_palavras[0])
    for lista in indices_palavras[1:]:
        resultado = resultado & set(lista)

    return sorted(resultado)

def buscar_ou(indice, palavras): 
# Retorna as linhas que contêm PELO MENOS UMA das palavras. 
    if not palavras:
        return []
    
    indices_palavras = []
    for palavra in palavras:
        indices_palavras.append(buscar(indice, palavra))

    resultado = set(indices_palavras[0])
    for lista in indices_palavras[1:]:
        resultado = resultado | set(lista)

    return sorted(resultado)



def normalizar_palavras(linha):
    # Palavra = sequência de letras (com ou sem acento) e/ou dígitos.
    # Qualquer outro caractere (pontuação, aspas, parênteses, hífen, barra...)
    # funciona como separador. Ex.: "guarda-chuva" -> ["guarda", "chuva"].
    # [^\W_] = caracteres de palavra (\w) exceto o underline.
    return re.findall(r"[^\W_]+", linha.lower())
