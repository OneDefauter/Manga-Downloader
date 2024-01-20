import os
import re
import time
import shutil
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style

import src.download as download
import src.organizar as organizar
import src.move as move

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, app_instance):
    folder_path = os.path.join(folder_selected, nome_foler, numero_capitulo)

    # Verificar se a pasta já existe e tem conteúdo
    contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

    print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

    if debug_var.get():
        baixando_label.config(text=f"Verificando pasta do capítulo {numero_capitulo}")
        
    if contents:
        print(f"{Fore.GREEN}INFO:{Style.RESET_ALL} a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
        for item in contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Exclui pasta e conteúdo
            else:
                os.remove(item_path)  # Exclui arquivo

    os.makedirs(folder_path, exist_ok=True)

    if debug_var.get():
        baixando_label.config(text=f"Aguardando página do capítulo {numero_capitulo}")

    driver.get(url)
    driver.implicitly_wait(10)

    time.sleep(2)
    
    verify1 = driver.find_element(By.XPATH, '/html/body/div/div')
    text = verify1.find_element(By.XPATH, '/html/body/div/div/div[2]').text
    if "Capítulo aguardando aprovação." in text:
        print("Capítulo aguardando aprovação.")
        return 4
    
    links_das_imagens = []
    count = 0
    
    # Espera o leitor carregar
    while True:
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.pagereader')))
        finally:
            break
    
    try:
        pop_up = driver.find_element(By.CLASS_NAME, 'el-dialog__close')
        pop_up.click()
    except:
        ...


    def button_mode(search, define):
        max_attempts = 3
        attempts = 0

        while attempts < max_attempts:
            try:
                # Aguarde até que o botão esteja presente na página usando XPath com base no texto
                xpath_expression = f"//button[@class='buttonreader pointer' and text()='{search}']"
                button_element = WebDriverWait(driver, 3).until(
                    EC.presence_of_element_located((By.XPATH, xpath_expression))
                )

                # Verifique o texto do botão
                button_text = button_element.text

                if button_text == search:
                    button_element.click()
                    
                    time.sleep(2)

                    try:
                        # Aguarde até que o botão esteja presente na página usando XPath com base no texto
                        xpath_expression = f"//button[@class='buttonreader pointer' and text()='{define}']"
                        button_element = WebDriverWait(driver, 5).until(
                            EC.presence_of_element_located((By.XPATH, xpath_expression))
                        )
                    except:
                        # Incrementar o contador de tentativas se o tempo de espera exceder
                        attempts += 1
                        continue
                    
                    else:
                        break

            except:
                # Incrementar o contador de tentativas se o tempo de espera exceder
                attempts += 1
                continue

    button_mode('Passar páginas', 'Páginas abertas')

    # Descobrir a quantidade de paginas
    elemento_lista_paginas = driver.find_element(By.CSS_SELECTOR, 'div[id^="el-popper-container-"] div:nth-child(2) div div div:nth-child(1) ul')
    itens_lista_paginas = elemento_lista_paginas.find_elements(By.CSS_SELECTOR, 'li')
    numero_ultima_pagina = int(len(itens_lista_paginas))

    button_mode('Páginas abertas', 'Passar páginas')

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    def load_images():
        count_repet = 0
        count_limit = 10
        
        while count_repet < count_limit:
            
            leitor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "manga-reader"))
            )

            imagens = leitor.find_elements(By.TAG_NAME, 'img')

            # Função para rolar até a imagem e aguardar o carregamento
            def scroll_to_image(image_element):
                driver.execute_script("arguments[0].scrollIntoView();", image_element)
                wait_time = 0
                while not image_element.get_attribute("complete") and wait_time < 10:
                    time.sleep(0.5)
                    wait_time += 1
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Itera sobre as imagens
            for imagem in imagens:
                scroll_to_image(imagem)

            count_repet += 1
            
        return imagens

    imagens = load_images()

    while True:
        if len(imagens) != numero_ultima_pagina:
            imagens = load_images()
        else:
            break

        while True:
            leitor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "manga-reader"))
            )
        
            paginas = driver.find_elements(By.XPATH, '//img[@class="pagereader" and @alt="Manga page"]')
            links_das_imagens = []
        
            # Função para rolar até a imagem e aguardar o carregamento
            def scroll_to_image(image_element):
                driver.execute_script("arguments[0].scrollIntoView();", image_element)
                wait_time = 0
                while not image_element.get_attribute("complete") and wait_time < 10:
                    time.sleep(1)
                    wait_time += 1
        
            # Itera sobre as imagens
            for imagem in paginas:
                scroll_to_image(imagem)
                
                # Aqui você pode adicionar o código para baixar a imagem ou qualquer outra ação desejada
                links_das_imagens.append(str(imagem.get_attribute('src')))
            
            # Extrai os links das imagens
            links_das_imagens = [link.strip() for link in links_das_imagens]
            links_count = str(len(links_das_imagens))
            
            if 'None' in links_das_imagens:
                load_images()
            else:
                break
            
    def download_images(count):
        for imagem in links_das_imagens:
            if debug_var.get():
                baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nBaixando página: {count} / {links_count}")
                
            driver.get(imagem)
            
            try:
                input_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="number"]'))
                )
            except:
                driver.refresh()
                time.sleep(1)
                
                input_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="number"]'))
                )
            
            input_element.clear()  # Limpa qualquer valor existente no campo
            input_element.send_keys(count)
            
            download_button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, "/html/body/button"))
            )
            download_button.click()
            
            # Remover parâmetros de consulta da URL
            parsed_url = urlparse(imagem)
            url_without_query = parsed_url.scheme + "://" + parsed_url.netloc + parsed_url.path

            # Encontrar a extensão do arquivo
            extension_match = re.search(r'\.(jpg|jpeg|png|gif|bmp|webp|avif)$', url_without_query, re.IGNORECASE)

            if extension_match:
                file_extension = extension_match.group(1)
            
            print(f"{Fore.GREEN}Baixando {imagem} como {count:02d}.{file_extension}...{Style.RESET_ALL}")
            
            time.sleep(0.5)
            
            count += 1
        
        return count
    
    count = download_images(1)
    
    if debug_var.get():
        baixando_label.config(text=f"Arrumando páginas...")
        
    time.sleep(2)
    
    while True:
        lista = os.listdir(download_folder)
        if count == len(lista) + 1:
            break
        
        else:
            for image in lista:
                image = os.path.join(download_folder, image)
                os.remove(image)
            
            count = download_images(1)

    move.setup(download_folder, folder_path)
            
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')
    
    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
    
    return 0

