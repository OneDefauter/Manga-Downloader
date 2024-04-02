import os
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    # Abre a página
    driver.get(url)
    
    # Verifica o status do site
    def func(param):
        result = status_check.setup(driver, url)
        if result != 200:
            return result

    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")
    
    x = 1
    while True:
        capitulos_encontrados = []
        
        driver.execute_script("window.dispatchEvent(new Event('mousemove'));")
        
        attempts = 0
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '//div[contains(@class, "bg-card")]//a//div//h2'))
                )
                break
            except:
                attempts += 1
                driver.refresh()
                
        capitulos = driver.find_elements(By.XPATH, '//div[@class="bg-card dark:bg-dark transition duration-300  p-4 rounded-lg"]')
        
        for capitulo in capitulos:
            chapter_link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')
            chapter_number = capitulo.find_element(By.XPATH, './/h2').text
            if chapter_number == '':
                continue
            
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
            
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
        
        if len(capitulos_encontrados) > 0:
            break
        else:
            if x < max_attent:
                x += 1
            else:
                break
    
    return capitulos_encontrados