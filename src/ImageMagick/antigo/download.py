import os
import sys
import requests
import subprocess
from tkinter import messagebox

def download(url):
    temp_folder = os.environ['TEMP']
    installer_path = os.path.join(temp_folder, 'ImageMagick-Installer.exe')

    response = requests.get(url)
    with open(installer_path, 'wb') as f:
        f.write(response.content)

    # Instalar o ImageMagick usando subprocess
    subprocess.run([installer_path, '/VERYSILENT', '/SUPPRESSMSGBOXES'])
        
    os.remove(installer_path)
    messagebox.showinfo("Instalação concluída", "ImageMagick instalado com sucesso.")
    
    sys.exit()