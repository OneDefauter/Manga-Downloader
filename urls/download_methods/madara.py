import os
import re
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style

import src.organizar as organizar
import src.move as move


def setup(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, folder_path, app_instance):
    def load_image():
        count_repet = 0
        count_limit = 10
        
        while count_repet < count_limit:
    
            if debug_var.get():
                baixando_label.config(text=f"Carregando capítulo {numero_capitulo}\nVerificação {count_repet + 1} / {count_limit}")
    
            leitor = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "reading-content"))
            )
        
            paginas = leitor.find_elements(By.CLASS_NAME, 'page-break')
        
            # Função para rolar até a imagem e aguardar o carregamento
            def scroll_to_image0(image_element):
                driver.execute_script("arguments[0].scrollIntoView();", image_element)
                wait_time = 0
                while not image_element.get_attribute("complete") and wait_time < 10:
                    time.sleep(0.5)
                    wait_time += 1
        
            # Itera sobre as imagens
            for pagina in paginas:
                imagem = pagina.find_element(By.TAG_NAME, 'img')
                scroll_to_image0(imagem)
                
            count_repet += 1
        
    load_image()
    
    while True:
        leitor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "reading-content"))
        )
    
        paginas = leitor.find_elements(By.CLASS_NAME, 'page-break')
        links_das_imagens = []
    
        # Função para rolar até a imagem e aguardar o carregamento
        def scroll_to_image(image_element):
            driver.execute_script("arguments[0].scrollIntoView();", image_element)
            wait_time = 0
            while not image_element.get_attribute("complete") and wait_time < 10:
                time.sleep(1)
                wait_time += 1
    
        # Itera sobre as imagens
        for pagina in paginas:
            imagem = pagina.find_element(By.TAG_NAME, 'img')
            scroll_to_image(imagem)
            
            # Aqui você pode adicionar o código para baixar a imagem ou qualquer outra ação desejada
            links_das_imagens.append(str(imagem.get_attribute('src')))
        
        # Extrai os links das imagens
        links_das_imagens = [link.strip() for link in links_das_imagens]
        links_count = str(len(links_das_imagens))
        
        if 'None' in links_das_imagens:
            load_image()
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
            
            extension_match = re.search(r'\.(jpg|jpeg|png|gif|bmp|webp|avif)$', imagem, re.IGNORECASE)
            
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
            
    organizar.organizar(folder_path, compactar, compact_extension, extension)

    if debug_var.get():
        baixando_label.config(text=f"Aguarde...")
        
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')