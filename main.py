import src.check as mdi
mdi.setup()

import os
import requests

temp_folder = os.environ['TEMP']
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")

# Configuração de pastas
folder = ['setup', 'src', 'themes', 'urls']
url_folder = [
    'argos_comics',
    'argos_hentai',
    'br_mangas',
    'crystal_scan',
    'flower_manga',
    'ler_manga_online',
    'ler_mangá',
    'manga_br',
    'mangás_chan',
    'projeto_scanlator',
    'slimeread',
    'tsuki',
    'yomumangás',
]




# Cria as pastas necessárias
os.makedirs(app_folder, exist_ok=True)

for x in folder:
    x = os.path.join(app_folder, x)
    os.makedirs(x, exist_ok=True)

for x in url_folder:
    x = os.path.join(app_folder, 'urls', x)
    os.makedirs(x, exist_ok=True)



# Importações da pasta 'src'
import src.imagemagick_check as imc

# Importação da pasta 'Setup'
import setup.main as setup_main

# Verifica se o ImageMagick está instalado
imc.setup()

# Inicia a GUI
setup_main.setup()