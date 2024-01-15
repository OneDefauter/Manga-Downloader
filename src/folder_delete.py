import os

def delete_empty_folders(base_folder):
    if os.path.exists(base_folder):
        for folder_name in os.listdir(base_folder):
            folder_path = os.path.join(base_folder, folder_name)

            # Verificar se é um diretório
            if os.path.isdir(folder_path):
                # Verificar se o diretório está vazio
                if not os.listdir(folder_path):
                    print(f'Deletando pasta vazia: {folder_path}')
                    os.rmdir(folder_path)