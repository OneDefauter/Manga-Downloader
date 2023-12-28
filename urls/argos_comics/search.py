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

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance):
    # Abre a página
    driver.get(url)
    
    # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
    driver.implicitly_wait(5)
    
    # Verifica o status do site
    result = status_check.setup(driver, url)
    if result != 200:
        driver.quit()
        return result
    
    # Injeta um script JavaScript para simular um pequeno movimento do mouse
    driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

    # Aguarde até que o botão seja visível (você pode ajustar o tempo de espera conforme necessário)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "chapter-readmore"))
        )

        # Clique no botão
        element.click()

    except:
        pass
    
    janelas_abertas = driver.window_handles
    
    for _ in range(1, 15):
        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            driver.close()
            janelas_abertas = driver.window_handles
            driver.switch_to.window(janelas_abertas[0])
            break
        else:
            janelas_abertas = driver.window_handles
            time.sleep(1)
    
    time.sleep(5)
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    try:
        # Localizar todos os elementos que têm a classe 'has-child'
        volumes_com_child = driver.find_elements(By.CLASS_NAME, 'has-child')

        # Expandir todos os volumes
        for volume in volumes_com_child:
            volume.click()
            time.sleep(1)
            # Aguarde a expansão do volume
            # wait.until(EC.presence_of_element_located((By.XPATH, f'{volume}/following-sibling::ul')))

    except TimeoutException:
        pass
    
    time.sleep(5)

    lista_capitulos = []

    try:
        # Esperar a lista de capítulos carregar
        wait = WebDriverWait(driver, 10)
        lista_capitulos = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sub-chap-list')))
    
        # Selecionar os elementos de capítulo
        lista_capitulos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sub-chap-list')))
    except:
        pass
    
    capitulos_encontrados = []

    for sub_chap_list in lista_capitulos:
        capitulos = sub_chap_list.find_elements(By.CLASS_NAME, 'wp-manga-chapter')

        for capitulo in capitulos:
            # Obter o número do capítulo
            # Obter o número do capítulo do texto do link
            link_text = capitulo.find_element(By.TAG_NAME, 'a').text
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', link_text.replace(',', '')))

            # Obter o link do capítulo
            link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Verificar se o capítulo está no intervalo desejado
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados

