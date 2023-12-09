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

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label):
    # Abre a página
    driver.get(url)
    
    # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
    driver.implicitly_wait(5)
    
    # Verifica se a página contém o texto "Página não encontrada"
    if "Página não encontrada" in driver.page_source:
            print("Erro: URL inválida. Status code: 404")
            driver.quit()
            return
    
    time.sleep(5)
    
    os.system("cls")
    print("Verificando capítulos...")
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    capitulos_encontrados = []
    chapter_elements = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div")
    
    # Extrai os dados dos capítulos
    for element in chapter_elements:
        for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
            chapter_number = sub.find_element(By.CLASS_NAME, 'mb-0').text
            
            # Use split para dividir a string e pegar o primeiro elemento
            chapter_number = chapter_number.split('\n', 1)[0]
    
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
            
            chapter_link = sub.get_attribute('href')
            
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
        
    return capitulos_encontrados

