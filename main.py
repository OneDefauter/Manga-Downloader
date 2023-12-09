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

context = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/urls/'
context2 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/src/'
context3 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/themes/'
context4 = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/setup/'

urls = {
    'argos_comics': {'main': f'{context}/argos_comics/main.py', 'run':f'{context}/argos_comics/run.py', 'search':f'{context}/argos_comics/search.py'},
    'argos_hentai': {'main': f'{context}/argos_hentai/main.py', 'run':f'{context}/argos_hentai/run.py', 'search':f'{context}/argos_hentai/search.py'},
    'br_mangas': {'main': f'{context}/br_mangas/main.py', 'run':f'{context}/br_mangas/run.py', 'search':f'{context}/br_mangas/search.py', 'change':f'{context}/br_mangas/change.py'},
    'crystal_scan': {'main': f'{context}/crystal_scan/main.py', 'run':f'{context}/crystal_scan/run.py', 'search':f'{context}/crystal_scan/search.py'},
    'flower_manga': {'main': f'{context}/flower_manga/main.py', 'run':f'{context}/flower_manga/run.py', 'search':f'{context}/flower_manga/search.py'},
    'ler_mangá': {'main': f'{context}/ler_mangá/main.py', 'run':f'{context}/ler_mangá/run.py', 'search':f'{context}/ler_mangá/search.py'},
    'ler_manga_online': {'main': f'{context}/ler_manga_online/main.py', 'run':f'{context}/ler_manga_online/run.py', 'search':f'{context}/ler_manga_online/search.py'},
    'manga_br': {'main': f'{context}/manga_br/main.py', 'run':f'{context}/manga_br/run.py', 'search':f'{context}/manga_br/search.py'},
    'mangás_chan': {'main': f'{context}/mangás_chan/main.py', 'run':f'{context}/mangás_chan/run.py', 'search':f'{context}/mangás_chan/search.py'},
    'projeto_scanlator': {'main': f'{context}/projeto_scanlator/main.py', 'run':f'{context}/projeto_scanlator/run.py', 'search':f'{context}/projeto_scanlator/search.py'},
    'slimeread': {'main': f'{context}/slimeread/main.py', 'run':f'{context}/slimeread/run.py', 'search':f'{context}/slimeread/search.py', 'login':f'{context}/slimeread/login.py'},
    'tsuki': {'main': f'{context}/tsuki/main.py', 'run':f'{context}/tsuki/run.py', 'search':f'{context}/tsuki/search.py'},
    'yomumangás': {'main': f'{context}/yomumangás/main.py', 'run':f'{context}/yomumangás/run.py', 'search':f'{context}/yomumangás/search.py'}
}

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
    'theme':f'{context2}/theme.py',
    'time_zone':f'{context2}/time_zone.py'
}

urls3 = {
    'azure': {
        'azure': f'{context3}/azure/azure.tcl', 
        'theme': {
            'dark_tcl': f'{context3}/azure/theme/dark.tcl',
            'light_tcl': f'{context3}/azure/theme/dark.tcl',
            'dark': {
                f'{context3}/azure/theme/dark/box-accent.png',
                f'{context3}/azure/theme/dark/box-basic.png',
                f'{context3}/azure/theme/dark/box-hover.png',
                f'{context3}/azure/theme/dark/box-invalid.png',
                f'{context3}/azure/theme/dark/button-hover.png',
                f'{context3}/azure/theme/dark/card.png',
                f'{context3}/azure/theme/dark/check-accent.png',
                f'{context3}/azure/theme/dark/check-basic.png',
                f'{context3}/azure/theme/dark/check-hover.png',
                f'{context3}/azure/theme/dark/check-tri-accent.png',
                f'{context3}/azure/theme/dark/check-tri-basic.png',
                f'{context3}/azure/theme/dark/check-tri-hover.png',
                f'{context3}/azure/theme/dark/circle-accent.png',
                f'{context3}/azure/theme/dark/circle-basic.png',
                f'{context3}/azure/theme/dark/circle-hover.png',
                f'{context3}/azure/theme/dark/combo-button-basic.png',
                f'{context3}/azure/theme/dark/combo-button-focus.png',
                f'{context3}/azure/theme/dark/combo-button-hover.png',
                f'{context3}/azure/theme/dark/down-accent.png',
                f'{context3}/azure/theme/dark/down.png',
                f'{context3}/azure/theme/dark/empty.png',
                f'{context3}/azure/theme/dark/hor-accent.png',
                f'{context3}/azure/theme/dark/hor-basic.png',
                f'{context3}/azure/theme/dark/hor-hover.png',
                f'{context3}/azure/theme/dark/notebook.png',
                f'{context3}/azure/theme/dark/off-basic.png',
                f'{context3}/azure/theme/dark/on-accent.png',
                f'{context3}/azure/theme/dark/on-basic.png',
                f'{context3}/azure/theme/dark/outline-basic.png',
                f'{context3}/azure/theme/dark/outline-hover.png',
                f'{context3}/azure/theme/dark/radio-accent.png',
                f'{context3}/azure/theme/dark/radio-basic.png',
                f'{context3}/azure/theme/dark/radio-hover.png',
                f'{context3}/azure/theme/dark/radio-tri-accent.png',
                f'{context3}/azure/theme/dark/radio-tri-basic.png',
                f'{context3}/azure/theme/dark/radio-tri-hover.png',
                f'{context3}/azure/theme/dark/rect-accent-hover.png',
                f'{context3}/azure/theme/dark/rect-accent.png',
                f'{context3}/azure/theme/dark/rect-basic.png',
                f'{context3}/azure/theme/dark/rect-hover.png',
                f'{context3}/azure/theme/dark/right.png',
                f'{context3}/azure/theme/dark/scale-hor.png',
                f'{context3}/azure/theme/dark/scale-vert.png',
                f'{context3}/azure/theme/dark/separator.png',
                f'{context3}/azure/theme/dark/size.png',
                f'{context3}/azure/theme/dark/tab-basic.png',
                f'{context3}/azure/theme/dark/tab-disabled.png',
                f'{context3}/azure/theme/dark/tab-hover.png',
                f'{context3}/azure/theme/dark/tick-hor-accent.png',
                f'{context3}/azure/theme/dark/tick-hor-basic.png',
                f'{context3}/azure/theme/dark/tick-hor-hover.png',
                f'{context3}/azure/theme/dark/tick-vert-accent.png',
                f'{context3}/azure/theme/dark/tick-vert-basic.png',
                f'{context3}/azure/theme/dark/tick-vert-hover.png',
                f'{context3}/azure/theme/dark/tree-basic.png',
                f'{context3}/azure/theme/dark/tree-pressed.png',
                f'{context3}/azure/theme/dark/up-accent.png',
                f'{context3}/azure/theme/dark/up.png',
                f'{context3}/azure/theme/dark/vert-accent.png',
                f'{context3}/azure/theme/dark/vert-basic.png',
                f'{context3}/azure/theme/dark/vert-hover.png'
            },
            'light': {
                f'{context3}/azure/theme/light/box-accent.png',
                f'{context3}/azure/theme/light/box-basic.png',
                f'{context3}/azure/theme/light/box-hover.png',
                f'{context3}/azure/theme/light/box-invalid.png',
                f'{context3}/azure/theme/light/button-hover.png',
                f'{context3}/azure/theme/light/card.png',
                f'{context3}/azure/theme/light/check-accent.png',
                f'{context3}/azure/theme/light/check-basic.png',
                f'{context3}/azure/theme/light/check-hover.png',
                f'{context3}/azure/theme/light/check-tri-accent.png',
                f'{context3}/azure/theme/light/check-tri-basic.png',
                f'{context3}/azure/theme/light/check-tri-hover.png',
                f'{context3}/azure/theme/light/circle-accent.png',
                f'{context3}/azure/theme/light/circle-basic.png',
                f'{context3}/azure/theme/light/circle-hover.png',
                f'{context3}/azure/theme/light/combo-button-basic.png',
                f'{context3}/azure/theme/light/combo-button-focus.png',
                f'{context3}/azure/theme/light/combo-button-hover.png',
                f'{context3}/azure/theme/light/down-accent.png',
                f'{context3}/azure/theme/light/down.png',
                f'{context3}/azure/theme/light/empty.png',
                f'{context3}/azure/theme/light/hor-accent.png',
                f'{context3}/azure/theme/light/hor-basic.png',
                f'{context3}/azure/theme/light/hor-hover.png',
                f'{context3}/azure/theme/light/notebook.png',
                f'{context3}/azure/theme/light/off-basic.png',
                f'{context3}/azure/theme/light/off-hover.png',
                f'{context3}/azure/theme/light/on-accent.png',
                f'{context3}/azure/theme/light/on-basic.png',
                f'{context3}/azure/theme/light/on-hover.png',
                f'{context3}/azure/theme/light/outline-basic.png',
                f'{context3}/azure/theme/light/outline-hover.png',
                f'{context3}/azure/theme/light/radio-accent.png',
                f'{context3}/azure/theme/light/radio-basic.png',
                f'{context3}/azure/theme/light/radio-hover.png',
                f'{context3}/azure/theme/light/radio-tri-accent.png',
                f'{context3}/azure/theme/light/radio-tri-basic.png',
                f'{context3}/azure/theme/light/radio-tri-hover.png',
                f'{context3}/azure/theme/light/rect-accent-hover.png',
                f'{context3}/azure/theme/light/rect-accent.png',
                f'{context3}/azure/theme/light/rect-basic.png',
                f'{context3}/azure/theme/light/rect-hover.png',
                f'{context3}/azure/theme/light/right.png',
                f'{context3}/azure/theme/light/scale-hor.png',
                f'{context3}/azure/theme/light/scale-vert.png',
                f'{context3}/azure/theme/light/separator.png',
                f'{context3}/azure/theme/light/size.png',
                f'{context3}/azure/theme/light/tab-basic.png',
                f'{context3}/azure/theme/light/tab-disabled.png',
                f'{context3}/azure/theme/light/tab-hover.png',
                f'{context3}/azure/theme/light/tick-hor-accent.png',
                f'{context3}/azure/theme/light/tick-hor-basic.png',
                f'{context3}/azure/theme/light/tick-hor-hover.png',
                f'{context3}/azure/theme/light/tick-vert-accent.png',
                f'{context3}/azure/theme/light/tick-vert-basic.png',
                f'{context3}/azure/theme/light/tick-vert-hover.png',
                f'{context3}/azure/theme/light/tree-basic.png',
                f'{context3}/azure/theme/light/tree-pressed.png',
                f'{context3}/azure/theme/light/up-accent.png',
                f'{context3}/azure/theme/light/up.png',
                f'{context3}/azure/theme/light/vert-accent.png',
                f'{context3}/azure/theme/light/vert-basic.png',
                f'{context3}/azure/theme/light/vert-hover.png'
            }
        }
    },
    'forest': {
        'forest_dark_tcl': f'{context3}/forest/forest-dark.tcl',
        'forest_light_tcl': f'{context3}/forest/forest-light.tcl',
        'forest-dark': {
            f'{context3}/forest/forest-dark/border-accent-hover.png',
            f'{context3}/forest/forest-dark/border-accent.png',
            f'{context3}/forest/forest-dark/border-basic.png',
            f'{context3}/forest/forest-dark/border-hover.png',
            f'{context3}/forest/forest-dark/border-invalid.png',
            f'{context3}/forest/forest-dark/card.png',
            f'{context3}/forest/forest-dark/check-accent.png',
            f'{context3}/forest/forest-dark/check-basic.png',
            f'{context3}/forest/forest-dark/check-hover.png',
            f'{context3}/forest/forest-dark/check-tri-accent.png',
            f'{context3}/forest/forest-dark/check-tri-basic.png',
            f'{context3}/forest/forest-dark/check-tri-hover.png',
            f'{context3}/forest/forest-dark/check-unsel-accent.png',
            f'{context3}/forest/forest-dark/check-unsel-basic.png',
            f'{context3}/forest/forest-dark/check-unsel-hover.png',
            f'{context3}/forest/forest-dark/check-unsel-pressed.png',
            f'{context3}/forest/forest-dark/circle-accent.png',
            f'{context3}/forest/forest-dark/circle-basic.png',
            f'{context3}/forest/forest-dark/circle-hover.png',
            f'{context3}/forest/forest-dark/combo-button-basic.png',
            f'{context3}/forest/forest-dark/combo-button-focus.png',
            f'{context3}/forest/forest-dark/combo-button-hover.png',
            f'{context3}/forest/forest-dark/down.png',
            f'{context3}/forest/forest-dark/empty.png',
            f'{context3}/forest/forest-dark/hor-accent.png',
            f'{context3}/forest/forest-dark/hor-basic.png',
            f'{context3}/forest/forest-dark/hor-hover.png',
            f'{context3}/forest/forest-dark/notebook.png',
            f'{context3}/forest/forest-dark/off-accent.png',
            f'{context3}/forest/forest-dark/off-basic.png',
            f'{context3}/forest/forest-dark/off-hover.png',
            f'{context3}/forest/forest-dark/on-accent.png',
            f'{context3}/forest/forest-dark/on-basic.png',
            f'{context3}/forest/forest-dark/on-hover.png',
            f'{context3}/forest/forest-dark/radio-accent.png',
            f'{context3}/forest/forest-dark/radio-basic.png',
            f'{context3}/forest/forest-dark/radio-hover.png',
            f'{context3}/forest/forest-dark/radio-tri-accent.png',
            f'{context3}/forest/forest-dark/radio-tri-basic.png',
            f'{context3}/forest/forest-dark/radio-tri-hover.png',
            f'{context3}/forest/forest-dark/radio-unsel-accent.png',
            f'{context3}/forest/forest-dark/radio-unsel-basic.png',
            f'{context3}/forest/forest-dark/radio-unsel-hover',
            f'{context3}/forest/forest-dark/radio-unsel-hover.png',
            f'{context3}/forest/forest-dark/rect-accent-hover.png',
            f'{context3}/forest/forest-dark/rect-accent.png',
            f'{context3}/forest/forest-dark/rect-basic.png',
            f'{context3}/forest/forest-dark/rect-hover.png',
            f'{context3}/forest/forest-dark/right.png',
            f'{context3}/forest/forest-dark/scale-hor.png',
            f'{context3}/forest/forest-dark/scale-vert.png',
            f'{context3}/forest/forest-dark/separator.png',
            f'{context3}/forest/forest-dark/sizegrip.png',
            f'{context3}/forest/forest-dark/spin-button-down-basic.png',
            f'{context3}/forest/forest-dark/spin-button-down-focus.png',
            f'{context3}/forest/forest-dark/spin-button-up.png',
            f'{context3}/forest/forest-dark/tab-accent.png',
            f'{context3}/forest/forest-dark/tab-basic.png',
            f'{context3}/forest/forest-dark/tab-hover.png',
            f'{context3}/forest/forest-dark/thumb-hor-accent.png',
            f'{context3}/forest/forest-dark/thumb-hor-basic.png',
            f'{context3}/forest/forest-dark/thumb-hor-hover.png',
            f'{context3}/forest/forest-dark/thumb-vert-accent.png',
            f'{context3}/forest/forest-dark/thumb-vert-basic.png',
            f'{context3}/forest/forest-dark/thumb-vert-hover.png',
            f'{context3}/forest/forest-dark/tree-basic.png',
            f'{context3}/forest/forest-dark/tree-pressed.png',
            f'{context3}/forest/forest-dark/up.png',
            f'{context3}/forest/forest-dark/vert-accent.png',
            f'{context3}/forest/forest-dark/vert-basic.png',
            f'{context3}/forest/forest-dark/vert-hover.png'
        },
        'forest-light': {
            f'{context3}/forest/forest-light/border-accent-hover.png',
            f'{context3}/forest/forest-light/border-accent.png',
            f'{context3}/forest/forest-light/border-basic.png',
            f'{context3}/forest/forest-light/border-hover.png',
            f'{context3}/forest/forest-light/border-invalid.png',
            f'{context3}/forest/forest-light/card.png',
            f'{context3}/forest/forest-light/check-accent.png',
            f'{context3}/forest/forest-light/check-basic.png',
            f'{context3}/forest/forest-light/check-hover.png',
            f'{context3}/forest/forest-light/check-tri-accent.png',
            f'{context3}/forest/forest-light/check-tri-basic.png',
            f'{context3}/forest/forest-light/check-tri-hover.png',
            f'{context3}/forest/forest-light/check-unsel-accent.png',
            f'{context3}/forest/forest-light/check-unsel-basic.png',
            f'{context3}/forest/forest-light/check-unsel-hover.png',
            f'{context3}/forest/forest-light/check-unsel-pressed.png',
            f'{context3}/forest/forest-light/circle-accent.png',
            f'{context3}/forest/forest-light/circle-basic.png',
            f'{context3}/forest/forest-light/circle-hover.png',
            f'{context3}/forest/forest-light/combo-button-basic.png',
            f'{context3}/forest/forest-light/combo-button-focus.png',
            f'{context3}/forest/forest-light/combo-button-hover.png',
            f'{context3}/forest/forest-light/down-focus.png',
            f'{context3}/forest/forest-light/down.png',
            f'{context3}/forest/forest-light/empty.png',
            f'{context3}/forest/forest-light/hor-accent.png',
            f'{context3}/forest/forest-light/hor-basic.png',
            f'{context3}/forest/forest-light/hor-hover.png',
            f'{context3}/forest/forest-light/notebook.png',
            f'{context3}/forest/forest-light/off-accent.png',
            f'{context3}/forest/forest-light/off-basic.png',
            f'{context3}/forest/forest-light/off-hover.png',
            f'{context3}/forest/forest-light/on-accent.png',
            f'{context3}/forest/forest-light/on-basic.png',
            f'{context3}/forest/forest-light/on-hover.png',
            f'{context3}/forest/forest-light/radio-accent.png',
            f'{context3}/forest/forest-light/radio-basic.png',
            f'{context3}/forest/forest-light/radio-hover.png',
            f'{context3}/forest/forest-light/radio-tri-accent.png',
            f'{context3}/forest/forest-light/radio-tri-basic.png',
            f'{context3}/forest/forest-light/radio-tri-hover.png',
            f'{context3}/forest/forest-light/radio-unsel-accent.png',
            f'{context3}/forest/forest-light/radio-unsel-basic.png',
            f'{context3}/forest/forest-light/radio-unsel-hover',
            f'{context3}/forest/forest-light/radio-unsel-hover.png',
            f'{context3}/forest/forest-light/radio-unsel-pressed.png',
            f'{context3}/forest/forest-light/rect-accent-hover.png',
            f'{context3}/forest/forest-light/rect-accent.png',
            f'{context3}/forest/forest-light/rect-basic.png',
            f'{context3}/forest/forest-light/rect-hover.png',
            f'{context3}/forest/forest-light/right-focus.png',
            f'{context3}/forest/forest-light/right.png',
            f'{context3}/forest/forest-light/scale-hor.png',
            f'{context3}/forest/forest-light/scale-vert.png',
            f'{context3}/forest/forest-light/separator.png',
            f'{context3}/forest/forest-light/sizegrip.png',
            f'{context3}/forest/forest-light/spin-button-down-basic.png',
            f'{context3}/forest/forest-light/spin-button-down-focus.png',
            f'{context3}/forest/forest-light/spin-button-up.png',
            f'{context3}/forest/forest-light/tab-accent.png',
            f'{context3}/forest/forest-light/tab-basic.png',
            f'{context3}/forest/forest-light/tab-hover.png',
            f'{context3}/forest/forest-light/thumb-hor-accent.png',
            f'{context3}/forest/forest-light/thumb-hor-basic.png',
            f'{context3}/forest/forest-light/thumb-hor-hover.png',
            f'{context3}/forest/forest-light/thumb-vert-accent.png',
            f'{context3}/forest/forest-light/thumb-vert-basic.png',
            f'{context3}/forest/forest-light/thumb-vert-hover.png',
            f'{context3}/forest/forest-light/tree-basic.png',
            f'{context3}/forest/forest-light/tree-pressed.png',
            f'{context3}/forest/forest-light/up.png',
            f'{context3}/forest/forest-light/vert-accent.png',
            f'{context3}/forest/forest-light/vert-basic.png',
            f'{context3}/forest/forest-light/vert-hover.png'
        }
    }
}

urls4 = {
    'main': f'{context4}/main.py'
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

for name, value in urls3.items():
    if name == 'azure':
        folder_path = os.path.join(app_folder, 'themes', name)
        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(app_folder, 'themes', name, 'theme', 'dark'), exist_ok=True)
        os.makedirs(os.path.join(app_folder, 'themes', name, 'theme', 'light'), exist_ok=True)
        
        file_path = os.path.join(folder_path, 'azure.tcl')
        download(file_path, value['azure'], 'azure.tcl')
        
        file_path = os.path.join(folder_path, 'theme', 'dark.tcl')
        download(file_path, value['theme']['dark_tcl'], 'dark.tcl')
        
        file_path = os.path.join(folder_path, 'theme', 'light.tcl')
        download(file_path, value['theme']['light_tcl'], 'light.tcl')
        
        for url_name in value['theme']['dark']:
            file_name = os.path.basename(url_name)
            file_path = os.path.join(folder_path, 'theme', 'dark', file_name)
            if not os.path.exists(file_path):
                download(file_path, url_name, file_name)
        
        for url_name in value['theme']['light']:
            file_name = os.path.basename(url_name)
            file_path = os.path.join(folder_path, 'theme', 'light', file_name)
            if not os.path.exists(file_path):
                download(file_path, url_name, file_name)
                
    if name == 'forest':
        folder_path = os.path.join(app_folder, 'themes', name)
        os.makedirs(folder_path, exist_ok=True)
        os.makedirs(os.path.join(app_folder, 'themes', name, 'forest-dark'), exist_ok=True)
        os.makedirs(os.path.join(app_folder, 'themes', name, 'forest-light'), exist_ok=True)
        
        file_path = os.path.join(folder_path, 'forest-dark.tcl')
        download(file_path, value['forest_dark_tcl'], 'forest-dark.tcl')
        
        file_path = os.path.join(folder_path, 'forest-light.tcl')
        download(file_path, value['forest_light_tcl'], 'forest-light.tcl')
        
        for url_name in value['forest-dark']:
            file_name = os.path.basename(url_name)
            file_path = os.path.join(folder_path, 'forest-dark', file_name)
            if not os.path.exists(file_path):
                download(file_path, url_name, file_name)
        
        for url_name in value['forest-light']:
            file_name = os.path.basename(url_name)
            file_path = os.path.join(folder_path, 'forest-light', file_name)
            if not os.path.exists(file_path):
                download(file_path, url_name, file_name)


for name, value in urls2.items():
    file_path = os.path.join(app_folder, 'src', f'{name}.py') if name != 'change_log' else os.path.join(app_folder, 'src', f'{name}.txt')
    
    download(file_path, value, name)

for name, value in urls4.items():
    file_path = os.path.join(app_folder, 'setup', f'{name}.py')
    
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