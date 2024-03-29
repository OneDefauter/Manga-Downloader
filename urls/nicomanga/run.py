import os
import time
import shutil
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from colorama import Fore, Style

import src.organizar as organizar
import src.move as move

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
    
    if debug_var.get():
        baixando_label.config(text=f"Verificando capítulo {numero_capitulo}")
    
    # Injeta um script JavaScript para simular um pequeno movimento do mouse
    driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

    try:
        # <button type="button" data-dismiss="modal" id="close" class="btn btn-warning"><span class="glyphicon glyphicon-forward"></span> I Know</button>
        warning_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-warning"))
        )
        
        warning_btn.click()
    except:
        ...

    # Pega o tempo inicial
    tempo_inicial = datetime.now()

    # Define o limite de tempo em segundos (30 segundos no seu caso)
    limite_tempo_segundos = 30

    while True:
        janelas_abertas = driver.window_handles

        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            driver.close()
            janelas_abertas = driver.window_handles
            driver.switch_to.window(janelas_abertas[0])
            break
        else:
            tempo_atual = datetime.now()
            tempo_decorrido = tempo_atual - tempo_inicial

            if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                print("Tempo limite atingido. Saindo do loop.")
                return

    time.sleep(1)

    try:
        # <button type="button" data-dismiss="modal" id="close" class="btn btn-warning"><span class="glyphicon glyphicon-forward"></span> I Know</button>
        warning_btn = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "btn-warning"))
        )
        
        warning_btn.click()
    except:
        ...

    time.sleep(1)

    def load_images():
        count_repet = 0
        count_limit = 10

        while count_repet < count_limit:
            try:
                if debug_var.get():
                    baixando_label.config(text=f"Carregando capítulo {numero_capitulo}\nVerificação {count_repet + 1} / {count_limit}")

                # Espera até que o elemento do leitor esteja presente na página
                leitor = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "listImgs"))
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

            except Exception as e:
                print(f"Erro durante o carregamento de imagens: {e}")
                # Se ocorrer um erro, você pode querer tentar novamente ou lidar com a situação de outra maneira
    
    load_images()
    
    while True:
        # Espera até que o elemento do leitor esteja presente na página
        leitor = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "listImgs"))
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
            break
    
    # Cria uma instância de ActionChains
    actions = ActionChains(driver)

    # Simula a combinação de teclas Alt + W
    actions.key_down(Keys.ALT).send_keys('w').key_up(Keys.ALT).perform()
    
    time.sleep(1)
    
    janelas_abertas = driver.window_handles
    
    for _ in range(1, 10):
        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])    
            # Localiza o elemento span pelo texto usando XPath
            span_element = driver.find_element(By.XPATH, "//span[contains(text(), 'Não perguntar novamente')]")

            # Clica no botão usando execute_script
            driver.execute_script("arguments[0].click();", span_element)
            
            janelas_abertas = driver.window_handles
            driver.switch_to.window(janelas_abertas[0])
            break
        else:
            janelas_abertas = driver.window_handles
            time.sleep(0.5)
    
    # Localiza o elemento tyc-image-container usando XPath
    tyc_image_container = driver.find_element(By.XPATH, "//div[@class='tyc-image-container']")
    
    # Em seguida, localiza o elemento input dentro de tyc-image-container com a classe height-value-min
    height_value_min_input = tyc_image_container.find_element(By.XPATH, ".//input[@class='height-value-min']")

    # Define o valor para 500
    height_value_min_input.clear()  # Limpa qualquer valor existente no campo
    height_value_min_input.send_keys("500")
    time.sleep(0.5)
    actions.key_down(Keys.ENTER).perform()
    
    time.sleep(1)
    
    # Localiza o elemento checkbox usando XPath
    checkbox_element = driver.find_element(By.XPATH, "//input[@class='height-check img-check tyc-input-checkbox']")

    # Verifica se a checkbox está marcada
    if not checkbox_element.is_selected():
        # Marca a checkbox se não estiver marcada
        driver.execute_script("arguments[0].click();", checkbox_element)
    


    time.sleep(1)
    
    image_wrappers = tyc_image_container.find_elements(By.XPATH, "//div[contains(@class, 'tyc-img-item-container')]")
    
    count_limit = len(image_wrappers)
    count = 1
    count2 = 0
    
    while count2 < count_limit:
        if debug_var.get():
            baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nBaixando página: {count} / {links_count}")
        
        img_downloader = image_wrappers[count2].find_element(By.CLASS_NAME, "tyc-image-info-container")
        container_button = img_downloader.find_element(By.CLASS_NAME, "download-direct")
        driver.execute_script("arguments[0].click();", container_button)
        
        janelas_abertas = driver.window_handles
        
        for _ in range(1, 10):
            if len(janelas_abertas) != 1:
                driver.switch_to.window(janelas_abertas[-1])
                break
            else:
                janelas_abertas = driver.window_handles
                time.sleep(0.5)
        
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
        
        print(f"{Fore.GREEN}Baixando {imagem} como {count:02d}.png...{Style.RESET_ALL}")
        
        time.sleep(0.5)
        
        driver.close()
        
        janelas_abertas = driver.window_handles
        driver.switch_to.window(janelas_abertas[0])
        
        count += 1
        count2 += 1
    
    
    if debug_var.get():
        baixando_label.config(text=f"Arrumando páginas...")
        
    time.sleep(2)
    
    close = 0
    max_close = 60
    
    while close < max_close:
        lista = os.listdir(download_folder)
        
        if count == len(lista) + 1:
            if not ".crdownload" in lista:
                break
            
        time.sleep(1)
        close += 1
        
        if debug_var.get():
            baixando_label.config(text=f"Arrumando páginas...\nAguarde {close} / {max_close}")
    
    move.setup(download_folder, folder_path)
            
    organizar.organizar(folder_path, compactar, compact_extension, extension)

    if debug_var.get():
        baixando_label.config(text=f"Aguarde...")
        
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')

    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

