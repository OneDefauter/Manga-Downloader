import os
import requests

temp_folder = os.environ['TEMP']
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")

# Configuração de pastas
folder = ['setup', 'src', 'urls', 'engine', 'images']
url_folder = [
    'argos_comics',
    'argos_scan',
    'br_mangas',
    'crystal_scan',
    'download_methods',
    'flower_manga',
    'hentai_teca',
    'ler_manga_online',
    'ler_mangá',
    'manga_br',
    'mangás_chan',
    'projeto_scanlator',
    'slimeread',
    'tsuki',
    'yomumangás',
    'nicomanga',
    'momo_no_hana',
    'valkyrie_scan',
    'limbo_scan',
    'iris_scanlator',
    'nobre_scan'
]

context = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/urls/'
context2 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/src/'
context3 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/themes/'
context4 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/setup/'
context5 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/engine/'
context6 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/images/'

# Agregadores
urls = {
    'argos_comics': {'main': f'{context}/argos_comics/main.py', 'run':f'{context}/argos_comics/run.py', 'search':f'{context}/argos_comics/search.py'},
    'br_mangas': {'main': f'{context}/br_mangas/main.py', 'run':f'{context}/br_mangas/run.py', 'search':f'{context}/br_mangas/search.py', 'change':f'{context}/br_mangas/change.py', 'ads':f'{context}/br_mangas/ads.py'},
    'crystal_scan': {'main': f'{context}/crystal_scan/main.py', 'run':f'{context}/crystal_scan/run.py', 'search':f'{context}/crystal_scan/search.py'},
    'flower_manga': {'main': f'{context}/flower_manga/main.py', 'run':f'{context}/flower_manga/run.py', 'search':f'{context}/flower_manga/search.py'},
    'ler_mangá': {'main': f'{context}/ler_mangá/main.py', 'run':f'{context}/ler_mangá/run.py', 'search':f'{context}/ler_mangá/search.py'},
    'ler_manga_online': {'main': f'{context}/ler_manga_online/main.py', 'run':f'{context}/ler_manga_online/run.py', 'search':f'{context}/ler_manga_online/search.py'},
    'manga_br': {'main': f'{context}/manga_br/main.py', 'run':f'{context}/manga_br/run.py', 'search':f'{context}/manga_br/search.py'},
    'mangás_chan': {'main': f'{context}/mangás_chan/main.py', 'run':f'{context}/mangás_chan/run.py', 'search':f'{context}/mangás_chan/search.py'},
    'projeto_scanlator': {'main': f'{context}/projeto_scanlator/main.py', 'run':f'{context}/projeto_scanlator/run.py', 'search':f'{context}/projeto_scanlator/search.py'},
    'slimeread': {'main': f'{context}/slimeread/main.py', 'run':f'{context}/slimeread/run.py', 'search':f'{context}/slimeread/search.py', 'login':f'{context}/slimeread/login.py'},
    'tsuki': {'main': f'{context}/tsuki/main.py', 'run':f'{context}/tsuki/run.py', 'search':f'{context}/tsuki/search.py'},
    'yomumangás': {'main': f'{context}/yomumangás/main.py', 'run':f'{context}/yomumangás/run.py', 'search':f'{context}/yomumangás/search.py'},
    'hentai_teca': {'main': f'{context}/hentai_teca/main.py', 'run':f'{context}/hentai_teca/run.py', 'search':f'{context}/hentai_teca/search.py'},
    'argos_scan': {'main': f'{context}/argos_scan/main.py', 'run':f'{context}/argos_scan/run.py', 'search':f'{context}/argos_scan/search.py'},
    'download_methods': {'madara': f'{context}/download_methods/madara.py'},
    'nicomanga': {'main': f'{context}/nicomanga/main.py', 'run':f'{context}/nicomanga/run.py', 'search':f'{context}/nicomanga/search.py'},
    'momo_no_hana': {'main': f'{context}/momo_no_hana/main.py', 'run':f'{context}/momo_no_hana/run.py', 'search':f'{context}/momo_no_hana/search.py'},
    'manhastro': {'main': f'{context}/manhastro/main.py', 'run':f'{context}/manhastro/run.py', 'search':f'{context}/manhastro/search.py'},
    'valkyrie_scan': {'main': f'{context}/valkyrie_scan/main.py', 'run':f'{context}/valkyrie_scan/run.py', 'search':f'{context}/valkyrie_scan/search.py'},
    'limbo_scan': {'main': f'{context}/limbo_scan/main.py', 'run':f'{context}/limbo_scan/run.py', 'search':f'{context}/limbo_scan/search.py'},
    'nobre_scan': {'main': f'{context}/nobre_scan/main.py', 'run':f'{context}/nobre_scan/run.py', 'search':f'{context}/nobre_scan/search.py'},
    'iris_scanlator': {'main': f'{context}/iris_scanlator/main.py', 'run':f'{context}/iris_scanlator/run.py', 'search':f'{context}/iris_scanlator/search.py'}
}


# Src
urls2 = {
    'changelog':f'{context2}/changelog.py',
    'change_log':f'{context2}/change_log.txt',
    'check':f'{context2}/check.py',
    'download':f'{context2}/download.py',
    'execute_driver':f'{context2}/execute_driver.py',
    'folder_main':f'{context2}/folder_main.py',
    'imagemagick_check':f'{context2}/imagemagick_check.py',
    'load':f'{context2}/load.py',
    'organizar':f'{context2}/organizar.py',
    'print':f'{context2}/print.py',
    'save':f'{context2}/save.py',
    'time_zone':f'{context2}/time_zone.py',
    'clean':f'{context2}/clean.py',
    'move':f'{context2}/move.py',
    'animation':f'{context2}/animation.py',
    'status_check':f'{context2}/status_check.py',
    'folder_delete':f'{context2}/folder_delete.py'
}


# Setup
urls4 = {
    'main': f'{context4}/main.py',
    'ttk': f'{context4}/ttk.py'
}


# Engine
urls5 = {
    'default': f'{context5}/default.py',
    'undetected': f'{context5}/undetected.py',
    'cloudflare': f'{context5}/cloudflare.py'
}


# Imagens
urls6 = {
    'icon': f'{context6}/icon.ico'
}



# Cria as pastas necessárias
os.makedirs(app_folder, exist_ok=True)

for x in folder:
    x = os.path.join(app_folder, x)
    os.makedirs(x, exist_ok=True)

# Cria a pasta dos agregadores e baixa os seus arquivos necessários
for name, value in urls.items():
    folder_path = os.path.join(app_folder, 'urls', name)
    os.makedirs(folder_path, exist_ok=True)

    for file_name, file_url in value.items():
        file_path = os.path.join(folder_path, f"{file_name}.py")  # Adiciona a extensão .py ao nome do arquivo

        # Baixa o arquivo usando requests
        response = requests.get(file_url)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as file:
                file.write(response.content)
            print(f"Arquivo '{file_name}.py' baixado com sucesso.")
        else:
            print(f"Falha ao baixar o arquivo '{file_name}.py'. Código de status: {response.status_code}")



def download(file_path, file_url, file_name):
    # Baixa o arquivo usando requests
    response = requests.get(file_url)
    
    if response.status_code == 200:
        with open(file_path, 'wb') as file:
            file.write(response.content)
        print(f"Arquivo '{file_name}' baixado com sucesso.")
    else:
        print(f"Falha ao baixar o arquivo '{file_name}'. Código de status: {response.status_code}")

for name, value in urls2.items():
    file_path = os.path.join(app_folder, 'src', f'{name}.py') if name != 'change_log' else os.path.join(app_folder, 'src', f'{name}.txt')
    
    download(file_path, value, name)

for name, value in urls4.items():
    file_path = os.path.join(app_folder, 'setup', f'{name}.py')
    
    download(file_path, value, name)

for name, value in urls5.items():
    file_path = os.path.join(app_folder, 'engine', f'{name}.py')
    
    download(file_path, value, name)

for name, value in urls6.items():
    file_path = os.path.join(app_folder, 'images', f'{name}.ico')
    
    download(file_path, value, name)



os.system('cls')

import src.check as mdi
mdi.setup()

# Importações da pasta 'src'
import src.imagemagick_check as imc

# Importação da pasta 'Setup'
import setup.main as setup_main

# Verifica se o ImageMagick está instalado
imc.setup()

# Inicia a GUI
setup_main.setup()