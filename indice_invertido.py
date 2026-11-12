def construir_indice(texto): 
# Recebe um texto com várias linhas. 
# Retorna um dicionário: palavra -> conjunto de linhas. 
    pass 

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

text = "Python, Programação! e AÇÃO."
print(normalizar_palavras(text))

