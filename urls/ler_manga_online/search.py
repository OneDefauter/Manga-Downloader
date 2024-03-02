import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")
    
    x = 1
    while True:
        capitulos_encontrados = []
        capitulos = []
        
        attempts = 0
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'capitulos'))
                )
                break
            except:
                attempts += 1
                driver.refresh()
        
        try:
            capitulos = driver.find_elements(By.CLASS_NAME, "capitulos")
        except:
            pass
        
        # Extrai os dados dos capítulos
        for element in capitulos:
            for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                chapter_number = sub.find_element(By.CLASS_NAME, 'capitulo').text

                # Use split para dividir a string e pegar o primeiro elemento
                chapter_number = chapter_number.split(' ', 1)[1].split(' ', 1)[0] if ' ' in chapter_number else chapter_number
                if chapter_number == "":
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

    return capitulos_encontrados