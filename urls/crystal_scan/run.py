import os
import re
import sys
import time
import shutil
import asyncio
import aiohttp
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

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension):
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

    leitor = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, "reading-content"))
    )

    paginas = leitor.find_elements(By.CLASS_NAME, 'page-break')
    links_das_imagens = []

    # Função para rolar até a imagem e aguardar o carregamento
    def scroll_to_image(image_element):
        driver.execute_script("arguments[0].scrollIntoView();", image_element)
        wait_time = 0
        while not image_element.get_attribute("complete") and wait_time < 10:
            time.sleep(1)
            wait_time += 1

    # Itera sobre as imagens
    for pagina in paginas:
        imagem = pagina.find_element(By.TAG_NAME, 'img')
        scroll_to_image(imagem)
        
        # Aqui você pode adicionar o código para baixar a imagem ou qualquer outra ação desejada
        links_das_imagens.append(str(imagem.get_attribute('src')))
        
    # Extrai os links das imagens
    links_das_imagens = [link.strip() for link in links_das_imagens]

    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
    
    # Criar lista de tarefas assíncronas para o download
    tasks = [download.download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

    # Agendar as tarefas para execução simultânea
    await asyncio.gather(*tasks)

    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

