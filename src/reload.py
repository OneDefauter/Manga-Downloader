import os
import tempfile
import platform
import subprocess

temp_folder = tempfile.gettempdir()
path = os.path.join(temp_folder, "Mangá Downloader (APP)", "main.py")

def setup():
    print('Reiniciando...')
    sistema_operacional = platform.system()
    if sistema_operacional == 'Windows':
        subprocess.Popen(['python', path])
    else:
        subprocess.Popen(['python3', path])
