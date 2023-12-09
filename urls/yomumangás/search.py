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
        sys.exit()
    
    time.sleep(5)
    
    for _ in range(3):
        script = 'document.querySelector(\'button[title="Alterar a quantidade de capítulos a vista"]\').click();'
        driver.execute_script(script)
        time.sleep(1)  # Aguarde um pouco entre os cliques se necessário
    
    os.system("cls")
    print("Verificando capítulos...")
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    capitulos_encontrados = []
    count = 2

    # Loop para percorrer todas as páginas
    while True:
        # Localiza os elementos que contêm as informações dos capítulos
        chapter_elements = driver.find_elements(By.CSS_SELECTOR, '[class^="styles_Chapters__"]')

        # Extrai os dados dos capítulos
        for element in chapter_elements:
            for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                chapter_number = sub.find_element(By.CSS_SELECTOR, 'h4').text
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                chapter_link = sub.get_attribute('href')

                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

        # Tenta clicar no botão de próxima página
        try:
            # Tenta clicar no botão de próxima página e verifica se há mais páginas
            next_page_button_script = 'var button = document.querySelector(\'button[title="Próxima Página"]\'); if (button && !button.hasAttribute("disabled")) { button.click(); return true; } else { return false; }'
            result = driver.execute_script(next_page_button_script)

            # Se não houver mais próxima página, sai do loop
            if not result:
                break
            
            print(f"Carregando página... {count}")
            
        except:
            # Se não houver mais próxima página, sai do loop
            print("Não há mais próxima página.")
            break
        
        count += 1
        # Aguarde um pouco para garantir que a próxima página seja totalmente carregada
        time.sleep(5)

    return capitulos_encontrados

