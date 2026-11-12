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
    pontuacoes = str.maketrans('','', '.,!?;:-...—')

    palavra = palavra.translate(pontuacoes)
    palavra = palavra.lower().strip()
    
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
    pontuacoes = str.maketrans('','', '.,!?;:-...—')

    linha = linha.translate(pontuacoes)
    vetor = linha.lower().split()

    return vetor