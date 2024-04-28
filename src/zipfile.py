import os
import zipfile

def setup(download_folder):
    arquivos = os.listdir(download_folder)
    for arquivo in arquivos:
        if arquivo.endswith('.zip'):
            zip_file_path = os.path.join(download_folder, arquivo)
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(download_folder)
            os.remove(zip_file_path)
    
    arquivos = os.listdir(download_folder)
    for arquivo in arquivos:
        file_path = os.path.join(download_folder, arquivo)
        if not (arquivo.lower().endswith('.png') or arquivo.lower().endswith('.jpg')):
            os.remove(file_path)
