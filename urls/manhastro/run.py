import os
import re
import time
import shutil
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
    
    def load_image():
        count_repet = 0
        count_save = 0
        paginas = [0]
        paginas_save = 0
        while count_repet < max_verify:
    
            if debug_var.get():
                baixando_label.config(text=f"Carregando capítulo {numero_capitulo}\nVerificação {count_repet + 1} / {max_verify}\nEncontrados {len(paginas)} imagens")
    
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
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                imagem = pagina.find_element(By.TAG_NAME, 'img')
                scroll_to_image0(imagem)
                
            count_repet += 1
            
            if len(paginas) != paginas_save:
                paginas_save = len(paginas)
                count_save += 1
                
            else:
                if count_save + 10 == count_repet:
                    break
    
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
        links_das_imagens = [link for link in links_das_imagens if "Aviso" not in link]
        
        def remove_duplicatas(lista):
            lista_sem_duplicatas = []
            [lista_sem_duplicatas.append(item) for item in lista if item not in lista_sem_duplicatas]
            return lista_sem_duplicatas
        
        links_das_imagens = remove_duplicatas(links_das_imagens)
        
        if 'None' in links_das_imagens:
            load_image()
        else:
            break
    
    def download_images(count, files):
        for imagem in links_das_imagens:
            if debug_var.get():
                baixando_label.config(text=f"Capítulo {numero_capitulo}\nBaixando página: {count} / {str(len(links_das_imagens))}")
            
            driver.switch_to.window(driver.window_handles[0])
            driver.execute_script(f"window.open('{imagem}', '_blank')")
            
            time.sleep(0.5)
            t = False
            
            while True:
                janelas_abertas = driver.window_handles

                if len(janelas_abertas) > 1:
                    driver.switch_to.window(janelas_abertas[-1])
                    break
                else:
                    # driver.execute_script("window.open('about:blank', '_blank');")
                    # driver.switch_to.window(driver.window_handles[-1])
                    # driver.close()
                    # driver.switch_to.window(driver.window_handles[0])
                    count += 1
                    t = True
                    print(f"{Fore.GREEN}Baixando {imagem}{Style.RESET_ALL}")
                    break
                
            if t:
                continue
                
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