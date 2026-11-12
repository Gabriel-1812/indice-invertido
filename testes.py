from indice_invertido import * 

texto = ( 
"Python e dados\n" 
"Dados e algoritmos\n" 
"Python e algoritmos" 
) 

indice = construir_indice(texto) 

# Teste 1: construção do índice 
assert indice["python"] == {1, 3} 
assert indice["dados"] == {1, 2} 
assert indice["algoritmos"] == {2, 3} 

# Teste 2: busca simples 
assert buscar(indice, "python") == [1, 3] 
assert buscar(indice, "java") == [] 

# Teste 3: consultas combinadas 
assert buscar_e(indice, ["python", "dados"]) == [1] 
assert buscar_ou(indice, ["python", "dados"]) == [1, 2, 3]


# ---------------------------------------------------------------
# Testes próprios (casos de borda citados no enunciado)
# ---------------------------------------------------------------
import copy

# Texto vazio
assert construir_indice("") == {}

# Linhas vazias contam na numeração
assert construir_indice("a\n\nb") == {"a": {1}, "b": {3}}

# Maiúsculas e minúsculas equivalentes
assert construir_indice("Python PYTHON python") == {"python": {1}}

# Palavra repetida na mesma linha não duplica a linha
assert construir_indice("dados dados\ndados")["dados"] == {1, 2}

# Pontuação não faz parte das palavras
idx = construir_indice('(dados) "dados" [dados] «dados» dados. dados, dados! —dados')
assert idx == {"dados": {1}}

# Hífen e barra separam palavras (decisão registrada no relatório)
idx = construir_indice("guarda-chuva python/java")
assert set(idx) == {"guarda", "chuva", "python", "java"}

# Acentos preservados: palavras com e sem acento são diferentes
idx = construir_indice("é e É\nprogramação programacao")
assert idx["é"] == {1}
assert idx["e"] == {1}
assert idx["programação"] == {2}
assert idx["programacao"] == {2}

# Consulta também é normalizada
assert buscar(indice, "Python") == [1, 3]
assert buscar(indice, "PYTHON,") == [1, 3]

# Consultas inválidas ou vazias na busca simples
assert buscar(indice, "") == []
assert buscar(indice, "python dados") == []

# Palavra inexistente em E e OU
assert buscar_e(indice, ["python", "java"]) == []
assert buscar_ou(indice, ["java", "rust"]) == []
assert buscar_ou(indice, ["java", "dados"]) == [1, 2]

# Três ou mais palavras
assert buscar_e(indice, ["python", "e", "dados"]) == [1]
assert buscar_ou(indice, ["python", "dados", "algoritmos"]) == [1, 2, 3]

# Lista vazia
assert buscar_e(indice, []) == []
assert buscar_ou(indice, []) == []

# Retorno é lista (não conjunto)
assert isinstance(buscar(indice, "python"), list)
assert isinstance(buscar_e(indice, ["python", "dados"]), list)
assert isinstance(buscar_ou(indice, ["python", "dados"]), list)

# Consultas não modificam o índice
antes = copy.deepcopy(indice)
buscar(indice, "python")
buscar_e(indice, ["python", "dados", "algoritmos"])
buscar_ou(indice, ["python", "dados", "java"])
assert indice == antes

print("Todos os testes passaram.")
