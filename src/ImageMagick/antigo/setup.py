from tkinter import messagebox

from src.ImageMagick.antigo.verify import verify
from src.ImageMagick.antigo.download import download
from src.ImageMagick.antigo.get_installed_version import get_installed_version
from src.ImageMagick.antigo.compare_versions import compare_versions

# URL do instalador do ImageMagick
url = 'https://github.com/OneDefauter/Menu_/releases/download/Req/ImageMagick-7.1.1-26-Q16-HDRI-x64-dll.exe'

# Versão
required_version = '7.1.1-26'

def setup():
    if not verify():
        messagebox.showinfo("Instalação do ImageMagick", "ImageMagick não está instalado.\nBaixando e instalando o ImageMagick...")
        download(url)
    
    installed_version = get_installed_version()
    
    if installed_version:
        print(f"Versão instalada do ImageMagick: {installed_version}")

        if not compare_versions(installed_version, required_version):
            print("A versão instalada está desatualizada. Baixando e instalando nova versão do ImageMagick...")
            download(url)
