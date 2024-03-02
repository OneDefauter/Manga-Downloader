import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    # Abre a página
    driver.get(url)
    
    result = status_check.setup(driver, url)
    if result != 200:
        driver.quit()
        return result
    
    try:
        # Aguarda até que o botão esteja presente na página
        close_button = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close this dialog"]'))
        )
        close_button.click() # Clica no botão
    except:
        pass
    
    attempts = 1
    while attempts < max_attent:
        try:
            WebDriverWait(driver, 2).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.datechapter'))
            )
            break
        except:
            attempts += 1
            driver.refresh()
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    capitulos_encontrados = []
    trying = 1
    
    # Loop para percorrer todas as páginas
    while True:
        chapter_elements = []
        try:
            # Localiza os elementos que contêm as informações dos capítulos
            chapter_elements = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.datechapter'))
            )
        except:
            pass
        
        # Localiza os elementos que contêm as informações dos capítulos
        chapter_elements = driver.find_elements(By.CSS_SELECTOR, '.cardchapters')

        # Extrai os dados dos capítulos
        for chapter_element in chapter_elements:
            chapter_number = chapter_element.find_element(By.CSS_SELECTOR, 'a').text
            
            if chapter_number == '':
                continue
            
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '.')))

            if inicio <= numero_capitulo <= fim:
                chapter_link = chapter_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

        # Tenta clicar no botão de próxima página
        try:
            next_page_button = driver.find_element(By.XPATH, '//li[@class="page-item"]/a[@class="page-link" and contains(text(), ">")]')
            next_page_button.click()
        except:
            if trying < max_attent:
                if len(capitulos_encontrados) == 0:
                    driver.refresh()
                    trying += 1
                else:
                    break # Se não houver mais próxima página, sai do loop
            else:
                break # Se não houver mais próxima página, sai do loop
        
        try:
            WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '.datechapter'))
            )
        except:
            print("Erro")
            input()
        
        # time.sleep(1)

    return capitulos_encontrados

