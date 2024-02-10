import os
import time
import shutil
import asyncio
from colorama import Fore, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import src.download as download
import src.organizar as organizar

import urls.br_mangas.change as mudar
import urls.br_mangas.ads as ads


async def setup(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, app_instance):
    folder_path = os.path.join(folder_selected, nome_foler, numero_capitulo)

    # Verificar se a pasta já existe e tem conteúdo
    contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

    print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")
    
    if contents:
        print(f"{Fore.GREEN}INFO:{Style.RESET_ALL} a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
        for item in contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Exclui pasta e conteúdo
            else:
                os.remove(item_path)  # Exclui arquivo

    os.makedirs(folder_path, exist_ok=True)

    driver.get(url)
    driver.implicitly_wait(10)
    time.sleep(1)
    
    if debug_var.get():
        baixando_label.config(text=f"Carregando capítulo {numero_capitulo}...")
    
    btn_next = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "thePicLink")))
    
    link = btn_next.get_attribute('href')
    
    driver.get(link)
    driver.implicitly_wait(10)
    time.sleep(1)
    
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "videonaoliberado")))
        ads.setup(driver)
        time.sleep(1)
    except:
        pass
    
    mudar.setup(driver)

    links_das_imagens = []

    try:
        # Agora você pode encontrar a div que contém as imagens
        div_imagens = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'images_all')))
        
        # Encontra todas as tags de imagem dentro da div
        imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

        # Extrai os links das imagens
        links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
    except:
        pass
    
    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
    
    # Criar lista de tarefas assíncronas para o download
    tasks = [download.download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

    # Agendar as tarefas para execução simultânea
    await asyncio.gather(*tasks)
    
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')

    organizar.organizar(folder_path, compactar, compact_extension, extension)
    
    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
