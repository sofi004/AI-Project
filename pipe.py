import sys

def main():
    # Verifica se um arquivo foi fornecido como argumento na linha de comando
    if len(sys.argv) != 2:
        print("Usage: python pipe.py <filename>")
        return

    filename = sys.argv[1]  # Obtém o nome do arquivo a partir do argumento de linha de comando

    # Abre o arquivo fornecido e o lê
    try:
        with open(filename, 'r') as file:
            content = file.read()
            print("Conteúdo do arquivo:")
            print(content)
    except FileNotFoundError:
        print(f"Arquivo '{filename}' não encontrado.")

main()