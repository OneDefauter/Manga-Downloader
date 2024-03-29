import os
import re
import time
import shutil
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from colorama import Fore, Style

import src.move as move
import src.organizar as organizar

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, app_instance, max_attent, max_verify):
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

    WebDriverWait(driver, 30).until(
            EC.visibility_of_element_located((By.CLASS_NAME, "images-container"))
        )
    
    time.sleep(3)
    
    # Encontra a div que contém as imagens
    div_images_container = driver.find_element(By.CLASS_NAME, 'images-container')

    # Encontra todas as tags de imagem dentro da div
    imagens = div_images_container.find_elements(By.CLASS_NAME, 'images')

    # Extrai os links das imagens
    links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]

    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
    
    def download_images(count, files):
        for imagem in links_das_imagens:
            if debug_var.get():
                baixando_label.config(text=f"Capítulo {numero_capitulo}\nBaixando página: {count} / {str(len(links_das_imagens))}")
                
            driver.get(imagem)
            
            try:
                input_element = WebDriverWait(driver, 10).until(
                    EC.visibility_of_element_located((By.CSS_SELECTOR, 'input[type="number"]'))
                )
            except:
                driver.get(imagem)
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
            
            time.sleep(0.2)
            
            attention = 0
            warning_img = 0
            while True:
                lista = os.listdir(download_folder)
                if len(lista) > files:
                    files += 1
                    break
                else:
                    if warning_img > max_attent:
                        print(f"{Fore.RED}Falha ao baixar {imagem} como {count:02d}.{file_extension}...{Style.RESET_ALL}")
                        break
                    elif attention < 1000:
                        attention += 1
                        time.sleep(0.1)
                        continue
                    else:
                        download_button.click()
                        attention = 0
                        warning_img += 1
                        continue
            count += 1
    
    download_images(1, 0)
    
    if debug_var.get():
        baixando_label.config(text=f"Arrumando páginas...")
        
    move.setup(download_folder, folder_path)
    
    organizar.organizar(folder_path, compactar, compact_extension, extension)

    if debug_var.get():
        baixando_label.config(text=f"Aguarde...")
    
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

