import os
import shutil
from colorama import Fore, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import urls.download_methods.madara as madara

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
    
    try:
        # Espere até que o elemento com o id "pageloader" esteja presente no DOM
        elemento_pageloader = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.ID, "pageloader"))
        )
        # Verifique se o estilo "display: none;" está presente no atributo style
        WebDriverWait(driver, 10).until(
            lambda driver: "display: none;" in elemento_pageloader.get_attribute("style")
        )
    except:
        pass

    madara.setup(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, folder_path, app_instance, max_attent, max_verify)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
    

