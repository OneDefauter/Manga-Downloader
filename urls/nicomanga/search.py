import os
import re
import time
from selenium.webdriver.common.by import By

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    # Abre a página
    driver.get(url)
    
    # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
    driver.implicitly_wait(5)
    
    # Verifica o status do site
    result = status_check.setup(driver, url)
    if result != 200:
        return result
    
    time.sleep(2)
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    capitulos_encontrados = []
    chapter_elements = []
    
    try:
        chapter_elements = driver.find_elements(By.CLASS_NAME, "list-chapters")
    except:
        pass
    
    # Extrai os dados dos capítulos
    for element in chapter_elements:
        for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
            chapter_number = sub.find_element(By.CLASS_NAME, 'chapter-name').text
            
            # Use split para dividir a string e pegar o primeiro elemento
            chapter_number = chapter_number.split('\n', 1)[0]
    
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
            
            chapter_link = sub.get_attribute('href')
            
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
        
    return capitulos_encontrados

