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
    driver.execute_script(f"window.open('{url}', '_blank')")
    
    time.sleep(10)
    
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    time.sleep(1)
    driver.switch_to.window(driver.window_handles[0])
    
    # Verifica o status do site
    def func(param):
        result = status_check.setup(driver, url)
        if result != 200:
            driver.quit()
            return result
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    time.sleep(2)

    capitulos_encontrados = []
    capitulos = []

    try:
        capitulos = driver.find_elements(By.XPATH, '//div[@class="eplister"]//ul[@class="clstyle"]//li')
    except:
        pass
    
    
    for capitulo in capitulos:
        numero_capitulo = float(capitulo.get_attribute('data-num'))
        if inicio <= numero_capitulo <= fim:
            link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados

