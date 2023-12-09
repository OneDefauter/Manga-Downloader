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

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder):
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
    driver.implicitly_wait(5)

    time.sleep(0.5)
    
    verify1 = driver.find_element(By.XPATH, '/html/body/div/div')
    text = verify1.find_element(By.XPATH, '/html/body/div/div/div[2]').text
    if "Capítulo aguardando aprovação." in text:
        print("Capítulo aguardando aprovação.")
        return 4
    
    links_das_imagens = []
    count = 1
    
    if debug_var.get():
        baixando_label.config(text=f"Verificando capítulo {numero_capitulo}")
    
    wait = WebDriverWait(driver, 10)
    
    # Espera o leitor carregar
    while True:
        try:
            wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.pagereader')))
        finally:
            break
    
    # Descobrir a quantidade de paginas
    elemento_lista_paginas = driver.find_element(By.CSS_SELECTOR, 'div[id^="el-popper-container-"] div:nth-child(2) div div div:nth-child(1) ul')
    itens_lista_paginas = elemento_lista_paginas.find_elements(By.CSS_SELECTOR, 'li')
    numero_ultima_pagina = int(len(itens_lista_paginas))
    
    while True:
        if debug_var.get():
            baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nCarregando página: {count} / {numero_ultima_pagina}")
    
        imagem_leitor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, 'pagereader'))
        )
        
        # Obtém a URL atual
        url_anterior = driver.current_url
    
        # Tente verificar se a imagem foi carregada até 10 vezes
        tentativas = 0
        max_tentativas = 300
        
        while tentativas < max_tentativas:
            try:
                # Aguardar até que a imagem esteja presente no DOM
                WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, ".manga-reader img.pagereader"))
                )
                
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
                    # Encontrar o elemento da imagem pelo seletor CSS
                    imagem_elemento = driver.find_element(By.CSS_SELECTOR, ".manga-reader img.pagereader")

                    # Obter a URL da imagem do atributo 'src'
                    imagem_url = imagem_elemento.get_attribute("src")

                    # Abrir a imagem em uma nova guia usando JavaScript
                    script = f"window.open('{imagem_url}', '_blank');"
                    driver.execute_script(script)
                    
                    # Obter todas as guias abertas
                    janelas_abertas = driver.window_handles
                    
                    if len(janelas_abertas) == 2:
                        time.sleep(0.2)
                        janelas_abertas = driver.window_handles
                        if len(janelas_abertas) == 1:
                            if debug_var.get():
                                baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nBaixando página: {count} / {numero_ultima_pagina}")
    
                            lista = os.listdir(download_folder)
                    
                            for _ in range(1, 300):
                                if len(lista) != 0:
                                    if not ".crdownload" in lista[0]:
                                        break
                                    else:
                                        lista = os.listdir(download_folder)
                                        time.sleep(1)
                                else:
                                    time.sleep(1)
                            
                            file = os.path.join(download_folder, lista[0])
                            
                            image_extension = os.path.splitext(lista[0])[1]
                            
                            image_name = f"{count:02d}.{image_extension}"
                            image_path = os.path.join(folder_path, image_name)
                            
                            print(f"Baixando {imagem_url} como {image_name}...")
                            
                            os.makedirs(folder_path, exist_ok=True)
                            
                            shutil.move(file, image_path)
                            
                            break
                            
                    
                    # Mudar para a nova guia (que deve ser a última na lista)
                    driver.switch_to.window(janelas_abertas[-1])
                    
                    if debug_var.get():
                        baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nBaixando página: {count} / {numero_ultima_pagina}")
    
                    while True:
                        try:
                            # Executar um script JavaScript para verificar se a imagem foi carregada
                            script2 = """
                                var imagem = document.querySelector('img');
                                if (imagem.complete) {
                                    return true;
                                } else {
                                    return false;
                                }
                            """
                        
                            imagem_carregada2 = driver.execute_script(script2)
                            
                            if imagem_carregada2:
                                break
                        except:
                            ...
                    
                    action_chains = ActionChains(driver)

                    # Pressione a tecla Alt
                    action_chains.key_down(Keys.ALT)

                    # Pressione a tecla W
                    action_chains.send_keys('w')

                    # Libere a tecla Alt
                    action_chains.key_up(Keys.ALT)

                    # Execute as ações
                    action_chains.perform()

                    time.sleep(0.5)

                    download_button = driver.find_element(By.CLASS_NAME, "download-direct")
                    download_button.click()

                    time.sleep(0.5)
                    
                    lista = os.listdir(download_folder)
                    
                    for _ in range(1, 300):
                        if len(lista) != 0:
                            if not ".crdownload" in lista[0]:
                                break
                            else:
                                lista = os.listdir(download_folder)
                                time.sleep(1)
                        else:
                            time.sleep(1)
                    
                    file = os.path.join(download_folder, lista[0])
                    
                    image_extension = os.path.splitext(lista[0])[1]
                    
                    image_name = f"{count:02d}.{image_extension}"
                    image_path = os.path.join(folder_path, image_name)
                    
                    print(f"Baixando {imagem_url} como {image_name}...")
                    
                    time.sleep(0.5)
                    
                    shutil.move(file, image_path)
                    
                    time.sleep(0.2)
                    
                    # Fechar a guia atual
                    driver.close()
                    
                    break  # Sair do loop se a imagem foi carregada com sucesso
                else:
                    tentativas += 1
                    # print(f"Tentativa {tentativas}: A imagem ainda não foi carregada. Tentando novamente...")
                    time.sleep(1)
            except TimeoutException:
                tentativas += 1
                # print(f"Tentativa {tentativas}: Tempo limite expirado. Tentando novamente...")
                time.sleep(1)

        driver.switch_to.window(janelas_abertas[0])

        div_imagens = driver.find_element(By.XPATH, '/html/body/div/div')
        imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

        links_das_imagens += [imagem.get_attribute('src') for imagem in imagens]
        
        if count == numero_ultima_pagina:
            break
            
        # Clica na imagem do leitor para avançar para a próxima página
        # imagem_leitor.click()
        # Clique no elemento usando JavaScript
        driver.execute_script("arguments[0].click();", imagem_elemento)
        
        time.sleep(1)

        # Verifica se a nova URL contém um indicativo de próximo capítulo
        nova_url = driver.current_url
        
        if url_anterior != nova_url:
            break
        
        count += 1
        
    links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
    links_das_imagens = [link for link in links_das_imagens if link is not None]
    links_das_imagens = [link for link in links_das_imagens if not 'data:image' in link]
    links_das_imagens = [urlunparse(urlparse(url)._replace(query='')) for url in links_das_imagens]
    links_das_imagens = sorted(links_das_imagens)
    
    if len(links_das_imagens) == 0:
        print("Nenhuma imagem encontrada")
        if debug_var.get():
            baixando_label.config(text=f"Erro no capítulo {numero_capitulo}\nNenhuma imagem encontrada")
        return 2

    # if debug_var.get():
        # baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

    # Criar lista de tarefas assíncronas para o download
    # tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

    # Agendar as tarefas para execução simultânea
    # await asyncio.gather(*tasks)
    
    if debug_var.get():
        baixando_label.config(text=f"Organizando capítulo {numero_capitulo}")

    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
    
    return 0

