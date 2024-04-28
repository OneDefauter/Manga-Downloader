import re
import subprocess

def get_installed_version():
    # Comando para obter a versão instalada do ImageMagick
    command = 'magick --version'

    try:
        # Executar o comando e capturar a saída
        output = subprocess.check_output(command, shell=True, text=True)

        # Extrair a parte relevante da saída usando expressões regulares
        version_match = re.search(r'Version: ImageMagick (\S+)', output)
        if version_match:
            installed_version_str = version_match.group(1)
            return installed_version_str
        else:
            return None
        
    except subprocess.CalledProcessError:
        # Se o comando falhar, assumimos que o ImageMagick não está instalado
        return None

