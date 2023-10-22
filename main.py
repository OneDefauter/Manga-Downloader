import os
import re
import subprocess
import sys
import time
import requests
import win32api
import win32con
import shutil
import argparse
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

def is_imagick_installed():
    # Diretório onde procuraremos por pastas relacionadas ao ImageMagick
    program_files_path = r'C:\\Program Files'

    # Prefixo usado para identificar pastas do ImageMagick
    imagick_folder_prefix = 'ImageMagick'

    # Obtém uma lista de todas as pastas em C:\Program Files
    program_files_folders = [folder for folder in os.listdir(program_files_path)
                             if os.path.isdir(os.path.join(program_files_path, folder))]

    # Filtra as pastas que começam com o prefixo 'ImageMagick'
    imagick_folders = [folder for folder in program_files_folders if folder.startswith(imagick_folder_prefix)]

    # Verifica se cada pasta do ImageMagick contém o executável magick.exe
    for imagick_folder in imagick_folders:
        imagick_path = os.path.join(program_files_path, imagick_folder)
        magick_exe_path = os.path.join(imagick_path, 'magick.exe')
        
        # Se o executável magick.exe existir, consideramos o ImageMagick como instalado
        if os.path.isfile(magick_exe_path):
            return True

    # Se nenhum diretório do ImageMagick for encontrado, consideramos o ImageMagick não instalado
    return False

if not is_imagick_installed():
    print("ImageMagick não está instalado.\nBaixando e instalando o ImageMagick...")
    
    # URL do instalador do ImageMagick
    url = 'https://github.com/OneDefauter/Menu_/releases/download/Req/ImageMagick-7.1.1-21-Q16-HDRI-x64-dll.exe'

    installer_path = 'ImageMagick-Installer.exe'

    response = requests.get(url)
    with open(installer_path, 'wb') as f:
        f.write(response.content)

    # Instalar o ImageMagick usando subprocess
    subprocess.run([installer_path, '/VERYSILENT'])
        
    os.remove(installer_path)
    print("ImageMagick instalado com sucesso.")
    
    sys.exit()

# Lista de agregadores
lista_agregadores = ["BR Mangás", "Crystal Scan"]

def initialize_driver(browser="chrome", headless=True):
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--no-sandbox')
        return webdriver.Chrome(options=chrome_options)
    else:
        raise ValueError("Navegador não suportado")

# Configuração do parser para argumentos de linha de comando
parser = argparse.ArgumentParser(description="Mangá Downloader")
parser.add_argument("-nh", "--no-headless", action="store_true", help="Executar o Selenium em modo não headless")
parser.add_argument("-a", "--agregador", type=int, choices=range(1, len(lista_agregadores) + 1), help="Número do agregador")
parser.add_argument("-n", "--nome", type=str, help="Nome da obra")
parser.add_argument("-c", "--capitulo", type=float, help="Número do capítulo")
parser.add_argument("-t", "--ate", type=float, help="Até qual capítulo baixar")

args = parser.parse_args()

# Inicialização do driver após a análise dos argumentos
driver = initialize_driver("chrome", not args.no_headless)

os.system("cls")

# Se o argumento do agregador foi fornecido
if args.agregador:
    agregador_escolhido = args.agregador
else:
    # Se não foi fornecido, solicite ao usuário que escolha
    print("Escolha um agregador de mangás:")
    for i, agregador in enumerate(lista_agregadores, start=1):
        print(f"[{i}] - {agregador}")

    agregador_escolhido = int(input("\nDigite o número do agregador desejado: "))
    os.system("cls")

# Se o argumento do nome da obra foi fornecido
nome = args.nome if args.nome else input("Digite o nome da obra: ")
nome_formatado = nome.replace(" ", "-").replace("’", "").replace("'", "").lower()

# Se o argumento do número do capítulo for fornecido e o argumento do até qual capítulo baixar não for fornecido
if args.capitulo and not args.ate:
    capítulo = args.capitulo
    ate = capítulo
    
# Se o argumento do até qual capítulo baixar for fornecido e o argumento do número do capítulo não for fornecido
elif args.ate and not args.capitulo:
    ate = args.ate
    capítulo = ate
else:
    # Se o argumento do número do capítulo foi fornecido
    capítulo = args.capitulo if args.capitulo else float(input("Digite o número do capítulo: "))

    # Se o argumento do até qual capítulo baixar foi fornecido
    ate = args.ate if args.ate else float(input("Digite até qual capítulo deseja baixar (pressione Enter para usar o mesmo valor do capítulo): ") or capítulo)







async def download(link, folder_path, session, max_attempts=10, sleep_time=5):
    attempts = 0
    while attempts < max_attempts:
        try:
            image_name = link.split("/")[-1]
            image_path = os.path.join(folder_path, image_name)

            # Aguardar um tempo antes de fazer o download
            await asyncio.sleep(2)

            async with session.get(link) as response:
                # Verificar se a resposta tem status 200 (OK)
                if response.status == 200:
                    print(f"Baixando {link}...")

                    # Salvar a imagem no disco
                    with open(image_path, "wb") as f:
                        f.write(await response.read())

                    # Se chegou até aqui, o download foi bem-sucedido, então saia do loop
                    break
                else:
                    print(f"Tentativa {attempts + 1} - Erro ao baixar {link}. Status code: {response.status}")
                    # Aguardar um tempo antes de tentar novamente
                    await asyncio.sleep(sleep_time)

        except Exception as e:
            print(f"Tentativa {attempts + 1} - Erro ao baixar {link}: {e}")

        # Incrementar o número de tentativas
        attempts += 1

    # Se chegou aqui, significa que atingiu o número máximo de tentativas sem sucesso
    if attempts == max_attempts:
        print(f"Atenção: Não foi possível baixar {link} após {max_attempts} tentativas.")



def organizar(folder_path):
    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    count = 1

    for filename in file_list:
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}__{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    for filename in file_list:
        base, ext = os.path.splitext(filename)
        new_filename = f"{count:02d}{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        count += 1



    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

    input_images = [os.path.join(folder_path, image) for image in image_files]
    output_folder = os.path.join(folder_path, "temp")

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    atributos_atuais = win32api.GetFileAttributes(output_folder)
    win32api.SetFileAttributes(output_folder, atributos_atuais | win32con.FILE_ATTRIBUTE_HIDDEN)



    output_filename = os.path.join(output_folder, f"0.jpg")
    command = ["magick", "convert", "-quality", "100", "-crop", f"32000x5000"]

    command += input_images + [output_filename]

    subprocess.run(command, check=True)

    for image_file in input_images:
        os.remove(image_file)

    # Contador para numerar os arquivos
    count = 1

    output_files = sorted([f for f in os.listdir(output_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    for filename in output_files:
        base, ext = os.path.splitext(filename)
        new_filename = f"{count:02d}{ext}"
        os.rename(os.path.join(output_folder, filename), os.path.join(output_folder, new_filename))
        count += 1

    output_files = [f for f in os.listdir(output_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
    for image in output_files:
        output_pathfile = os.path.join(output_folder, image)
        shutil.move(output_pathfile, folder_path)

    # shutil.move(output_filename, folder_path)
    output_folder2 = os.path.join(folder_path, "temp")
    os.removedirs(output_folder2)



async def main():
    
    print("\nAguarde...")
    
    if agregador_escolhido == 1:
        base_url = 'https://www.brmangas.net/ler/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"https://www.brmangas.net/manga/{nome_formatado}-online/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    sys.exit()
            
            # Esperar a lista de capítulos carregar
            capitulos = driver.find_elements(By.XPATH, '//div[@class="lista_manga"]//li[@class="row lista_ep"]')

            capitulos_encontrados = []
            
            os.system("cls")
            print("Verificando capítulos...")

            for capitulo in capitulos:
                numero_capitulo = float(capitulo.get_attribute('data-cap'))
                if inicio <= numero_capitulo <= fim:
                    link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            sys.exit()

        def mudar():
            # Localiza o elemento do menu suspenso pelo ID
            select_modo_leitura = driver.find_element(By.ID, 'modo_leitura')

            # Cria um objeto Select para interagir com o menu suspenso
            modo_leitura_dropdown = Select(select_modo_leitura)

            # Obtém o valor atual do modo de leitura
            modo_atual = modo_leitura_dropdown.first_selected_option.get_attribute('value')

            print(f'Modo atual de leitura: {modo_atual}')

            # Verifica se o modo atual é o desejado (por exemplo, 'Páginas abertas')
            if modo_atual != '2':
                # Seleciona a opção desejada ('Páginas abertas')
                modo_leitura_dropdown.select_by_value('2')  # Troque '2' pelo valor da opção desejada

                # Espera até que o novo conteúdo seja carregado após a seleção
                driver.implicitly_wait(10)
                
                print("Modo de leitura alterado para: Páginas abertas")

                time.sleep(3)

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")
            
            if contents:
                print(f"A pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(1)

            mudar()

            # Agora você pode encontrar a div que contém as imagens
            div_imagens = driver.find_element(By.ID, 'images_all')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session) for link in links_das_imagens]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path)
            
            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.close()





    if agregador_escolhido == 2:
        base_url = 'https://crystalscan.net/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"https://crystalscan.net/manga/{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    sys.exit()
            
            # Injeta um script JavaScript para simular um pequeno movimento do mouse
            driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

            # Aguarde até que o botão seja visível (você pode ajustar o tempo de espera conforme necessário)
            try:
                element = WebDriverWait(driver, 5).until(
                    EC.visibility_of_element_located((By.CLASS_NAME, "chapter-readmore"))
                )

                # Clique no botão
                element.click()

            except TimeoutException:
                # print("O botão não está presente ou não é visível. Ignorando o clique.")
                pass
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")

            # Esperar a lista de capítulos carregar
            chapter_elements = driver.find_elements(By.CLASS_NAME, "wp-manga-chapter")

            capitulos_encontrados = []

            for capitulo in chapter_elements:
                # Encontra o elemento 'a' dentro do 'li'
                a_element = capitulo.find_element(By.TAG_NAME, "a")

                # Obtém o texto do número do capítulo
                # Usa expressão regular para extrair números, pontos e vírgulas
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', a_element.text.strip()))

                if inicio <= numero_capitulo <= fim:
                    link = a_element.get_attribute("href")
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"A pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(1)

            scroll_increment = 500
            total_height = driver.execute_script("return Math.max( document.body.scrollHeight, document.body.offsetHeight, document.documentElement.clientHeight, document.documentElement.scrollHeight, document.documentElement.offsetHeight);")

            while scroll_increment < total_height:
                driver.execute_script(f"window.scrollBy(0, {scroll_increment});")
                scroll_increment += 500
                time.sleep(1)  # Aguarda um segundo entre rolagens para dar tempo à página de carregar

            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.CLASS_NAME, 'reading-content')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('data-src') for imagem in imagens]
            links_das_imagens = [link.strip() for link in links_das_imagens]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session) for link in links_das_imagens]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path)

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.close()





# Executar o loop de eventos do asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
