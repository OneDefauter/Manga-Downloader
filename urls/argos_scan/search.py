import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
    
    
    try:
        WebDriverWait(driver, 30).until(
                EC.visibility_of_element_located((By.CLASS_NAME, "obra-capitulos"))
            )
    except:
        pass
    
    
    if debug_var.get():
        baixando_label.config(text=f"Verificando capítulos")
    
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
        
        match = re.search(r'\d+', nome)
        if match:
            numero_capitulo = float(match.group())
        
        if inicio <= numero_capitulo <= fim:
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados

