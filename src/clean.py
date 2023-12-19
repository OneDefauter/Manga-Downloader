import os

def setup(caminho_da_pasta):
    try:
        # Obtém a lista de arquivos na pasta
        arquivos = os.listdir(caminho_da_pasta)

        # Itera sobre cada arquivo na pasta e o exclui
        for arquivo in arquivos:
            caminho_completo = os.path.join(caminho_da_pasta, arquivo)
            if os.path.isfile(caminho_completo):
                os.remove(caminho_completo)
                print(f"Arquivo removido: {caminho_completo}")

        # print("Todos os arquivos foram removidos da pasta.")

    except Exception as e:
        print(f"Erro ao apagar arquivos: {e}")