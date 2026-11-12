import os

from indice_invertido import *
from experimentos import carregar_texto

# Caminho relativo ao próprio arquivo: funciona de qualquer pasta.
ARQUIVO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "dados", "o_cortico.txt")

def mostrar(resultado):
    # Livro grande: mostra a quantidade de linhas e a lista.
    print(f"{len(resultado)} linha(s): {resultado}")

def main():
    # Reaproveita a leitura dos experimentos, que remove a licença do Gutenberg.
    texto = carregar_texto(ARQUIVO)

    indice = construir_indice(texto)
    print(f"O Cortiço carregado: {len(texto.splitlines())} linhas, {len(indice)} palavras distintas.")

    while True:
        consulta = input("Digite sua consulta ou (0 para sair): ").strip()

        if consulta == '0':
            print("Encerrando programa...")
            break

        elementos = consulta.split()

        if not elementos:
            print("Consulta vazia. Tente novamente.")
            continue

        if len(elementos) == 1:
            # Chama busca simples
            mostrar(buscar(indice, elementos[0]))

        elif len(elementos) >= 3 and len(elementos) % 2 != 0:

            palavras = elementos[0::2]
            operadores = [op.lower() for op in elementos[1::2]]

            if all(op == "e" for op in operadores):
                # Chama buscar_e()
                mostrar(buscar_e(indice, palavras))

            elif all(op == "ou" for op in operadores):
                # Chama buscar_ou()
                mostrar(buscar_ou(indice, palavras))

            else:
                print("Operadores inválidos. Use apenas E ou apenas OU, sem misturar.")

        else:
            print("Formato inválido. Utilize: palavra, palavra E palavra ou palavra OU palavra.")

if __name__ == "__main__":
    main()
