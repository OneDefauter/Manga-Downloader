import subprocess

def is_imagemagick_installed():
    # Verifica se o ImageMagick está instalado usando o comando 'convert'
    try:
        subprocess.run(["convert", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except subprocess.CalledProcessError:
        return False
    except FileNotFoundError:
        return False  # 'convert' não encontrado, o ImageMagick provavelmente não está instalado