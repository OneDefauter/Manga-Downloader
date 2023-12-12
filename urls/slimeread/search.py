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
        return 'e1'
    
    time.sleep(3)
    
    os.system("cls")
    
    print("Verificando capítulos...")
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    capitulos_encontrados = []
    turn = False

    # Espera a lista de capítulos carregar
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//section[@class='mt-8']"))
    )
    
    # Localiza os elementos que contêm as informações dos capítulos
    xpath = f'//html//body//div//div//main//section[@class="mt-8"]//div[@class="mt-2"]//div//div'
    chapter_elements = driver.find_elements(By.XPATH, xpath)
        
    if chapter_elements:
        # Mantém apenas o primeiro elemento e descarta os outros
        chapter_elements = [chapter_elements[0]]
        
    if "Cap" in chapter_elements[0].text:
        turn = True
    
    if turn is False:
        print("Erro: Nenhum capítulo encontrado")
        driver.quit()
        return 'e3'
    
    # Extrai os dados dos capítulos
    for element in chapter_elements:
        for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
            chapter_number = sub.find_element(By.CSS_SELECTOR, 'p').text
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
            chapter_link = sub.get_attribute('href')
            
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

    return capitulos_encontrados

