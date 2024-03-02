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
    
    time.sleep(5)
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    
    capitulos_encontrados = []
    chapter_elements = []
    
    try:
        chapter_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/div[4]/div/ul")
    except:
        pass
    
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    # Extrai os dados dos capítulos
    for element in chapter_elements:
        for sub in element.find_elements(By.CLASS_NAME, 'wp-manga-chapter'):
            chapter_number = sub.text

            # Use split para dividir a string e pegar o primeiro elemento
            chapter_number = chapter_number.split('-', 1)[0]

            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))

            sub2 = sub.find_element(By.CSS_SELECTOR, 'a')
            chapter_link = sub2.get_attribute('href')

            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

    return capitulos_encontrados

