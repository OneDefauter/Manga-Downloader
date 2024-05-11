import sys
import platform
from tkinter import messagebox

from src.ImageMagick.novo.is_winget_installed import is_winget_installed
from src.ImageMagick.novo.is_imagemagick_installed import is_imagemagick_installed
from src.ImageMagick.novo.install_imagemagick_with_winget import install_imagemagick_with_winget

from src.ImageMagick.novo.Unix.check import is_imagemagick_installed as Unix
from src.ImageMagick.novo.Unix.install import install_imagemagick

def setup():
    sistema_operacional = platform.system()
    if sistema_operacional != 'Windows':
        if not Unix():
            install_imagemagick()
            sys.exit()
        else:
            return True
    
    if not is_winget_installed():
        return False

    if not is_imagemagick_installed():
        messagebox.showinfo("Instalação do ImageMagick", "ImageMagick não está instalado.\nInstalando o ImageMagick...")
        if not install_imagemagick_with_winget():
            messagebox.showinfo("Instalação do ImageMagick", "Falha ao instalar o ImageMagick.")
            return False
        else:
            messagebox.showinfo("Instalação do ImageMagick", "ImageMagick instalado com sucesso.")
            sys.exit()
    else:
        from src.ImageMagick.antigo.get_installed_version import get_installed_version
        versão = get_installed_version()
        if versão:
            print(f"Versão instalada do ImageMagick: {versão}")
            
    return True