import os
import sys
import requests
import subprocess
from tkinter import messagebox



def verify():
    # Diretório onde procuraremos por pastas relacionadas ao ImageMagick
    program_files_path = r'C:\\Program Files'

    # Prefixo usado para identificar pastas do ImageMagick
    imagick_folder_prefix = 'ImageMagick'

    # Obtém uma lista de todas as pastas em C:\Program Files
    program_files_folders = [folder for folder in os.listdir(program_files_path)
                             if os.path.isdir(os.path.join(program_files_path, folder))]

    # Filtra as pastas que começam com o prefixo 'ImageMagick'
    imagick_folders = [folder for folder in program_files_folders if folder.startswith(imagick_folder_prefix)]

    # Verifica se cada pasta do ImageMagick contém o executável magick.exe
    for imagick_folder in imagick_folders:
        imagick_path = os.path.join(program_files_path, imagick_folder)
        magick_exe_path = os.path.join(imagick_path, 'magick.exe')
        
        # Se o executável magick.exe existir, consideramos o ImageMagick como instalado
        if os.path.isfile(magick_exe_path):
            return True

    # Se nenhum diretório do ImageMagick for encontrado, consideramos o ImageMagick não instalado
    return False



def download():
    messagebox.showinfo("Instalação do ImageMagick", "ImageMagick não está instalado.\nBaixando e instalando o ImageMagick...")
    
    # URL do instalador do ImageMagick
    url = 'https://github.com/OneDefauter/Menu_/releases/download/Req/ImageMagick-7.1.1-21-Q16-HDRI-x64-dll.exe'

    temp_folder = os.environ['TEMP']
    installer_path = os.path.join(temp_folder, 'ImageMagick-Installer.exe')

    response = requests.get(url)
    with open(installer_path, 'wb') as f:
        f.write(response.content)

    # Instalar o ImageMagick usando subprocess
    subprocess.run([installer_path, '/VERYSILENT'])
        
    os.remove(installer_path)
    messagebox.showinfo("Instalação concluída", "ImageMagick instalado com sucesso.")
    
    sys.exit()



def setup():
    if not verify():
        download()