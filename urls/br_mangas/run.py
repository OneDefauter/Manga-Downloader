import os
import time
import shutil
import asyncio
from colorama import Fore, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

import src.download as download
import src.organizar as organizar

import urls.br_mangas.change as mudar


async def setup(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension):
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
    
    try:
        # Espera até que o botão esteja presente na página
        btn_next = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "btn_next"))
        )

        # Abre o link em uma nova guia
        btn_next.send_keys(Keys.CONTROL + Keys.RETURN)
        
        # Espera até que a nova guia seja carregada
        WebDriverWait(driver, 10).until(
            EC.number_of_windows_to_be(2)  # Aguarda até que haja duas guias abertas
        )

        driver.close()
        janelas_abertas = driver.window_handles
        driver.switch_to.window(janelas_abertas[0])
        
        # Aguarda até que a página esteja completamente carregada
        WebDriverWait(driver, 30).until(
            lambda x: x.execute_script("return document.readyState") == "complete"
        )

        # Espera até que um elemento específico esteja presente na nova página
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "ver000"))
        )
        
        driver.refresh()

    except Exception as e:
        print(f"Erro: {e}")
    
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "modo_leitura"))
        )
    except Exception as e:
        print(e)
        input()
    
    mudar.setup(driver)

    # Agora você pode encontrar a div que contém as imagens
    div_imagens = driver.find_element(By.ID, 'images_all')

    # Encontra todas as tags de imagem dentro da div
    imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

    # Extrai os links das imagens
    links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
    
    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
    
    # Criar lista de tarefas assíncronas para o download
    tasks = [download.download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

    # Agendar as tarefas para execução simultânea
    await asyncio.gather(*tasks)

    organizar.organizar(folder_path, compactar, compact_extension, extension)
    
    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")