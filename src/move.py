import os
import shutil

def setup(origem, destino):
    try:
        # Certifica-se de que o diretório de destino existe, se não, cria-o
        if not os.path.exists(destino):
            os.makedirs(destino)

        # Obtém a lista de arquivos na pasta de origem
        arquivos = os.listdir(origem)

        # Itera sobre cada arquivo na pasta de origem
        for arquivo in arquivos:
            caminho_origem = os.path.join(origem, arquivo)

            # Verifica se o arquivo é uma imagem (pode ser ajustado para outros tipos de arquivo)
            if os.path.isfile(caminho_origem) and arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                caminho_destino = os.path.join(destino, arquivo)

                # Move o arquivo para a pasta de destino
                shutil.move(caminho_origem, caminho_destino)
                # print(f"Imagem movida para: {caminho_destino}")

        # print("Todas as imagens foram movidas para a nova pasta.")

    except Exception as e:
        print(f"Erro ao mover imagens: {e}")
