import os
import re
import sys
import time
import shutil
import asyncio
import aiohttp
from urllib.parse import urlparse, urlunparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style

import src.download as download
import src.organizar as organizar

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']):
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
    
    if debug_var.get():
        baixando_label.config(text=f"Verificando capítulo {numero_capitulo}")
    
    # Injeta um script JavaScript para simular um pequeno movimento do mouse
    driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

    time.sleep(3)
    
    # Encontrar o elemento <select>
    select_element = driver.find_element(By.ID, 'select-paged')

    # Obter todas as opções dentro do <select>
    options = select_element.find_elements(By.TAG_NAME, 'option')

    # Iterar sobre cada opção
    for option in options:
        try:
            # Clicar na opção para selecioná-la
            option.click()

            # Aguardar até que a página seja carregada (aqui estamos esperando por até 10 segundos)
            WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'selector.pagedsel.r'))
            )

            # Adicione aqui a lógica adicional para processar a página conforme necessário
            # ...
            time.sleep(1)

        except Exception as e:
            print(f"Erro ao processar a opção: {e}")
    
    # Encontra a div que contém as imagens
    div_imagens = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/article/div[3]')

    # Encontra todas as tags de imagem dentro da div
    imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

    # Extrai os links das imagens
    links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
    links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
    links_das_imagens = [link for link in links_das_imagens if link is not None]
    links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

    # Criar lista de tarefas assíncronas para o download
    tasks = [download.download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

    # Agendar as tarefas para execução simultânea
    await asyncio.gather(*tasks)

    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

