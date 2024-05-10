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
        capitulos_encontrados = []
        capitulos = []
        
        attempts = 1
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, "/html/body/main/div/div/div/div[2]/div/div"))
                )
                break
            except:
                attempts += 1
                driver.refresh()
        
        chapter_elements = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div")
    
        for element in chapter_elements:
            for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                chapter_number = sub.find_element(By.CLASS_NAME, 'mb-0').text
                
                # Use split para dividir a string e pegar o primeiro elemento
                chapter_number = chapter_number.split('\n', 1)[0]
                if chapter_number == '':
                    continue
        
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                
                chapter_link = sub.get_attribute('href')
                
                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
    
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