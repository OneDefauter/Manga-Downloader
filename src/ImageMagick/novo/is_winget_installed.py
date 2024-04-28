import subprocess

def is_winget_installed():
    try:
        # Tente executar o comando winget
        subprocess.run(['winget', '--version'], capture_output=True, check=True)
        return True
    except (FileNotFoundError, subprocess.CalledProcessError):
        # Se o comando falhar ou não for encontrado, o Winget não está instalado
        return False