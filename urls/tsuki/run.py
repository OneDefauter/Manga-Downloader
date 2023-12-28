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
import src.move as move

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, app_instance):
    folder_path = os.path.join(folder_selected, nome_foler, numero_capitulo)

    # Verificar se a pasta já existe e tem conteúdo
    contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

    print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

    if debug_var.get():
        baixando_label.config(text=f"Verificando pasta do capítulo {numero_capitulo}")
        
    if contents:
        print(f"{Fore.GREEN}INFO:{Style.RESET_ALL} a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
        for item in contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Exclui pasta e conteúdo
            else:
                os.remove(item_path)  # Exclui arquivo

    os.makedirs(folder_path, exist_ok=True)

    if debug_var.get():
        baixando_label.config(text=f"Aguardando página do capítulo {numero_capitulo}")

    driver.get(url)
    driver.implicitly_wait(10)

    time.sleep(1)
    
    verify1 = driver.find_element(By.XPATH, '/html/body/div/div')
    text = verify1.find_element(By.XPATH, '/html/body/div/div/div[2]').text
    if "Capítulo aguardando aprovação." in text:
        print("Capítulo aguardando aprovação.")
        return 4
    
    links_das_imagens = []
    count = 0
    
    # Espera o leitor carregar
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.pagereader')))
        finally:
            break
    
    # Descobrir a quantidade de paginas
    elemento_lista_paginas = driver.find_element(By.CSS_SELECTOR, 'div[id^="el-popper-container-"] div:nth-child(2) div div div:nth-child(1) ul')
    itens_lista_paginas = elemento_lista_paginas.find_elements(By.CSS_SELECTOR, 'li')
    numero_ultima_pagina = int(len(itens_lista_paginas))
    
    
    while count < numero_ultima_pagina:
        if debug_var.get():
            baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nCarregando páginas: {count + 1} / {numero_ultima_pagina}")
            
        # Aguardar até que a imagem esteja presente no DOM
        try:
            imagem_elemento = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, ".manga-reader img.pagereader"))
            )
        except:
            continue
            
        close = 0
        close_max = 60
            
        while close < close_max:
            # Executar um script JavaScript para verificar se a imagem foi carregada
            script = """
                var imagem = document.querySelector('.manga-reader img.pagereader');
                if (imagem.complete) {
                    return true;
                } else {
                    return false;
                }
            """
            
            imagem_carregada = driver.execute_script(script)
            
            if imagem_carregada:
                links_das_imagens.append(imagem_elemento.get_attribute("src"))
                break
            
            else:
                time.sleep(1)
                close += 1
                
        driver.execute_script("arguments[0].click();", imagem_elemento)
        count += 1
        
        time.sleep(1)
    
    count = 1
            
    for imagem in links_das_imagens:
        if debug_var.get():
            baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nBaixando página: {count} / {numero_ultima_pagina}")
            
        driver.get(imagem)
        
        try:
            input_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="number"]'))
            )
        except:
            driver.refresh()
            time.sleep(1)
            
            input_element = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="number"]'))
            )
        
        input_element.clear()  # Limpa qualquer valor existente no campo
        input_element.send_keys(count)
        
        download_button = WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/button"))
        )
        download_button.click()
        
        print(f"{Fore.GREEN}Baixando {imagem} como {count:02d}.png...{Style.RESET_ALL}")
        
        time.sleep(0.5)
        
        count += 1
    
    if debug_var.get():
        baixando_label.config(text=f"Arrumando páginas...")
        
    time.sleep(3)
    
    close = 0
    max_close = 60
    
    while close < max_close:
        lista = os.listdir(download_folder)
        
        if count == len(lista) + 1:
            if not ".crdownload" in lista:
                break
            
        time.sleep(1)
        close += 1
        
        if debug_var.get():
            baixando_label.config(text=f"Arrumando páginas...\nAguarde {close} / {max_close}")
    
    move.setup(download_folder, folder_path)
            
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')
    
    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
    
    return 0

