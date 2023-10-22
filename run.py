import os
import subprocess
import requests
import tempfile
import sys

# Verificar se os módulos estão instalados
required_modules = ['requests', 'pywin32', 'selenium', 'aiohttp']

for module in required_modules:
    try:
        __import__('win32api') if module == 'pywin32' else __import__(module)
    except ImportError:
        print(f"Módulo {module} não encontrado. Instalando...")
        subprocess.run(['pip', 'install', module])

# URL do arquivo main.py no repositório GitHub
main_py_url = 'https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/main.py'

# Nome do arquivo de destino
main_py_filename = 'main.py'

# Obter o diretório temporário do sistema
temp_dir = tempfile.gettempdir()

# Caminho completo para o arquivo main.py na pasta temporária
main_py_path = os.path.join(temp_dir, main_py_filename)

# Baixar o arquivo main.py
response = requests.get(main_py_url)
with open(main_py_path, 'wb') as f:
    f.write(response.content)

# print(f"{main_py_filename} foi baixado com sucesso em {temp_dir}.")

# Obtendo argumentos do script run.py
run_args = sys.argv[1:]

# Construindo a lista completa de argumentos para main.py
main_args = ['python', main_py_path] + run_args

# Abrir o arquivo main.py com argumentos
subprocess.run(main_args)