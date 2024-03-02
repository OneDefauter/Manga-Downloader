import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    # Abre a página
    driver.execute_script(f"window.open('{url}', '_blank')")
    
    time.sleep(10)
    
    driver.switch_to.window(driver.window_handles[0])
    driver.close()
    driver.switch_to.window(driver.window_handles[0])
    
    # Verifica o status do site
    def func(param):
        result = status_check.setup(driver, url)
        if result != 200:
            driver.quit()
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
                WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.XPATH, '//div[@class="eplister"]//ul//li'))
                )
                break
            except:
                attempts += 1
                driver.refresh()
        
        try:
            capitulos = driver.find_elements(By.XPATH, '//div[@class="eplister"]//ul//li')
        except:
            pass
        
        for capitulo in capitulos:
            numero_capitulo = float(capitulo.get_attribute('data-num'))
            if inicio <= numero_capitulo <= fim:
                link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
            
        if len(capitulos_encontrados) > 0:
            break
        else:
            if x < max_attent:
                x += 1
            else:
                break

    return capitulos_encontrados