import sys
from tkinter import messagebox

from src.ImageMagick.novo.is_winget_installed import is_winget_installed
from src.ImageMagick.novo.is_imagemagick_installed import is_imagemagick_installed
from src.ImageMagick.novo.install_imagemagick_with_winget import install_imagemagick_with_winget

def setup():
    if not is_winget_installed():
        messagebox.showinfo("Instalação do ImageMagick", "Winget não está instalado.")
        sys.exit()

    if not is_imagemagick_installed():
        messagebox.showinfo("Instalação do ImageMagick", "ImageMagick não está instalado.\nInstalando o ImageMagick...")
        if not install_imagemagick_with_winget():
            messagebox.showinfo("Instalação do ImageMagick", "Falha ao instalar o ImageMagick.")
            sys.exit()
        else:
            messagebox.showinfo("Instalação do ImageMagick", "ImageMagick instalado com sucesso.")
            sys.exit()
    else:
        from src.ImageMagick.antigo.get_installed_version import get_installed_version
        versão = get_installed_version()
        if versão:
            print(f"Versão instalada do ImageMagick: {versão}")
            
    return True