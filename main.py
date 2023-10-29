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
import zipfile
from urllib.parse import urlparse, urlunparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions

os.system("cls")

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



def initialize_driver(browser="chrome", headless=True):
    if browser.lower() == "chrome":
        chrome_options = Options()
        if headless:
            chrome_options.add_argument("--headless")
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--no-sandbox')
        if agregador_escolhido not in carregar_imagens:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
        return webdriver.Chrome(options=chrome_options)
    else:
        raise ValueError("Navegador não suportado")



# Lista de agregadores como um dicionário
dic_agregadores = {
    "BR Mangás": "https://www.brmangas.net/",
    "Crystal Scan": "https://crystalscan.net/",
    "Argos Comics": "https://argoscomics.com/",
    "Argos Hentai": "https://argoshentai.com/",
    "Mangás Chan": "https://mangaschan.net/",
    "Ler Mangá": "https://lermanga.org/",
    "Tsuki": "https://tsuki-mangas.com/",
    "YomuMangás": "https://yomumangas.com/",
    "SlimeRead": "https://slimeread.com/",
    "Flower Manga": "https://flowermanga.com/",
    "Ler Manga Online": "https://lermangaonline.com.br/",
    "Manga BR": "https://mangabr.net/",
    "Projeto Scanlator": "https://projetoscanlator.com/",
}

precisa_url = [
    "Tsuki",
    "YomuMangás",
    "SlimeRead",
]

carregar_imagens = [
    "Tsuki",
]

compactar = [
    "CBZ",
    "RAR",
    "ZIP",
]

# Configuração do parser para argumentos de linha de comando
parser = argparse.ArgumentParser(description="Mangá Downloader")
parser.add_argument("-nh", "--no-headless", action="store_true", help="Executar o Selenium em modo não headless")
parser.add_argument("-a", "--agregador", type=int, choices=dic_agregadores.keys(), help="Nome do agregador")
parser.add_argument("-n", "--nome", type=str, help="Nome da obra")
parser.add_argument("-c", "--capitulo", type=float, help="Número do capítulo")
parser.add_argument("-t", "--ate", type=float, help="Até qual capítulo baixar")

args = parser.parse_args()

def print_log(title, details=None):
    box_width = 100
    title = f'► {title} ◄'.center(box_width - 2)  # Ajuste manual do espaçamento
    
    print('╔' + '═' * (box_width - 2) + '╗')
    print(f'║{title}║')
    
    if details:
        for detail in details:
            print(f'║ {detail:<{box_width-4}} ║')  # Ajuste para exibir detalhes
    
    print('╚' + '═' * (box_width - 2) + '╝')

# Se o argumento do agregador foi fornecido
if args.agregador:
    agregador_escolhido = args.agregador
    agregador_escolhido = list(dic_agregadores.keys())[agregador_escolhido - 1]
    print_log(f'Agregador escolhido: {agregador_escolhido}')
else:
    # Se não foi fornecido, solicite ao usuário que escolha
    print("Sites disponíveis:")
    for i, (agregador, link) in enumerate(dic_agregadores.items(), start=1):
        print(f"[{i}] - {agregador} ({link})")

    escolha_numero = int(input("\nDigite o número do agregador desejado: "))
    agregador_escolhido = list(dic_agregadores.keys())[escolha_numero - 1]
    os.system("cls")
    
    # Exibir o nome escolhido usando a função personalizada
    print_log(f'Agregador escolhido: {agregador_escolhido}')

# Se o argumento do nome da obra foi fornecido
nome = args.nome if args.nome else input("Digite o nome da obra: ")
os.system("cls")
print_log(f'Agregador escolhido: {agregador_escolhido}', [f'Obra escolhida: {nome}'])

nome_foler = nome.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "")
nome_formatado = nome.replace(" ", "-").replace("’", "").replace("'", "").replace(" – ", "").lower()

# Se o argumento do número do capítulo for fornecido e o argumento do até qual capítulo baixar não for fornecido
if args.capitulo and not args.ate:
    capítulo = args.capitulo
    ate = capítulo
    os.system("cls")
    print_log(f'Agregador escolhido: {agregador_escolhido}', [f'Obra escolhida: {nome}', f'Capítulo escolhido: {str(capítulo).replace(".0", "")}', f'Até qual capítulo baixar: {str(ate).replace(".0", "")}'])
    
# Se o argumento do até qual capítulo baixar for fornecido e o argumento do número do capítulo não for fornecido
elif args.ate and not args.capitulo:
    ate = args.ate
    capítulo = ate
    os.system("cls")
    print_log(f'Agregador escolhido: {agregador_escolhido}', [f'Obra escolhida: {nome}', f'Capítulo escolhido: {str(capítulo).replace(".0", "")}', f'Até qual capítulo baixar: {str(ate).replace(".0", "")}'])

else:
    # Se o argumento do número do capítulo foi fornecido
    capítulo = args.capitulo if args.capitulo else float(input("Digite o número do capítulo: "))
    os.system("cls")
    print_log(f'Agregador escolhido: {agregador_escolhido}', [f'Obra escolhida: {nome}', f'Capítulo escolhido: {str(capítulo).replace(".0", "")}'])


    # Se o argumento do até qual capítulo baixar foi fornecido
    ate = args.ate if args.ate else float(input("Digite até qual capítulo deseja baixar (pressione Enter para usar o mesmo valor do capítulo): ") or capítulo)
    os.system("cls")
    print_log(f'Agregador escolhido: {agregador_escolhido}', [f'Obra escolhida: {nome}', f'Capítulo escolhido: {str(capítulo).replace(".0", "")}', f'Até qual capítulo baixar: {str(ate).replace(".0", "")}'])



print("Compactar:")
print("[1] - Não")
print("[2] - Sim")
try:
    compact_1 = int(input("\nQuer compactar: "))
except Exception:
    compact_1 = 1

if compact_1 == 1:
    compact_1 = "Não"
elif compact_1 == 2:
    compact_1 = "Sim"
else:
    compact_1 = "Não"


os.system("cls")
print_log(
    f'Agregador escolhido: {agregador_escolhido}', 
    [
        f'Obra escolhida: {nome}',
        f'Capítulo escolhido: {str(capítulo).replace(".0", "")}',
        f'Até qual capítulo baixar: {str(ate).replace(".0", "")}',
        f'Compactar: {compact_1}'
    ]
)

if compact_1 == "Sim":
    print("Tipo de compactação:")
    print("[1] - CBZ")
    print("[2] - ZIP")
    try:
        compact_2 = int(input("\nDigite o número do tipo de compactação: "))
    except Exception:
        compact_2 = 1
    
    if compact_2 == 1:
        compact = "CBZ"
    elif compact_2 == 2:
        compact = "ZIP"
    else:
        compact = "CBZ"

os.system("cls")   
print_log(
    f'Agregador escolhido: {agregador_escolhido}', 
    [
        f'Obra escolhida: {nome}',
        f'Capítulo escolhido: {str(capítulo).replace(".0", "")}',
        f'Até qual capítulo baixar: {str(ate).replace(".0", "")}',
        f'Compactar: {compact_1}',
        f'Tipo de compactação: {compact}'
    ]
)


# Precisa de URL
if agregador_escolhido in precisa_url:
    url = str(input("Digite a URL da obra: "))
    
    if not dic_agregadores[agregador_escolhido] in url:
        print("Erro: URL inválida.")
        sys.exit()
    os.system("cls")
    print_log(f'Agregador escolhido: {agregador_escolhido}', [f'Obra escolhida: {nome}', f'Capítulo escolhido: {str(capítulo).replace(".0", "")}', f'Até qual capítulo baixar: {str(ate).replace(".0", "")}', f'URL da obra: {url}'])




# Extensões permitidas
extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']





async def download(link, folder_path, session, counter, max_attempts=10, sleep_time=5):
    attempts = 0
    while attempts < max_attempts:
        try:
            image_extension = link.split(".")[-1]
            image_name = f"{counter:02d}.{image_extension}"
            image_path = os.path.join(folder_path, image_name)

            # Aguardar um tempo antes de fazer o download
            await asyncio.sleep(2)

            async with session.get(link) as response:
                # Verificar se a resposta tem status 200 (OK)
                if response.status == 200:
                    print(f"Baixando {link} como {image_name}...")
                    
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



def organizar(folder_path, nome, numero_capitulo):
    # Verifique se há arquivos de imagem na pasta
    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))]

    if not image_files:
        print("Capítulo sem imagem.")
        # Excluir pasta se estiver vazia
        shutil.rmtree(folder_path)
        return
    
    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    count = 1

    for filename in file_list:
        base, ext = os.path.splitext(filename)
        new_filename = f"{base}__{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))

    file_list = sorted([f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    for filename in file_list:
        base, ext = os.path.splitext(filename)
        new_filename = f"{count:02d}{ext}"
        os.rename(os.path.join(folder_path, filename), os.path.join(folder_path, new_filename))
        count += 1



    image_files = [f for f in os.listdir(folder_path) if f.lower().endswith(tuple(extensoes_permitidas))]

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

    output_files = sorted([f for f in os.listdir(output_folder) if f.lower().endswith(tuple(extensoes_permitidas))], key=lambda x: [int(c) if c.isdigit() else c for c in re.split(r'(\d+)', x)])

    for filename in output_files:
        base, ext = os.path.splitext(filename)
        new_filename = f"{count:02d}{ext}"
        os.rename(os.path.join(output_folder, filename), os.path.join(output_folder, new_filename))
        count += 1

    output_files = [f for f in os.listdir(output_folder) if f.lower().endswith(tuple(extensoes_permitidas))]
    for image in output_files:
        output_pathfile = os.path.join(output_folder, image)
        shutil.move(output_pathfile, folder_path)

    # shutil.move(output_filename, folder_path)
    output_folder2 = os.path.join(folder_path, "temp")
    os.removedirs(output_folder2)
    
    if compact_1 == "Sim":
        if compact == "CBZ":
            if os.path.exists(f'{folder_path}.cbz'):
                os.remove(f'{folder_path}.cbz')
            with zipfile.ZipFile(f'{folder_path}.cbz', 'w') as zipf:
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.jpg'):
                        zipf.write(os.path.join(folder_path, file_name), file_name)
            shutil.rmtree(folder_path)
        elif compact == "ZIP":
            if os.path.exists(f'{folder_path}.zip'):
                os.remove(f'{folder_path}.zip')
            with zipfile.ZipFile(f'{folder_path}.zip', 'w') as zipf:
                for file_name in os.listdir(folder_path):
                    if file_name.endswith('.jpg'):
                        zipf.write(os.path.join(folder_path, file_name), file_name)
            shutil.rmtree(folder_path)



async def main():
    # Inicialização do driver após a análise dos argumentos
    driver = initialize_driver("chrome", not args.no_headless)
    
    print("\nAguarde...")
    
    # Num 01
    if "BR Mangás" in agregador_escolhido:
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
                
                if not "brmangas" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
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
            driver.quit()
            sys.exit(0)

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
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")
            
            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
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
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)
            
            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 02
    elif "Crystal Scan" in agregador_escolhido:
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
                
                if not "crystalscan" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
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
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
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

            # Função para realizar a rolagem até determinado ponto
            def scroll_to_position(position):
                script = f"window.scrollTo(0, document.body.scrollHeight * {position});"
                driver.execute_script(script)
                time.sleep(2)
            
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
            links_das_imagens = [imagem.get_attribute('data-src') for imagem in imagens]
            links_das_imagens = [link.strip() for link in links_das_imagens]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 03
    elif "Argos Comics" in agregador_escolhido:
        base_url = 'https://argoscomics.com/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"https://argoscomics.com/manga/{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "argoscomics" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
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

            try:
                # Localizar todos os elementos que têm a classe 'has-child'
                volumes_com_child = driver.find_elements(By.CLASS_NAME, 'has-child')

                # Expandir todos os volumes
                for volume in volumes_com_child:
                    volume.click()
                    time.sleep(1)
                    # Aguarde a expansão do volume
                    # wait.until(EC.presence_of_element_located((By.XPATH, f'{volume}/following-sibling::ul')))

            except TimeoutException:
                pass
            
            time.sleep(5)

            # Esperar a lista de capítulos carregar
            wait = WebDriverWait(driver, 10)
            lista_capitulos = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sub-chap-list')))

            # Selecionar os elementos de capítulo
            lista_capitulos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sub-chap-list')))

            capitulos_encontrados = []

            for sub_chap_list in lista_capitulos:
                capitulos = sub_chap_list.find_elements(By.CLASS_NAME, 'wp-manga-chapter')

                for capitulo in capitulos:
                    # Obter o número do capítulo
                    # Obter o número do capítulo do texto do link
                    link_text = capitulo.find_element(By.TAG_NAME, 'a').text
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', link_text.replace(',', '')))

                    # Obter o link do capítulo
                    link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    # Verificar se o capítulo está no intervalo desejado
                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(5)
            
            # Encontra a div que contém as imagens
            div_reading_content = driver.find_element(By.CLASS_NAME, 'reading-content')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_reading_content.find_elements(By.CLASS_NAME, 'wp-manga-chapter-img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 04
    elif "Argos Hentai" in agregador_escolhido:
        base_url = 'https://argoshentai.com/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"https://argoshentai.com/manga/{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "argoshentai" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
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

            try:
                # Localizar todos os elementos que têm a classe 'has-child'
                volumes_com_child = driver.find_elements(By.CLASS_NAME, 'has-child')

                # Expandir todos os volumes
                for volume in volumes_com_child:
                    volume.click()
                    time.sleep(1)
                    # Aguarde a expansão do volume
                    # wait.until(EC.presence_of_element_located((By.XPATH, f'{volume}/following-sibling::ul')))

            except TimeoutException:
                pass
            
            time.sleep(5)

            # Esperar a lista de capítulos carregar
            wait = WebDriverWait(driver, 10)
            lista_capitulos = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'sub-chap-list')))

            # Selecionar os elementos de capítulo
            lista_capitulos = wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'sub-chap-list')))

            capitulos_encontrados = []

            for sub_chap_list in lista_capitulos:
                capitulos = sub_chap_list.find_elements(By.CLASS_NAME, 'wp-manga-chapter')

                for capitulo in capitulos:
                    # Obter o número do capítulo
                    # Obter o número do capítulo do texto do link
                    link_text = capitulo.find_element(By.TAG_NAME, 'a').text
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', link_text.replace(',', '')))

                    # Obter o link do capítulo
                    link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')

                    # Verificar se o capítulo está no intervalo desejado
                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(5)
            
            # Encontra a div que contém as imagens
            div_reading_content = driver.find_element(By.CLASS_NAME, 'reading-content')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_reading_content.find_elements(By.CLASS_NAME, 'wp-manga-chapter-img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 05
    elif "Mangás Chan" in agregador_escolhido:
        base_url = 'https://mangaschan.net/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"https://mangaschan.net/manga/{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "mangaschan" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
            
            os.system("cls")
            print("Verificando capítulos...")

            time.sleep(2)

            capitulos = driver.find_elements(By.XPATH, '//div[@class="eplister"]//li')

            capitulos_encontrados = []

            for capitulo in capitulos:
                numero_capitulo = float(capitulo.get_attribute('data-num'))
                if inicio <= numero_capitulo <= fim:
                    link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)
            
            time.sleep(5)
            
            # Injeta um script JavaScript para simular um pequeno movimento do mouse
            driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

            time.sleep(5)
            
            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/article/div[3]')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None]
            links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 06
    elif "Ler Mangá" in agregador_escolhido:
        base_url = 'https://lermanga.org/mangas/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"https://lermanga.org/mangas/{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            lista_capitulos = driver.find_elements(By.CLASS_NAME, "single-chapter")
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "lermanga" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()

            elif len(lista_capitulos) == 0:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "lermanga" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")
            
            lista_capitulos = driver.find_elements(By.CLASS_NAME, "single-chapter")

            capitulos_encontrados = []

            for capitulo in lista_capitulos:
                # Obter o número do capítulo
                # Obter o número do capítulo do texto do link
                link_text = capitulo.find_element(By.TAG_NAME, 'a').text
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', link_text.replace(',', '')))

                # Obter o link do capítulo
                link = capitulo.find_element(By.TAG_NAME, 'a').get_attribute('href')

                # Verificar se o capítulo está no intervalo desejado
                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(2)
            
            # Seleciona o modo "Modo Scroll"
            select_element = Select(driver.find_element(By.ID, 'slch'))
            select_element.select_by_value('2')

            # Aguarde um pouco após a seleção (opcional)
            time.sleep(1)

            driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

            time.sleep(1)

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
            div_imagens = driver.find_element(By.CLASS_NAME, 'reader-area')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 07
    elif "Tsuki" in agregador_escolhido:
        base_url = 'https://tsuki-mangas.com/obra/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            global url
            # url = f"https://tsuki-mangas.com/obra/{nome_formatado}/"
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print("Erro: URL inválida. Status code: 404")
                driver.quit()
                sys.exit()
            
            time.sleep(5)
            
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            count = 2
            
            # Loop para percorrer todas as páginas
            while True:
                # Localiza os elementos que contêm as informações dos capítulos
                chapter_elements = driver.find_elements(By.CSS_SELECTOR, '.cardchapters')

                # Extrai os dados dos capítulos
                for chapter_element in chapter_elements:
                    chapter_number = chapter_element.find_element(By.CSS_SELECTOR, 'a').text
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))

                    if inicio <= numero_capitulo <= fim:
                        chapter_link = chapter_element.find_element(By.CSS_SELECTOR, 'a').get_attribute('href')
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

                # Tenta clicar no botão de próxima página
                try:
                    next_page_button = driver.find_element(By.XPATH, '//li[@class="page-item"]/a[@class="page-link" and contains(text(), ">")]')
                    next_page_button.click()
                except:
                    # Se não houver mais próxima página, sai do loop
                    break
                
                count += 1
                # Aguarde um pouco para garantir que a próxima página seja totalmente carregada
                time.sleep(5)

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(5)
            
            verify1 = driver.find_element(By.XPATH, '/html/body/div/div')
            text = verify1.find_element(By.XPATH, '/html/body/div/div/div[2]').text
            if "Capítulo aguardando aprovação." in text:
                print("Capítulo aguardando aprovação.")
                driver.quit()
                sys.exit()
            
            # Encontrar o elemento <select>
            select_element = driver.find_element(By.CSS_SELECTOR, '.contents select.selectreader')

            # Obter todas as opções dentro do <select>
            options = select_element.find_elements(By.TAG_NAME, 'option')

            links_das_imagens = []

            # Iterar sobre cada opção
            for option in options:
                # Obter o valor do atributo 'value' e converter para inteiro
                valor_da_opcao = int(option.get_attribute('value'))

                # Simular a seleção da opção
                option.click()

                time.sleep(5)

                div_imagens = driver.find_element(By.XPATH, '/html/body/div/div')
                imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

                links_das_imagens += [imagem.get_attribute('src') for imagem in imagens]

            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None]
            links_das_imagens = [urlunparse(urlparse(url)._replace(query='')) for url in links_das_imagens]
            
            if len(links_das_imagens) == 0:
                print("Nenhuma imagem encontrada")
                driver.quit()
                sys.exit() 

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 08
    elif "YomuMangás" in agregador_escolhido:
        base_url = 'https://yomumangas.com/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            driver.get(base_url)
            
            # url = f"https://yomumangas.com/manga/{nome_formatado}/"
            url = str(input("Digite a URL da obra: "))
            if not "yomumangas" in url:
                print("Erro: URL inválida. Status code: 404")
                driver.quit()
                sys.exit()
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print("Erro: URL inválida. Status code: 404")
                driver.quit()
                sys.exit()
            
            time.sleep(5)
            
            for _ in range(3):
                script = 'document.querySelector(\'button[title="Alterar a quantidade de capítulos a vista"]\').click();'
                driver.execute_script(script)
                time.sleep(1)  # Aguarde um pouco entre os cliques se necessário
            
            os.system("cls")
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            count = 2

            # Loop para percorrer todas as páginas
            while True:
                # Localiza os elementos que contêm as informações dos capítulos
                chapter_elements = driver.find_elements(By.CSS_SELECTOR, '[class^="styles_Chapters__"]')

                # Extrai os dados dos capítulos
                for element in chapter_elements:
                    for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                        chapter_number = sub.find_element(By.CSS_SELECTOR, 'h4').text
                        numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                        chapter_link = sub.get_attribute('href')

                        if inicio <= numero_capitulo <= fim:
                            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

                # Tenta clicar no botão de próxima página
                try:
                    # Tenta clicar no botão de próxima página e verifica se há mais páginas
                    next_page_button_script = 'var button = document.querySelector(\'button[title="Próxima Página"]\'); if (button && !button.hasAttribute("disabled")) { button.click(); return true; } else { return false; }'
                    result = driver.execute_script(next_page_button_script)

                    # Se não houver mais próxima página, sai do loop
                    if not result:
                        break
                    
                    print(f"Carregando página... {count}")
                    
                except:
                    # Se não houver mais próxima página, sai do loop
                    print("Não há mais próxima página.")
                    break
                
                count += 1
                # Aguarde um pouco para garantir que a próxima página seja totalmente carregada
                time.sleep(5)

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)

        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(5)
            
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(2)
            
            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.CSS_SELECTOR, '[class^="styles_Pages__"]')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None and link.startswith('http')]

            if len(links_das_imagens) == 0:
                print("Nenhuma imagem encontrada")
                driver.quit()
                sys.exit() 
            
            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 09
    elif "SlimeRead" in agregador_escolhido:
        base_url = 'https://slimeread.com/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            driver.get(base_url)
            
            # url = f"https://yomumangas.com/manga/{nome_formatado}/"
            url = str(input("Digite a URL da obra: "))
            if not "slimeread" in url:
                print("Erro: URL inválida. Status code: 404")
                driver.quit()
                sys.exit()
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print("Erro: URL inválida. Status code: 404")
                driver.quit()
                sys.exit()
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            turn = False

            # Localiza os elementos que contêm as informações dos capítulos
            for i in range(10):
                xpath = f'/html/body/div/div/main/section[{i}]/div[2]/div/div'
                chapter_elements = driver.find_elements(By.XPATH, xpath)
                
                if len(chapter_elements) == 0:
                    continue
                
                if "Cap" in chapter_elements[0].text:
                    turn = True
                    break
            
            if turn is False:
                print("Erro: Nenhum capítulo encontrado")
                driver.quit()
                sys.exit()
            
            # Extrai os dados dos capítulos
            for element in chapter_elements:
                for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                    chapter_number = sub.find_element(By.CSS_SELECTOR, 'p').text
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                    chapter_link = sub.get_attribute('href')
                    
                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)
        
        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(2)
            
            driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

            time.sleep(5)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(2)
            
            
            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.XPATH, '/html/body/div/div/main/div[3]')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None and link.startswith('http')]

            if len(links_das_imagens) == 0:
                print("Nenhuma imagem encontrada")
                driver.quit()
                sys.exit() 
            
            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 10
    elif "Flower Manga" in agregador_escolhido:
        base_url = 'https://flowermanga.com/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"{base_url}{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "flowermanga" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            
            # Executar o script JavaScript
            script = """
            var botao = document.querySelector('.c-chapter-readmore .btn');
            if (botao) {
                botao.click();
            } else {
                console.error("O botão não foi encontrado.");
            }
            """

            # Executar o script usando execute_script
            try:
                driver.execute_script(script)
            except Exception:
                pass

            time.sleep(2)

            # Localiza os elementos que contêm as informações dos capítulos
            chapter_elements = driver.find_elements(By.CLASS_NAME, "wp-manga-chapter")

            capitulos_encontrados = []

            for capitulo in chapter_elements:
                # Encontra o elemento 'a' dentro do 'li'
                a_element = capitulo.find_element(By.TAG_NAME, "a")

                # Obtém o texto do número do capítulo
                # Usa expressão regular para extrair números, pontos e vírgulas
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', a_element.text.replace(',', '')))
                link = a_element.get_attribute("href")

                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
                
            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)
        
        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(5)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(2)

            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.CLASS_NAME, 'reading-content')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() for link in links_das_imagens]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 11
    elif "Ler Manga Online" in agregador_escolhido:
        base_url = 'https://lermangaonline.com.br/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"{base_url}{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "lermangaonline" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            chapter_elements = driver.find_elements(By.CLASS_NAME, "capitulos")
            
            # Extrai os dados dos capítulos
            for element in chapter_elements:
                for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                    chapter_number = sub.find_element(By.CLASS_NAME, 'capitulo').text

                    # Use split para dividir a string e pegar o primeiro elemento
                    chapter_number = chapter_number.split(' ', 1)[1].split(' ', 1)[0] if ' ' in chapter_number else chapter_number

                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))

                    chapter_link = sub.get_attribute('href')

                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
                
            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)
        
        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            driver.implicitly_wait(10)

            time.sleep(5)

            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            
            time.sleep(2)

            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.CLASS_NAME, 'images')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None]
            links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()





    # Num 12
    elif "Manga BR" in agregador_escolhido:
        base_url = 'https://mangabr.net/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"{base_url}{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "mangabr" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            chapter_elements = driver.find_elements(By.XPATH, "/html/body/main/div/div/div/div[2]/div/div")
            
            # Extrai os dados dos capítulos
            for element in chapter_elements:
                for sub in element.find_elements(By.CSS_SELECTOR, 'a'):
                    chapter_number = sub.find_element(By.CLASS_NAME, 'mb-0').text
                    
                    # Use split para dividir a string e pegar o primeiro elemento
                    chapter_number = chapter_number.split('\n', 1)[0]
            
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                    
                    chapter_link = sub.get_attribute('href')
                    
                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
                
            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)
        
        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver.get(url)
            
            div_imagens = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div[3]')
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]

            while True:
                try:
                    next_page_button = WebDriverWait(driver, 2).until(
                        EC.visibility_of_element_located((By.CLASS_NAME, 'btn-next'))
                    )

                    next_page = next_page_button.get_attribute('href')

                except Exception:
                    div_imagens = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div[4]')
                    imagens = div_imagens.find_elements(By.TAG_NAME, 'img')
                    links_das_imagens += [imagem.get_attribute('src') for imagem in imagens]
                    break
                
                finally:
                    driver.get(next_page)
                    div_imagens = driver.find_element(By.XPATH, '/html/body/main/div/div/div/div[3]')
                    imagens = div_imagens.find_elements(By.TAG_NAME, 'img')
                    links_das_imagens += [imagem.get_attribute('src') for imagem in imagens]

            # Extrai os links das imagens
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None]
            links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()




    # Num 13
    elif "Projeto Scanlator" in agregador_escolhido:
        base_url = 'https://projetoscanlator.com/manga/'
        max_attempts = 10
        sleep_time = 0.1
        links = []

        # Função para obter capítulos dentro de um intervalo
        def obter_capitulos(driver, inicio, fim):
            url = f"{base_url}{nome_formatado}/"
            
            # Abre a página
            driver.get(url)
            
            # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
            driver.implicitly_wait(5)
            
            # Verifica se a página contém o texto "Página não encontrada"
            if "Página não encontrada" in driver.page_source:
                print(f"Erro: Obra {nome} não encontrado. Status code: 404")
                url = str(input("Digite a URL da obra: "))
                
                if not "projetoscanlator" in url:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
                
                # Tente abrir a página com o link fornecido
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    driver.quit()
                    sys.exit()
            
            time.sleep(5)
            
            os.system("cls")
            print("Verificando capítulos...")
            
            capitulos_encontrados = []
            chapter_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/div[4]/div/ul")

            capitulos_encontrados = []

            # Extrai os dados dos capítulos
            for element in chapter_elements:
                for sub in element.find_elements(By.CLASS_NAME, 'wp-manga-chapter'):
                    chapter_number = sub.text

                    # Use split para dividir a string e pegar o primeiro elemento
                    chapter_number = chapter_number.split('-', 1)[0]

                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))

                    sub2 = sub.find_element(By.CSS_SELECTOR, 'a')
                    chapter_link = sub2.get_attribute('href')

                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})

            return capitulos_encontrados

        capitulos_solicitados = obter_capitulos(driver, capítulo, ate)
        
        if len(capitulos_solicitados) == 0:
            print("Nenhum capítulo encontrado")
            driver.quit()
            sys.exit()

        async def run(url, numero_capitulo, session):
            folder_path = os.path.join(nome_foler, numero_capitulo)

            # Verificar se a pasta já existe e tem conteúdo
            contents = os.listdir(folder_path) if os.path.exists(folder_path) else []

            print(f"\n═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════")

            if contents:
                print(f"Info: a pasta {folder_path} já existe e contém arquivos. Excluindo conteúdo...")
                for item in contents:
                    item_path = os.path.join(folder_path, item)
                    if os.path.isdir(item_path):
                        shutil.rmtree(item_path)  # Exclui pasta e conteúdo
                    else:
                        os.remove(item_path)  # Exclui arquivo

            os.makedirs(folder_path, exist_ok=True)

            driver = initialize_driver("chrome", not args.no_headless)
            driver.get(url)
            
            # Localize o elemento select
            select_element = driver.find_element(By.XPATH, "/html/body/div[1]/div/div[1]/div/div/div/div/div/div/div[1]/div[3]/div/div[1]/div[2]/label/select")
            
            # Crie um objeto Select
            select = Select(select_element)
            select.select_by_visible_text("Estilo lista")
                
            time.sleep(5)
            
            # Encontra a div que contém as imagens
            div_imagens = driver.find_element(By.CLASS_NAME, 'reading-content')

            # Encontra todas as tags de imagem dentro da div
            imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

            # Extrai os links das imagens
            links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
            links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
            links_das_imagens = [link for link in links_das_imagens if link is not None]
            links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

            # Criar lista de tarefas assíncronas para o download
            tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

            # Agendar as tarefas para execução simultânea
            await asyncio.gather(*tasks)

            organizar(folder_path, nome, numero_capitulo)

            print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

        async with aiohttp.ClientSession() as session:
            driver.close()
            os.system("cls")
            
            # Inverter a ordem dos capítulos
            capitulos_solicitados.reverse()
            
            for capitulo in capitulos_solicitados:
                numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                url = capitulo['link']
                
                await run(url, numero_capitulo, session)
                    
            driver.quit()
















# Executar o loop de eventos do asyncio
loop = asyncio.get_event_loop()
loop.run_until_complete(main())
