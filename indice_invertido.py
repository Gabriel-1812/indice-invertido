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
    pass 

def buscar_e(indice, palavras): 
# Retorna as linhas que contêm TODAS as palavras. 
    pass 

def buscar_ou(indice, palavras): 
# Retorna as linhas que contêm PELO MENOS UMA das palavras. 
    pass 

def normalizar_palavras(linha):
    pontuacoes = str.maketrans('','', '.,!?;:-...—')
    linha = linha.translate(pontuacoes)
    vetor = linha.lower().split()
    return vetor

# text = "Python, Programação! e AÇÃO."
# print(normalizar_palavras(text))

texto = ( 
"Python e dados PYThon\n" 
"\n"
"Dados e algoritmos\n" 
"Python e algoritmos" 
) 
# texto = (" oi")
indice = construir_indice(texto)
print(indice)
print(indice["python"]) 
print(indice["dados"]) 
print(indice["algoritmos"]) 


 