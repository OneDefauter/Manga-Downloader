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

    time.sleep(2)
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    lista_capitulos = []

    try:
        lista_capitulos = driver.find_elements(By.CLASS_NAME, "single-chapter")
    except:
        pass

    capitulos_encontrados = []

    for capitulo in lista_capitulos:
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

