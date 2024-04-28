import os
import re
import time
import shutil
from urllib.parse import urlparse
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from colorama import Fore, Style
from datetime import datetime

import src.organizar as organizar
import src.move as move
from src.zipfile import setup
import src.clean as clean

async def run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, app_instance, max_attent, max_verify):
    clean.setup(download_folder, False)
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

    if debug_var.get():
        baixando_label.config(text=f"Aguardando página do capítulo {numero_capitulo}")

    driver.get(url)

    try:
        dialog = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.CLASS_NAME, "fc-ab-root"))
        )
        driver.execute_script("arguments[0].remove();", dialog)
    except:
        pass
    
    try:
        verify1 = driver.find_element(By.XPATH, '/html/body/div/div')
        text = verify1.find_element(By.XPATH, '/html/body/div/div/div[2]').text
        if "Capítulo aguardando aprovação." in text:
            print("Capítulo aguardando aprovação.")
            return 4
    except:
        pass
    
    # Espera o leitor carregar
    attents = 1
    while True:
        try:
            WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'img.pagereader')))
            break
        except:
            if attents < max_attent:
                driver.refresh()
                attents += 1
            else:
                print(f"{Fore.RED}Nenhuma imagem encontrada{Style.RESET_ALL}")
                print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
                if debug_var.get():
                    baixando_label.config(text=f"Nenhuma imagem foi encontrada no capítulo {numero_capitulo}")
                return
    
    try:
        pop_up = driver.find_element(By.CSS_SELECTOR, 'button[aria-label="Close this dialog"]')
        pop_up.click()
    except:
        pass

    try:
        botao = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, "//button[text()='Páginas abertas']")) 
        )
        botao.click()
    except:
        pass
    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 2);")

    time.sleep(1)

    def load_images():
        count_repet = 0
        count_save = 0
        paginas = [0]
        paginas_save = 0
        while count_repet < max_verify:
            try:
                if debug_var.get():
                    baixando_label.config(text=f"Carregando capítulo {numero_capitulo}\nVerificação {count_repet + 1} / {max_verify}\nEncontrados {len(paginas)} imagens")

                # Espera até que o elemento do leitor esteja presente na página
                leitor = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "manga-reader"))
                )

                # Obtém todas as imagens dentro do leitor
                paginas = leitor.find_elements(By.TAG_NAME, 'img')

                # Função para rolar até a imagem e aguardar o carregamento
                def scroll_to_image(image_element):
                    driver.execute_script("arguments[0].scrollIntoView();", image_element)
                    wait_time = 0
                    while not image_element.get_attribute("complete") and wait_time < 10:
                        time.sleep(0.5)
                        wait_time += 1

                # Itera sobre as imagens
                for imagem in paginas:
                    scroll_to_image(imagem)

                count_repet += 1
            
                if len(paginas) != paginas_save:
                    paginas_save = len(paginas)
                    count_save += 1
                    
                else:
                    if count_save + 10 == count_repet:
                        break

            except Exception as e:
                print(f"Erro durante o carregamento de imagens: {e}")
                # Se ocorrer um erro, você pode querer tentar novamente ou lidar com a situação de outra maneira
    
    load_images()
    
    while True:
        # Espera até que o elemento do leitor esteja presente na página
        leitor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "manga-reader"))
        )

        # Obtém todas as imagens dentro do leitor
        paginas = leitor.find_elements(By.TAG_NAME, 'img')
        links_das_imagens = []

        # Função para rolar até a imagem e aguardar o carregamento
        def scroll_to_image(image_element):
            driver.execute_script("arguments[0].scrollIntoView();", image_element)
            wait_time = 0
            while not image_element.get_attribute("complete") and wait_time < 10:
                time.sleep(0.5)
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
            pagina = paginas[0]
            scroll_to_image(pagina)
            ActionChains(driver).move_to_element(pagina).perform()
            ActionChains(driver).send_keys('g').perform()
            break
    
    actions_menu = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "pv-gallery-head-command-others"))
    )

    # Clique no elemento "Ações" para abrir o menu suspenso
    actions_menu.click()

    # Agora, espere até que o elemento "Baixar todas as imagens" esteja visível no menu suspenso
    download_option = WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, ".pv-gallery-head-command-drop-list-item[data-command='downloadImage']"))
    )

    # Clique no elemento "Baixar todas as imagens"
    download_option.click()
    
    print(f"{Fore.YELLOW}Baixando capítulo {numero_capitulo}{Style.RESET_ALL}")
    
    if debug_var.get():
        baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

    attention = 0
    completo = False
    falhou = False
    limite_tempo_segundos = 300
    while True:
        tempo_inicial = datetime.now()
        while True:
            lista = os.listdir(download_folder)
            if len(lista) == 1:
                if lista[0].endswith('.zip'):
                    if debug_var.get():
                        baixando_label.config(text=f"Extraindo capítulo{numero_capitulo}")
                    print(f"{Fore.GREEN}Download concluído, extraindo...{Style.RESET_ALL}")
                    setup(download_folder)
                    completo = True
                    break
            else:
                tempo_atual = datetime.now()
                tempo_decorrido = tempo_atual - tempo_inicial

                if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                    if attention == max_attent:
                        falhou = True
                        break
                    else:
                        attention += 1
                        break
        if falhou:
            print(f"{Fore.RED}Falha ao baixar o capítulo {numero_capitulo}.{Style.RESET_ALL}")
            return
        if completo:
            print(f"{Fore.GREEN}Extração completa.{Style.RESET_ALL}")
            break
    
    print(f"{Fore.GREEN}Movendo imagens...{Style.RESET_ALL}")
    move.setup(download_folder, folder_path)

    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')
    
    if debug_var.get():
        baixando_label.config(text=f"Aguarde...")

    print(f"{Fore.GREEN}Organizando imagens...{Style.RESET_ALL}")
    organizar.organizar(folder_path, compactar, compact_extension, extension)

    print(f"{Fore.GREEN}Completo.{Style.RESET_ALL}")
    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
