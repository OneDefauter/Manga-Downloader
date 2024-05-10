import subprocess

def install_imagemagick():
    try:
        subprocess.run(["sudo", "apt-get", "update"], check=True)
        subprocess.run(["sudo", "apt-get", "install", "-y", "imagemagick"], check=True)
        print("ImageMagick instalado com sucesso.")
        return True
    except subprocess.CalledProcessError:
        print("Falha ao instalar o ImageMagick.")
        return False