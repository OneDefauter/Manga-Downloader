import re
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
        attempts = 0
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "obra-capitulos"))
                )
                break
            except:
                attempts += 1
                driver.refresh()
        
        capitulos = []
        
        try:
            # Esperar até que o elemento desejado esteja presente na página
            capitulos_element = driver.find_element(By.CSS_SELECTOR, "div.obra-capitulos")
        
            # Obter os links dos capítulos
            capitulos = capitulos_element.find_elements(By.CSS_SELECTOR, "a.capitulo")
        except:
            pass
        
        capitulos_encontrados = []
        
        # Armazenar nome e link de cada capítulo na lista
        for capitulo in capitulos:
            link = capitulo.get_attribute("href")
            nome = capitulo.find_element(By.TAG_NAME, "p").text
            if nome == '':
                continue
            
            match = re.search(r'\d+', nome)
            if match:
                numero_capitulo = float(match.group())
            
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