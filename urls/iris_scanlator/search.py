import os
import time
from selenium.webdriver.common.by import By

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance):
    # Abre a página
    driver.get(url)
    
    # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
    driver.implicitly_wait(5)
    
    result = status_check.setup(driver, url)
    if result != 200:
        driver.quit()
        return result
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    time.sleep(2)

    capitulos_encontrados = []
    capitulos = []

    try:
        capitulos = driver.find_elements(By.XPATH, '//div[@class="eplister"]//ul[@class="clstyle"]//li')
    except:
        pass
    
    
    for capitulo in capitulos:
        numero_capitulo = float(capitulo.get_attribute('data-num'))
        if inicio <= numero_capitulo <= fim:
            link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados

