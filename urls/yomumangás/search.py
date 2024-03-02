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
        lista_capitulos = []
        capitulos_encontrados = []
        
        attempts = 0
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '[class^="styles_Chapters__"]'))
                )
                break
            except:
                attempts += 1
                driver.refresh()
        
        try:
            WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Mostrar tudo')]")))
            driver.execute_script("document.querySelector('button:contains(\"Mostrar tudo\")').click();")
        except:
            pass
        
        try:
            chapter_elements = driver.find_elements(By.CSS_SELECTOR, '[class^="styles_Chapters__"]')
        except:
            pass
        
        for element in chapter_elements:
            for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                chapter_number = sub.text
                if chapter_number == '':
                    continue
                match = re.search(r'Capítulo (\d+)', chapter_number)
                if match:
                    numero_capitulo = float(match.group(1))
                else:
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '.')))
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