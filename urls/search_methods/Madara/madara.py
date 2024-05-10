import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import src.status_check as status_check

def setup(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
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
        
        driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

        attempts = 0
        while attempts < max_attent:
            try:
                WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'wp-manga-chapter'))
                )
                break
            except:
                attempts += 1
                driver.refresh()
        
        try:
            driver.execute_script("document.querySelector('.btn-adult-confirm').click();")
        except:
            pass
        
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "chapter-readmore")))
            driver.execute_script("document.querySelector('.chapter-readmore').click();")
        except:
            pass

        try:
            driver.execute_script("document.querySelector('.has-child').click();")
            driver.execute_script('''
                var volumes = document.getElementsByClassName('has-child');
                for(var i = 0; i < volumes.length; i++){
                    volumes[i].click();
                    // Aguarde um segundo entre os cliques (opcional)
                    // Se necessário, você pode ajustar o tempo de espera
                    // usando o método sleep do Python ou um comando de espera do Selenium
                    // para garantir que a página tenha tempo para expandir o volume
                    // e o próximo clique ocorra no momento certo.
                    // Exemplo: time.sleep(1) ou driver.implicitly_wait(1)
                }
            ''')
        except:
            pass
        
        try:
            WebDriverWait(driver, 3).until(EC.visibility_of_element_located((By.CLASS_NAME, "chapter-readmore")))
            driver.execute_script("document.querySelector('.chapter-readmore').click();")
        except:
            pass

        try:
            # Esperar a lista de capítulos carregar
            wait = WebDriverWait(driver, 10)
            lista_capitulos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sub-chap-list')))
        except:
            pass
        

        for sub_chap_list in lista_capitulos:
            capitulos = sub_chap_list.find_elements(By.CLASS_NAME, 'wp-manga-chapter')

            for capitulo in capitulos:
                # Obter o número do capítulo
                # Obter o número do capítulo do texto do link
                link_text = capitulo.find_element(By.TAG_NAME, 'a').text
                if link_text == '':
                    continue
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', link_text.replace(',', '')))

                # Obter o link do capítulo
                link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # Verificar se o capítulo está no intervalo desejado
                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
                    
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