import os
import time
import shutil
import asyncio
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from colorama import Fore, Style

import src.download as download
import src.organizar as organizar

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, app_instance, extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']):
    folder_path = os.path.join(folder_selected, nome_foler, numero_capitulo)

    # Verificar se a pasta já existe e tem conteúdo
    contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

    print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

    if contents:
        print(f"{Fore.GREEN}INFO:{Style.RESET_ALL} a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
        for item in contents:
            item_path = os.path.join(folder_path, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)  # Exclui pasta e conteúdo
            else:
                os.remove(item_path)  # Exclui arquivo

    os.makedirs(folder_path, exist_ok=True)

    driver.get(url)
    
    # Localize o elemento select
    select_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div/div/div/div/div[1]/div[1]/div/div[2]/div[2]/label/select")
    
    # Crie um objeto Select
    select = Select(select_element)
    select.select_by_visible_text("Estilo lista")
        
    time.sleep(5)
    
    # Função para realizar a rolagem até determinado ponto
    def scroll_to_position(position):
        script = f"window.scrollTo(0, document.body.scrollHeight * {position});"
        driver.execute_script(script)
        time.sleep(0.750)
    
    # Rolar até o final da página e esperar
    scroll_to_position(1)
    
    # Rolar até o início da página e esperar
    scroll_to_position(0)
    
    # Rolar até 25% da página e esperar
    scroll_to_position(0.25)
    
    # Rolar até o final da página e esperar
    scroll_to_position(1)
    
    # Rolar até o início da página e esperar
    scroll_to_position(0)
    
    # Rolar até 50% da página e esperar
    scroll_to_position(0.5)
    
    # Rolar até o final da página e esperar
    scroll_to_position(1)
    
    # Rolar até o início da página e esperar
    scroll_to_position(0)
    
    # Rolar até 75% da página e esperar
    scroll_to_position(0.75)
    
    # Rolar até o final da página e esperar
    scroll_to_position(1)
    
    # Rolar até o início da página e esperar
    scroll_to_position(0)
    
    # Encontra a div que contém as imagens
    div_imagens = driver.find_element(By.CLASS_NAME, 'reading-content')

    # Encontra todas as tags de imagem dentro da div
    imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

    # Extrai os links das imagens
    links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
    links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
    links_das_imagens = [link for link in links_das_imagens if link is not None]
    links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

    # Criar lista de tarefas assíncronas para o download
    tasks = [download.download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

    # Agendar as tarefas para execução simultânea
    await asyncio.gather(*tasks)
            
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')

    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

