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
        
    time.sleep(1)
    
    try:
        # Aguarda até que o botão esteja presente na página
        close_button = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close this dialog"]'))
        )

        # Clica no botão
        close_button.click()

    except:
        pass
    
    print("Verificando capítulos...")
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    capitulos_encontrados = []
    count = 2
    
    # Loop para percorrer todas as páginas
    while True:
        chapter_elements = []
        try:
            # Localiza os elementos que contêm as informações dos capítulos
            chapter_elements = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.datechapter'))
            )
        except:
            pass
        
        # Localiza os elementos que contêm as informações dos capítulos
        chapter_elements = driver.find_elements(By.CSS_SELECTOR, '.cardchapters')

        # Extrai os dados dos capítulos
        for chapter_element in chapter_elements:
            chapter_number = chapter_element.find_element(By.CSS_SELECTOR, 'a').text
            
            if chapter_number == '':
                continue
            
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '.')))

            if inicio <= numero_capitulo <= fim:
                chapter_link = chapter_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

        # Tenta clicar no botão de próxima página
        try:
            next_page_button = driver.find_element(By.XPATH, '//li[@class="page-item"]/a[@class="page-link" and contains(text(), ">")]')
            next_page_button.click()
        except:
            # Se não houver mais próxima página, sai do loop
            break
        
        count += 1
        # Aguarde um pouco para garantir que a próxima página seja totalmente carregada
        
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.datechapter'))
            )
        except:
            print("Erro")
            input()
        
        # time.sleep(1)

    return capitulos_encontrados

