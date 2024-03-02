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
    result = status_check.setup(driver, url)
    if result != 200:
        return result
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")
    
    x = 1
    while True:
        capitulos = []
        capitulos_encontrados = []
        
        try:
            # Espere até que o elemento com o id "pageloader" esteja presente no DOM
            elemento_pageloader = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.ID, "pageloader"))
            )
            # Verifique se o estilo "display: none;" está presente no atributo style
            WebDriverWait(driver, 10).until(
                lambda driver: "display: none;" in elemento_pageloader.get_attribute("style")
            )
        except:
            pass
        
        attempts = 0
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'wp-manga-chapter'))
                )
                break
            except:
                attempts += 1
                driver.refresh()
                try:
                    # Espere até que o elemento com o id "pageloader" esteja presente no DOM
                    elemento_pageloader = WebDriverWait(driver, 3).until(
                        EC.presence_of_element_located((By.ID, "pageloader"))
                    )
                    # Verifique se o estilo "display: none;" está presente no atributo style
                    WebDriverWait(driver, 10).until(
                        lambda driver: "display: none;" in elemento_pageloader.get_attribute("style")
                    )
                except:
                    pass
        
        try:
            driver.execute_script("document.querySelector('.btn-adult-confirm').click();")
        except:
            pass
        
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "chapter-readmore")))
            driver.execute_script("document.querySelector('.chapter-readmore').click();")
        except:
            pass
        
        try:
            # Localiza os elementos que contêm as informações dos capítulos
            capitulos = driver.find_elements(By.CLASS_NAME, "wp-manga-chapter")
        except:
            pass

        for capitulo in capitulos:
            # Encontra o elemento 'a' dentro do 'li'
            link_text = capitulo.find_element(By.TAG_NAME, 'a').text
            if link_text == '':
                continue
            numero_capitulo = float(re.sub(r'[^\d.]+', '', link_text.replace(',', '')).replace('..', '.'))

            # Obter o link do capítulo
            link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')

            # Verificar se o capítulo está no intervalo desejado
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
        
        if len(capitulos_encontrados) > 0:
            break
        else:
            if x < max_attent:
                x += 1
            else:
                break

    if debug_var.get():
        baixando_label.config(text="Aguarde...")
    
    return capitulos_encontrados

