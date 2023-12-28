import os
from selenium.webdriver.common.by import By

import src.status_check as status_check

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance):
    # Abre a página
    driver.get(url)
    
    # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
    driver.implicitly_wait(5)
    
    # Verifica o status do site
    result = status_check.setup(driver, url)
    if result != 200:
        driver.quit()
        return result
    
    capitulos = []
    
    try:
        # Esperar a lista de capítulos carregar
        capitulos = driver.find_elements(By.XPATH, '//div[@class="lista_manga"]//li[@class="row lista_ep"]')
    except:
        pass
    
    capitulos_encontrados = []
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    for capitulo in capitulos:
        numero_capitulo = float(capitulo.get_attribute('data-cap'))
        if inicio <= numero_capitulo <= fim:
            link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados
