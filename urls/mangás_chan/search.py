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
            return 0
    
    os.system("cls")
    print("Verificando capítulos...")
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    time.sleep(2)

    capitulos = driver.find_elements(By.XPATH, '//div[@class="eplister"]//li')

    capitulos_encontrados = []

    for capitulo in capitulos:
        numero_capitulo = float(capitulo.get_attribute('data-num'))
        if inicio <= numero_capitulo <= fim:
            link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados

