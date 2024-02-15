import os
import re
import time
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
    
    # Injeta um script JavaScript para simular um pequeno movimento do mouse
    driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

    # Aguarde até que o botão seja visível (você pode ajustar o tempo de espera conforme necessário)
    try:
        element = WebDriverWait(driver, 5).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "chapter-readmore"))
        )

        # Clique no botão
        element.click()

    except:
        pass
    
    time.sleep(3)
    
    os.system("cls")
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    chapter_elements = []

    try:
        # Esperar a lista de capítulos carregar
        chapter_elements = driver.find_elements(By.CLASS_NAME, "wp-manga-chapter")
    except:
        pass
    

    capitulos_encontrados = []

    for capitulo in chapter_elements:
        # Encontra o elemento 'a' dentro do 'li'
        a_element = capitulo.find_element(By.TAG_NAME, "a")

        # Obtém o texto do número do capítulo
        # Usa expressão regular para extrair números, pontos e vírgulas
        numero_capitulo = re.sub(r'[^0-9.,]', '', a_element.text.strip())
        numero_capitulo = float(re.sub(r'^\.', '', numero_capitulo))

        if inicio <= numero_capitulo <= fim:
            link = a_element.get_attribute("href")
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados

