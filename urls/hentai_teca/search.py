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
    
    time.sleep(3)
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    # Injeta um script JavaScript para simular um pequeno movimento do mouse
    driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

    try:
        btn = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "chapter-readmore"))
        )
        
        btn.click()
    except:
        ...
    
    time.sleep(2)

    chapter_elements = []

    try:
        # Localiza os elementos que contêm as informações dos capítulos
        chapter_elements = driver.find_elements(By.CLASS_NAME, "wp-manga-chapter")
    except:
        pass

    capitulos_encontrados = []

    for capitulo in chapter_elements:
        # Encontra o elemento 'a' dentro do 'li'
        a_element = capitulo.find_element(By.TAG_NAME, "a")

        # Obtém o texto do número do capítulo
        # Usa expressão regular para extrair números, pontos e vírgulas
        numero_capitulo = float(re.sub(r'[^0-9.,]', '', a_element.text.replace(',', '')))
        link = a_element.get_attribute("href")

        if inicio <= numero_capitulo <= fim:
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
        
    return capitulos_encontrados

