import os
import re
import subprocess
import sys
import time
import webbrowser
import requests
import win32api
import win32con
import shutil
import argparse
import asyncio
import aiohttp
import zipfile
import pickle
import threading
import zipfile
import hashlib
from urllib.parse import urlparse, urlunparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import filedialog

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
    messagebox.showinfo("Instalação do ImageMagick", "ImageMagick não está instalado.\nBaixando e instalando o ImageMagick...")
    
    # URL do instalador do ImageMagick
    url = 'https://github.com/OneDefauter/Menu_/releases/download/Req/ImageMagick-7.1.1-21-Q16-HDRI-x64-dll.exe'

    temp_folder = os.environ['TEMP']
    installer_path = os.path.join(temp_folder, 'ImageMagick-Installer.exe')

    response = requests.get(url)
    with open(installer_path, 'wb') as f:
        f.write(response.content)

    # Instalar o ImageMagick usando subprocess
    subprocess.run([installer_path, '/VERYSILENT'])
        
    os.remove(installer_path)
    messagebox.showinfo("Instalação concluída", "ImageMagick instalado com sucesso.")
    
    sys.exit()



def print_log(title, details=None):
    box_width = 100
    title = f'► {title} ◄'.center(box_width - 2)  # Ajuste manual do espaçamento
    
    print('╔' + '═' * (box_width - 2) + '╗')
    print(f'║{title}║')
    
    if details:
        for detail in details:
            print(f'║ {detail:<{box_width-4}} ║')  # Ajuste para exibir detalhes
    
    print('╚' + '═' * (box_width - 2) + '╝')



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

def calcular_sha1(file_path):
    sha1 = hashlib.sha1()
    with open(file_path, 'rb') as f:
        # Leitura do arquivo em blocos de 4K para eficiência
        for byte_block in iter(lambda: f.read(4096), b""):
            sha1.update(byte_block)
    return sha1.hexdigest()



class MainApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mangá Downloader")
        self.auto_save = tk.BooleanVar(value=False)
        
        # Bloquear redimensionamento da janela
        self.root.resizable(False, False)
        
        # Bloquear movimento da janela
        # Remove a barra de título e torna a janela não interativa
        self.root.overrideredirect(False)
        
        # Configuração para centralizar a janela
        window_width = 900
        window_height = 420
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Diretório onde o arquivo settings.pickle será salvo
        app_dir = os.path.join(os.path.expanduser("~"), "app")
        if not os.path.exists(app_dir):
            os.mkdir(app_dir)
            print("✔ Pasta do app criada")
        self.settings_dir = os.path.join(app_dir, "MangaDownloader")
        if not os.path.exists(self.settings_dir):
            os.mkdir(self.settings_dir)
            print("✔ Pasta de configuração criada")
            
        
        # Pré-carregar configurações do usuário
        self.agregador_var = tk.StringVar(value="BR Mangás")
        self.nome_var = tk.StringVar()
        self.url_var = tk.StringVar()
        self.capitulo_var = tk.StringVar()
        self.ate_var = tk.StringVar()
        self.extension_var = tk.StringVar(value=".jpg")
        self.compact_extension_var = tk.StringVar(value=".zip")
        self.sim_var = tk.BooleanVar(value=False)
        self.nao_var = tk.BooleanVar(value=True)
        self.debug_var = tk.BooleanVar(value=True)
        self.headless_var = tk.BooleanVar(value=True)
        self.selenium_working = tk.BooleanVar(value=False)
        self.folder_selected = os.path.join(os.path.expanduser("~"), "Downloads")
        
        self.create_widgets()
        
        self.create_settings()
            
        self.selenium_process_completed = threading.Event()
        
        self.start_download_button.config(state="disabled")
        selenium_process_completed = threading.Thread(target=self.check_selenium)
        selenium_process_completed.start()
        
        self.wait_check_selenium()
        
    def wait_check_selenium(self):
        if not self.selenium_process_completed.is_set():
            self.root.after(100, self.wait_check_selenium)
        else:
            if self.selenium_working.get():
                self.start_download_button.config(state="normal")
        
    def check_selenium(self):
        # Configurar as opções do Chrome
        temp_folder = os.environ['TEMP']
        profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
        profile_folder_2 = os.path.join(profile_folder, "Default")
        extension_folder = os.path.join(profile_folder_2, "Extensions", "dhdgffkkebhmkfjojejmpbldmpobfkfo")
        download_folder = os.path.join(temp_folder, "Mangá Downloader Temp Download")
        
        zip_manga_downloader_profile_url = "https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/Manga.Downloader.Profile_v1.zip"
        caminho_arquivo_zip = os.path.join(temp_folder, "Mangá.Downloader.Profile_v1.zip")
        
        sha_1_profile_folder = "eb1ece5152ade33cb5fe6abb37505b6f31afeb4a"
        
        if os.path.exists(caminho_arquivo_zip):
            hash_sha1 = calcular_sha1(caminho_arquivo_zip)
            
            if hash_sha1 == sha_1_profile_folder:
                print("Arquivo verificado.")
                if os.path.exists(profile_folder):
                    # Remove a pasta "Mangá Downloader Profile" e seu conteúdo
                    shutil.rmtree(profile_folder)
                    
                    # Cria a pasta "Mangá Downloader Profile"
                    os.makedirs(profile_folder, exist_ok=True)
                    
                    # Exporta o perfil
                    with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
                        zip_ref.extractall(profile_folder)
                        
                else:
                    # Cria a pasta "Mangá Downloader Profile"
                    os.makedirs(profile_folder, exist_ok=True)
                    
                    # Exporta o perfil
                    with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
                        zip_ref.extractall(profile_folder)
            
            else:
                os.remove(caminho_arquivo_zip)
                
                response = requests.get(zip_manga_downloader_profile_url)
                with open(caminho_arquivo_zip, 'wb') as f:
                    f.write(response.content)
                
                # Remove a pasta "Mangá Downloader Profile" e seu conteúdo
                shutil.rmtree(profile_folder)
                
                # Cria a pasta "Mangá Downloader Profile"
                os.makedirs(profile_folder, exist_ok=True)
                
                # Exporta o perfil
                with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
                    zip_ref.extractall(profile_folder)
        
        else:
            response = requests.get(zip_manga_downloader_profile_url)
            with open(caminho_arquivo_zip, 'wb') as f:
                f.write(response.content)
                
            # Cria a pasta "Mangá Downloader Profile"
            os.makedirs(profile_folder, exist_ok=True)
            
            # Exporta o perfil
            with zipfile.ZipFile(caminho_arquivo_zip, 'r') as zip_ref:
                zip_ref.extractall(profile_folder)
            
        os.makedirs(download_folder, exist_ok=True)
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Execute sem uma janela visível, se desejar
        chrome_options.add_argument("--disable-gpu")  # Desativar a aceleração de hardware, se necessário
        chrome_options.add_argument(f"user-data-dir={profile_folder}")
        chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})

        try:
            # Tente iniciar o driver do Chrome
            teste = webdriver.Chrome(options=chrome_options)
            # Abra uma página de teste para garantir que o Chrome está funcionando
            # teste.get("https://www.google.com")
            
            # Se não houver exceção até aqui, o Chrome está funcionando
            self.selenium_working.set(True)
            teste.quit()

        except Exception:
            os.system("cls")
            if not self.selenium_working.get():
                self.baixando_label.config(text="Erro:\n Selenium não está\n funcionando corretamente")
                messagebox.showerror("Erro", "Selenium não está funcionando corretamente")
            self.selenium_working.set(False)
            self.selenium_process_completed.set()
            
        finally:
            os.system("cls")
            if not self.selenium_working.get():
                self.baixando_label.config(text="Erro:\n Selenium não está\n funcionando corretamente")
                messagebox.showerror("Erro", "Selenium não está funcionando corretamente")
            self.selenium_process_completed.set()
            
    def create_widgets(self):
        # Carregar configurações do usuário
        print("✔ Carregado configurações salvas")
        self.load_settings()
        
        vcmd1 = (root.register(self.validate1))
        vcmd2 = (root.register(self.validate2))
        
        
        # Agregadores
        tk.Label(self.root, text="Agregador:", font=("Helvetica", 14)).grid(row=0, column=0, padx=10, pady=5)
        agregadores = list(dic_agregadores.keys())

        self.agregador_combobox = ttk.Combobox(self.root, textvariable=self.agregador_var, values=agregadores, font=("Helvetica", 14), validate='all', validatecommand=(vcmd2, '%P'))
        self.agregador_combobox.grid(row=0, column=1, padx=10, pady=5)
        
        
        # Agregador site
        self.url_open =tk.Button(self.root, text="Site", font=("Helvetica", 14), command=self.site_url_open)
        self.url_open.grid(row=0, column=2, padx=10, pady=5)
        
        
        # Nome da obra
        tk.Label(self.root, text="Nome da obra:", font=("Helvetica", 14)).grid(row=1, column=0, padx=10, pady=5)
        self.name = tk.Entry(self.root, textvariable=self.nome_var, font=("Helvetica", 14))
        self.name.grid(row=1, column=1, padx=10, pady=5)
        
        
        # URL da obra
        tk.Label(self.root, text="URL da obra:", font=("Helvetica", 14)).grid(row=2, column=0, padx=10, pady=5)
        self.url = tk.Entry(self.root, textvariable=self.url_var, font=("Helvetica", 14))
        self.url.grid(row=2, column=1, padx=10, pady=5)
        
        
        # Capítulo
        tk.Label(self.root, text="Capítulo:", font=("Helvetica", 14)).grid(row=3, column=0, padx=10, pady=5)
        self.cap = tk.Entry(self.root, textvariable=self.capitulo_var, font=("Helvetica", 14), validate='all', validatecommand=(vcmd1, '%P'))
        self.cap.grid(row=3, column=1, padx=10, pady=5)
        
        
        # Até qual capítulo baixar
        tk.Label(self.root, text="Até qual capítulo baixar:", font=("Helvetica", 14)).grid(row=4, column=0, padx=10, pady=5)
        self.ate = tk.Entry(self.root, textvariable=self.ate_var, font=("Helvetica", 14), validate='all', validatecommand=(vcmd1, '%P'))
        self.ate.grid(row=4, column=1, padx=10, pady=5)
        
        
        # Label "Compactar"
        tk.Label(self.root, text="Compactar:", font=("Helvetica", 14)).grid(row=5, column=0, padx=10, pady=5)

        # Checkbutton para "Sim"
        self.comapt_check_yes = tk.Checkbutton(self.root, text="Sim", font=("Helvetica", 14), variable=self.sim_var, command=self.update_checkboxes_sim)
        self.comapt_check_yes.grid(row=5, column=1, padx=10, pady=5)

        # Checkbutton para "Não"
        self.comapt_check_no = tk.Checkbutton(self.root, text="Não", font=("Helvetica", 14), variable=self.nao_var, command=self.update_checkboxes_nao)
        self.comapt_check_no.grid(row=5, column=2, padx=10, pady=5)
        
        
        # Lista com as extensões de saída disponíveis
        tk.Label(self.root, text="Extensão da compactação:", font=("Helvetica", 14)).grid(row=6, column=0, padx=10, pady=5)
        compact_extensions = [".zip", ".rar", ".cbz"]

        self.comapct_extension_combobox = ttk.Combobox(self.root, textvariable=self.compact_extension_var, values=compact_extensions, font=("Helvetica", 14), validate='all', validatecommand=(vcmd1, '%P'))
        self.comapct_extension_combobox.grid(row=6, column=1, padx=10, pady=5)
        
        
        # Lista com as extensões de saída disponíveis
        tk.Label(self.root, text="Extensão de saída:", font=("Helvetica", 14)).grid(row=7, column=0, padx=10, pady=5)
        extensions = [".png", ".jpg"]

        self.extension_combobox = ttk.Combobox(self.root, textvariable=self.extension_var, values=extensions, font=("Helvetica", 14), validate='all', validatecommand=(vcmd1, '%P'))
        self.extension_combobox.grid(row=7, column=1, padx=10, pady=5)
        
        # Configuração da linha 2 como vazia
        self.root.rowconfigure(8, weight=1)
        
        # Iniciar download
        self.start_download_button = tk.Button(self.root, text="Iniciar download", font=("Helvetica", 14), command=self.start_download)
        self.start_download_button.grid(row=9, column=1, padx=10, pady=5)
        
        
        # Salvar configurações
        self.save_button =tk.Button(self.root, text="Salvar configurações", font=("Helvetica", 14), command=self.save_settings)
        self.save_button.grid(row=9, column=0, padx=10, pady=5)
        
    
    def site_url_open(self):
        agregador_escolhido = self.agregador_var.get()
        
        for dic_name, dic_url in dic_agregadores.items():
            
            if dic_name in agregador_escolhido:
                webbrowser.open(dic_url)
    
    
    def create_settings(self):
        # Configurações
        config = tk.Label(self.root, text="Configurações", font=("Helvetica", 14))
        config.grid(row=0, column=3, padx=10, pady=5)
        
        # Auto save
        self.check_auto_save = tk.Checkbutton(root, text="Auto salvar", font=("Helvetica", 14), variable=self.auto_save, command=self.update_checkboxes_save)
        self.check_auto_save.grid(row=1, column=3, padx=0, pady=0)
        
        # Debug
        self.debug_check = tk.Checkbutton(root, text="Info", font=("Helvetica", 14), variable=self.debug_var, command=self.update_checkboxes_debug)
        self.debug_check.grid(row=2, column=3, padx=0, pady=0)
        
        # Navegador
        self.nav_check = tk.Checkbutton(root, text="Navegador\nem segundo plano", font=("Helvetica", 14), variable=self.headless_var, command=self.update_checkboxes_nav)
        self.nav_check.grid(row=3, column=3, padx=0, pady=0)
        
        # Selecionar pasta
        self.select_folder_button = tk.Button(self.root, text="Selecionar pasta", font=("Helvetica", 14), command=self.select_folder)
        self.select_folder_button.grid(row=4, column=3, padx=10, pady=5)
        
        # Ir para a pasta selecionada
        self.select_folder_go_button = tk.Button(self.root, text="Ir para a pasta", font=("Helvetica", 14), command=self.select_folder_go)
        self.select_folder_go_button.grid(row=5, column=3, padx=10, pady=5)
        
        # Caixa de texto para exibir o caminho da pasta selecionada
        self.selected_folder_text = tk.Entry(self.root, font=("Helvetica", 12), width=40)
        self.selected_folder_text.grid(row=6, column=3, columnspan=2, padx=10, pady=5)
        
        # Label baixando
        self.baixando_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.baixando_label.grid(row=9, column=3, padx=10, pady=5)
        
        
    def select_folder_go(self):
        if self.folder_selected:
            webbrowser.open(self.folder_selected)
        else:
            print("Nenhuma pasta selecionada. Por favor, selecione uma pasta primeiro.")

    
    def select_folder(self):
        self.folder_selected = filedialog.askdirectory()
        self.selected_folder_text.delete(0, tk.END)
        self.selected_folder_text.insert(0, self.folder_selected)
        print("Pasta selecionada:", self.folder_selected)
        self.auto_save_settings()
        

    def update_checkboxes_debug(self):
        self.auto_save_settings()


    def update_checkboxes_nav(self):
        self.auto_save_settings()


    async def TkApp(self):
        print("Agregador escolhido:", self.agregador_var.get())
        print("Obra escolhida:", self.nome_var.get())
        print("URL da obra:", self.url_var.get())
        print("Capítulo escolhido:", self.capitulo_var.get())
        print("Até qual capítulo baixar:", self.ate_var.get())
        print("Compactar:", self.sim_var.get())
        print("Extensão da compactação:", self.compact_extension_var.get())
        print("Extensão de saída:", self.extension_var.get())
        print("Auto salvar:", self.auto_save.get())
        print("Debug:", self.debug_var.get())
        print("Navegador em segundo plano:", self.headless_var.get())
        print("\n")
        
        if self.nome_var.get() == "":
            print("Erro: Nome inválido.")
            messagebox.showerror("Erro", "Nome inválido")
            return
        
        if self.url_var.get() == "":
            print("Erro: URL inválida.")
            messagebox.showerror("Erro", "URL inválida")
            return
        
        if self.capitulo_var.get() == "":
            print("Erro: Capítulo inválido.")
            messagebox.showerror("Erro", "Capítulo inválido")
            return
        
        if self.ate_var.get() == "":
            ate = float(self.capitulo_var.get())
        else:
            ate = float(self.ate_var.get())
        
        agregador_escolhido = self.agregador_var.get()
        nome = self.nome_var.get()
        url = self.url_var.get()
        capítulo = float(self.capitulo_var.get())
        compactar = self.sim_var.get()
        extension = self.extension_var.get()
        compact_extension = self.compact_extension_var.get()
        
        nome_foler = nome.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace("\n", "")
        
        carregar_imagens = [
            "Tsuki",
            "Mangás Chan",
        ]
        
        extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']
        extensoes_permitidas2 = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'apng', 'avif', 'bmp', 'tiff']
            
        if self.debug_var.get():
            self.baixando_label.config(text="Iniciando...")
            print_log(
                f'Agregador escolhido: {agregador_escolhido}', 
                [
                    f'Obra escolhida: {nome}',
                    f'Capítulo escolhido: {str(capítulo).replace(".0", "")}',
                    f'Até qual capítulo baixar: {str(ate).replace(".0", "")}',
                    f'Compactar: {compactar}',
                    f'Tipo de compactação: {compact_extension}',
                    f'Extensão de saída: {extension}'
                ]
            )
            print("\n")

        # Configurações das pastas
        temp_folder = os.environ['TEMP']
        profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
        download_folder = os.path.join(temp_folder, "Mangá Downloader Temp Download")
        
        chrome_options = webdriver.ChromeOptions()
        if self.headless_var.get():
            chrome_options.add_argument("--headless")
            chrome_options.add_argument("--disable-web-security")
        # chrome_options.add_argument('--blink-settings=imagesEnabled=false') # Desativa a renderização de iamgens
        chrome_options.add_argument('--log-level=3')  # Nível 3 indica "sem logs"
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--no-sandbox')
        if agregador_escolhido not in carregar_imagens:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
        
        chrome_options.add_argument(f"user-data-dir={profile_folder}")
        chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})
        
        driver = webdriver.Chrome(options=chrome_options)
    
        
        async def download(link, folder_path, session, counter, max_attempts=10, sleep_time=5):
            attempts = 0
            while attempts < max_attempts:
                try:
                    for x in extensoes_permitidas2:
                        if x in link.lower():
                            if not f".{x}" in link.lower():
                                link2 = link.lower().replace(f"{x}", f".{x}")
                                image_extension = link2.split(".")[-1]
                            else:
                                image_extension = link.split(".")[-1]
                            
                    image_name = f"{counter:02d}.{image_extension}"
                    image_path = os.path.join(folder_path, image_name)

                    # Aguardar um tempo antes de fazer o download
                    await asyncio.sleep(2)

                    async with session.get(link, ssl=False) as response:
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



        def organizar(folder_path, compactar, compact_extension, extension, extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']):
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
            
            if compactar:
                if compact_extension == ".cbz":
                    if os.path.exists(f'{folder_path}.cbz'):
                        os.remove(f'{folder_path}.cbz')
                    with zipfile.ZipFile(f'{folder_path}.cbz', 'w') as zipf:
                        for file_name in os.listdir(folder_path):
                            if file_name.endswith(extension):
                                zipf.write(os.path.join(folder_path, file_name), file_name)
                    shutil.rmtree(folder_path)
                elif compact_extension == ".zip":
                    if os.path.exists(f'{folder_path}.zip'):
                        os.remove(f'{folder_path}.zip')
                    with zipfile.ZipFile(f'{folder_path}.zip', 'w') as zipf:
                        for file_name in os.listdir(folder_path):
                            if file_name.endswith(extension):
                                zipf.write(os.path.join(folder_path, file_name), file_name)
                    shutil.rmtree(folder_path)

        
        if self.debug_var.get():
            self.baixando_label.config(text="Aguarde...")
        print("\nAguarde...")
        
        
        # Num 01 (BR Mangás)
        async def agr_01(driver, url, capítulo, ate):
            base_url = 'https://www.brmangas.net/ler/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
                # Esperar a lista de capítulos carregar
                capitulos = driver.find_elements(By.XPATH, '//div[@class="lista_manga"]//li[@class="row lista_ep"]')

                capitulos_encontrados = []
                
                os.system("cls")
                print("Verificando capítulos...")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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
                
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
                
                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)
                
                print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")

            async with aiohttp.ClientSession() as session:
                os.system("cls")
                for capitulo in capitulos_solicitados:
                    numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                    url = capitulo['link']
                    
                    await run(url, numero_capitulo, session)
                        
                driver.quit()
                
            return 0


        
        # Num 02 (Crystal Scan)
        async def agr_02(driver, url, capítulo, ate):
            base_url = 'https://crystalscan.net/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
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
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
                
                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 03 (Argos Comics)
        async def agr_03(driver, url, capítulo, ate):
            base_url = 'https://argoscomics.com/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
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
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")
                
                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0


        
        # Num 04 (Argos Hentai)
        async def agr_04(driver, url, capítulo, ate):
            base_url = 'https://argoshentai.com/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
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
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0


        
        # Num 05 (Mangás Chan)
        async def agr_05(driver, url, capítulo, ate):
            base_url = 'https://mangaschan.net/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                if not base_url in url:
                    print("Erro: URL inválida.")
                    driver.quit()
                    return 0
                
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return 0
                
                os.system("cls")
                print("Verificando capítulos...")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
            
            if capitulos_solicitados == 0:
                driver.quit()
                self.process_completed.set()

            if len(capitulos_solicitados) == 0:
                print("Nenhum capítulo encontrado")
                driver.quit()
                sys.exit()

            async def run(url, numero_capitulo, session):
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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
                
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Verificando capítulo {numero_capitulo}")
                
                # Injeta um script JavaScript para simular um pequeno movimento do mouse
                driver.execute_script("window.dispatchEvent(new Event('mousemove'));")

                time.sleep(5)
                
                # Encontrar o elemento <select>
                select_element = driver.find_element(By.ID, 'select-paged')

                # Obter todas as opções dentro do <select>
                options = select_element.find_elements(By.TAG_NAME, 'option')

                # Iterar sobre cada opção
                for option in options:
                    try:
                        # Clicar na opção para selecioná-la
                        option.click()

                        # Aguardar até que a página seja carregada (aqui estamos esperando por até 10 segundos)
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'selector.pagedsel.r'))
                        )

                        # Adicione aqui a lógica adicional para processar a página conforme necessário
                        # ...
                        time.sleep(1)

                    except Exception as e:
                        print(f"Erro ao processar a opção: {e}")
                
                # Encontra a div que contém as imagens
                div_imagens = driver.find_element(By.XPATH, '/html/body/div[1]/div[2]/div/div/div/article/div[3]')

                # Encontra todas as tags de imagem dentro da div
                imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

                # Extrai os links das imagens
                links_das_imagens = [imagem.get_attribute('src') for imagem in imagens]
                links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
                links_das_imagens = [link for link in links_das_imagens if link is not None]
                links_das_imagens = [urlparse(link)._replace(query='').geturl() for link in links_das_imagens if any(extensao in urlparse(link).path.lower() for extensao in extensoes_permitidas)]

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 06 (Ler Mangá)
        async def agr_06(driver, url, capítulo, ate):
            base_url = 'https://lermanga.org/mangas/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                lista_capitulos = driver.find_elements(By.CLASS_NAME, "single-chapter")
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return

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
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 07 (Tsuki)
        async def agr_07(driver, url, capítulo, ate):
            base_url = 'https://tsuki-mangas.com/obra/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                driver.refresh()
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                if "Error code 521" in driver.page_source:
                    print("Site indisponível. Status code: 521")
                    messagebox.showerror("Erro", "Site indisponível")
                    return "Error code 521"
                    
                # Verifica se a página contém o texto "Página não encontrada"
                elif "Página não encontrada" in driver.page_source:
                    print("Erro: URL inválida. Status code: 404")
                    messagebox.showerror("Erro", "URL inválida")
                    return "Error code 404"
                    
                elif "manutenção" in driver.page_source.lower():
                    print("Erro: Site em manutenção")
                    messagebox.showerror("Erro", "Site em manutenção")
                    return "Error code 001"
                    
                time.sleep(5)
                
                try:
                    # Aguarda até que o botão esteja presente na página
                    close_button = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CSS_SELECTOR, 'button[aria-label="Close this dialog"]'))
                    )

                    # Clica no botão
                    close_button.click()

                except:
                    ...

                finally:
                    driver.refresh()
                    time.sleep(3)
                
                
                print("Verificando capítulos...")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

                capitulos_encontrados = []
                count = 2
                
                # Loop para percorrer todas as páginas
                while True:
                    # Localiza os elementos que contêm as informações dos capítulos
                    chapter_elements = driver.find_elements(By.CSS_SELECTOR, '.cardchapters')

                    # Extrai os dados dos capítulos
                    for chapter_element in chapter_elements:
                        chapter_number = chapter_element.find_element(By.CSS_SELECTOR, 'a').text
                        
                        if chapter_number == '':
                            print("Erro: Houve um erro ao obter o número do capítulo")
                            messagebox.showerror("Erro", "Houve um erro ao obter o número do capítulo")
                            return 998
                        
                        numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '.')))

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

            if capitulos_solicitados == "Error code 001":
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Site em manutenção")
                return 999

            elif capitulos_solicitados == "Error code 404":
                if self.debug_var.get():
                    self.baixando_label.config(text=f"URL inválida")
                return 404

            elif capitulos_solicitados == "Error code 521":
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Site indisponível")
                return 521

            if len(capitulos_solicitados) == 0:
                print("Nenhum capítulo encontrado")
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Nenhum capítulo encontrado")
                return 3

            async def run(url, numero_capitulo, session):
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                time.sleep(3)
                
                verify1 = driver.find_element(By.XPATH, '/html/body/div/div')
                text = verify1.find_element(By.XPATH, '/html/body/div/div/div[2]').text
                if "Capítulo aguardando aprovação." in text:
                    print("Capítulo aguardando aprovação.")
                    return 4
                
                links_das_imagens = []
                count = 1
                
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Verificando capítulo {numero_capitulo}")
                
                for x in range(1, 11):  # Começando de 1 para evitar /html/body/div[0]/...
                    try:
                        elemento_lista_paginas = driver.find_element(By.XPATH, f'/html/body/div[{x}]/div[2]/div/div/div[1]/ul')
                        itens_lista_paginas = elemento_lista_paginas.find_elements(By.CSS_SELECTOR, 'li')
                        
                        numero_ultima_pagina = int(len(itens_lista_paginas))
                        break  # Sair do loop se encontrar com sucesso
                    
                    except:
                        continue  # Ignorar elementos que não têm o formato esperado
                    
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nCarregando página: {count} / {numero_ultima_pagina}")
                
                while True:
                    imagem_leitor = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.CLASS_NAME, 'pagereader'))
                    )
                    
                    # Obtém a URL atual
                    url_anterior = driver.current_url
                
                    # Tente verificar se a imagem foi carregada até 10 vezes
                    tentativas = 0
                    max_tentativas = 300
                    
                    while tentativas < max_tentativas:
                        try:
                            # Aguardar até que a imagem esteja presente no DOM
                            WebDriverWait(driver, 10).until(
                                EC.presence_of_element_located((By.CSS_SELECTOR, ".manga-reader img.pagereader"))
                            )
                            
                            # Executar um script JavaScript para verificar se a imagem foi carregada
                            script = """
                                var imagem = document.querySelector('.manga-reader img.pagereader');
                                if (imagem.complete) {
                                    return true;
                                } else {
                                    return false;
                                }
                            """
                            
                            imagem_carregada = driver.execute_script(script)
                            
                            if imagem_carregada:
                                # Encontrar o elemento da imagem pelo seletor CSS
                                imagem_elemento = driver.find_element(By.CSS_SELECTOR, ".manga-reader img.pagereader")

                                # Obter a URL da imagem do atributo 'src'
                                imagem_url = imagem_elemento.get_attribute("src")

                                # Abrir a imagem em uma nova guia usando JavaScript
                                script = f"window.open('{imagem_url}', '_blank');"
                                driver.execute_script(script)
                                
                                time.sleep(1)
                                
                                # Obter todas as guias abertas
                                janelas_abertas = driver.window_handles
                                
                                # Mudar para a nova guia (que deve ser a última na lista)
                                driver.switch_to.window(janelas_abertas[-1])
                                
                                action_chains = ActionChains(driver)

                                # Pressione a tecla Alt
                                action_chains.key_down(Keys.ALT)

                                # Pressione a tecla W
                                action_chains.send_keys('w')

                                # Libere a tecla Alt
                                action_chains.key_up(Keys.ALT)

                                # Execute as ações
                                action_chains.perform()
                                
                                time.sleep(0.5)
                                
                                download_button = driver.find_element(By.CLASS_NAME, "download-direct")
                                download_button.click()

                                time.sleep(0.5)
                                
                                lista = os.listdir(download_folder)
                                
                                for _ in range(1, 300):
                                    if len(lista) != 0:
                                        if not ".crdownload" in lista[0]:
                                            break
                                        else:
                                            lista = os.listdir(download_folder)
                                            time.sleep(1)
                                    else:
                                        time.sleep(1)
                                
                                file = os.path.join(download_folder, lista[0])
                                
                                image_extension = os.path.splitext(lista[0])[1]
                                
                                image_name = f"{count:02d}.{image_extension}"
                                image_path = os.path.join(folder_path, image_name)
                                
                                print(f"Baixando {imagem_url} como {image_name}...")
                                
                                os.makedirs(folder_path, exist_ok=True)
                                
                                shutil.move(file, image_path)
                                
                                # Fechar a guia atual
                                driver.close()
                                
                                break  # Sair do loop se a imagem foi carregada com sucesso
                            else:
                                tentativas += 1
                                # print(f"Tentativa {tentativas}: A imagem ainda não foi carregada. Tentando novamente...")
                                time.sleep(1)
                        except TimeoutException:
                            tentativas += 1
                            # print(f"Tentativa {tentativas}: Tempo limite expirado. Tentando novamente...")
                            time.sleep(1)

                    driver.switch_to.window(janelas_abertas[0])

                    div_imagens = driver.find_element(By.XPATH, '/html/body/div/div')
                    imagens = div_imagens.find_elements(By.TAG_NAME, 'img')

                    links_das_imagens += [imagem.get_attribute('src') for imagem in imagens]
                    
                    if self.debug_var.get():
                        self.baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nCarregando página: {count} / {numero_ultima_pagina}")
                
                    if count == numero_ultima_pagina:
                        break
                        
                    # Clica na imagem do leitor para avançar para a próxima página
                    # imagem_leitor.click()
                    # Clique no elemento usando JavaScript
                    driver.execute_script("arguments[0].click();", imagem_elemento)
                    
                    time.sleep(1)

                    # Verifica se a nova URL contém um indicativo de próximo capítulo
                    nova_url = driver.current_url
                    
                    if url_anterior != nova_url:
                        break
                    
                    count += 1
                   
                links_das_imagens = [link.strip() if link is not None else None for link in links_das_imagens]
                links_das_imagens = [link for link in links_das_imagens if link is not None]
                links_das_imagens = [link for link in links_das_imagens if not 'data:image' in link]
                links_das_imagens = [urlunparse(urlparse(url)._replace(query='')) for url in links_das_imagens]
                links_das_imagens = sorted(links_das_imagens)
                
                if len(links_das_imagens) == 0:
                    print("Nenhuma imagem encontrada")
                    if self.debug_var.get():
                        self.baixando_label.config(text=f"Erro no capítulo {numero_capitulo}\nNenhuma imagem encontrada")
                    return 2

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                # tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                # await asyncio.gather(*tasks)
                
                if self.debug_var.get():
                    self.baixando_label.config(text=f"Organizando capítulo {numero_capitulo}")

                organizar(folder_path, compactar, compact_extension, extension)

                print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
                
                return 0

            async with aiohttp.ClientSession() as session:
                os.system("cls")
                
                # Inverter a ordem dos capítulos
                capitulos_solicitados.reverse()
                
                for capitulo in capitulos_solicitados:
                    numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
                    url = capitulo['link']
                    
                    result = await run(url, numero_capitulo, session)
                        
                driver.quit()
                
            return result

        
        
        # Num 08 (YomuMangás)
        async def agr_08(driver, url, capítulo, ate):
            base_url = 'https://yomumangas.com/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
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
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 09 (SlimeRead)
        async def agr_09(driver, url, capítulo, ate):
            base_url = 'https://slimeread.com/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
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
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 10 (Flower Manga)
        async def agr_10(driver, url, capítulo, ate):
            base_url = 'https://flowermanga.com/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
                time.sleep(5)
                
                os.system("cls")
                print("Verificando capítulos...")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 11 (Ler Manga Online)
        async def agr_11(driver, url, capítulo, ate):
            base_url = 'https://lermangaonline.com.br/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
                time.sleep(5)
                
                os.system("cls")
                print("Verificando capítulos...")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 12 (Manga BR)
        async def agr_12(driver, url, capítulo, ate):
            base_url = 'https://mangabr.net/manga/'

            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
                time.sleep(5)
                
                os.system("cls")
                print("Verificando capítulos...")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        # Num 13 (Projeto Scanlator)
        async def agr_13(driver, url, capítulo, ate):
            base_url = 'https://projetoscanlator.com/manga/'
            
            # Função para obter capítulos dentro de um intervalo
            def obter_capitulos(driver, inicio, fim):
                # Abre a página
                driver.get(url)
                
                # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
                driver.implicitly_wait(5)
                
                # Verifica se a página contém o texto "Página não encontrada"
                if "Página não encontrada" in driver.page_source:
                        print("Erro: URL inválida. Status code: 404")
                        driver.quit()
                        return
                
                time.sleep(5)
                
                os.system("cls")
                print("Verificando capítulos...")
                
                capitulos_encontrados = []
                chapter_elements = driver.find_elements(By.XPATH, "/html/body/div[1]/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div/div[4]/div/ul")
                if self.debug_var.get():
                    self.baixando_label.config(text="Verificando capítulos...")

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
                folder_path = os.path.join(self.folder_selected, nome_foler, numero_capitulo)

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

                if self.debug_var.get():
                    self.baixando_label.config(text=f"Baixando capítulo {numero_capitulo}")

                # Criar lista de tarefas assíncronas para o download
                tasks = [download(link, folder_path, session, counter) for counter, link in enumerate(links_das_imagens, start=1)]

                # Agendar as tarefas para execução simultânea
                await asyncio.gather(*tasks)

                organizar(folder_path, compactar, compact_extension, extension)

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
                
            return 0

        
        
        
        
        
        
        
        for dic_name, dic_url in dic_agregadores.items():
            
            # Check
            if not dic_name in agregador_escolhido:
                continue
            
            # Num 01 (BR Mangás)
            elif "BR Mangás" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_01(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 02 (Crystal Scan)
            elif "Crystal Scan" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_02(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
                
            # Num 03 (Argos Comics)
            elif "Argos Comics" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_03(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 04 (Argos Hentai)
            elif "Argos Hentai" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_04(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 05 (Mangás Chan)
            elif "Mangás Chan" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_05(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 06 (Ler Mangá)
            elif "Ler Mangá" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_06(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 07 (Tsuki)
            elif "Tsuki" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_07(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 08 (YomuMangás)
            elif "YomuMangás" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_08(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 09 (SlimeRead)
            elif "SlimeRead" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_09(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 10 (Flower Manga)
            elif "Flower Manga" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_10(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 11 (Ler Manga Online)
            elif "Ler Manga Online" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_11(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 12 (Manga BR)
            elif "Manga BR" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_12(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 13 (Projeto Scanlator)
            elif "Projeto Scanlator" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_13(driver, url, capítulo, ate)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
        


        if self.debug_var.get() and result == 0:
            self.baixando_label.config(text="Finalizado")
        
        elif self.debug_var.get() and result == 1:
            self.baixando_label.config(text="URL inválida")
        
        elif self.debug_var.get() and result == 3:
            self.baixando_label.config(text=f"Nenhum capítulo encontrado")
        
        elif self.debug_var.get() and result == 4:
            self.baixando_label.config(text=f"Capítulo não aprovado")
        
        self.process_completed.set()

    
    def start_download(self):
        self.disable_gui()
        
        self.process_completed = threading.Event()
        
        processing_thread = threading.Thread(target=self.run_async_loop)
        processing_thread.start()
        
        self.wait_run_async_loop()
        
    
    def wait_run_async_loop(self):
        if not self.process_completed.is_set():
            self.root.after(100, self.wait_run_async_loop)
        else:
            self.enable_gui()
    
    
    def run_async_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.TkApp())
        loop.close()
        
        
    def disable_gui(self):
        # Desabilitar os elementos da GUI durante o processamento
        # ... (desabilitar elementos conforme necessário)
        self.start_download_button.config(state=tk.DISABLED)
        self.save_button.config(state=tk.DISABLED)
        self.check_auto_save.config(state=tk.DISABLED)
        self.extension_combobox.config(state=tk.DISABLED)
        self.comapct_extension_combobox.config(state=tk.DISABLED)
        self.comapt_check_no.config(state=tk.DISABLED)
        self.comapt_check_yes.config(state=tk.DISABLED)
        self.ate.config(state=tk.DISABLED)
        self.cap.config(state=tk.DISABLED)
        self.name.config(state=tk.DISABLED)
        self.agregador_combobox.config(state=tk.DISABLED)
        self.url.config(state=tk.DISABLED)
        self.debug_check.config(state=tk.DISABLED)
        self.nav_check.config(state=tk.DISABLED)
        self.select_folder_button.config(state=tk.DISABLED)

    def enable_gui(self):
        # Habilitar os elementos da GUI que estavam desabilitados durante o processamento
        # ... (habilitar elementos conforme necessário)
        self.start_download_button.config(state=tk.NORMAL)
        self.save_button.config(state=tk.NORMAL)
        self.check_auto_save.config(state=tk.NORMAL)
        self.extension_combobox.config(state=tk.NORMAL)
        self.comapct_extension_combobox.config(state=tk.NORMAL)
        self.comapt_check_no.config(state=tk.NORMAL)
        self.comapt_check_yes.config(state=tk.NORMAL)
        self.ate.config(state=tk.NORMAL)
        self.cap.config(state=tk.NORMAL)
        self.name.config(state=tk.NORMAL)
        self.agregador_combobox.config(state=tk.NORMAL)
        self.url.config(state=tk.NORMAL)
        self.debug_check.config(state=tk.NORMAL)
        self.nav_check.config(state=tk.NORMAL)
        self.select_folder_button.config(state=tk.NORMAL)

            
    def validate1(self, P):
        if str.isdigit(P) or P == "" or "." in P:
            self.auto_save_settings()
            return True
        else:
            return False
            
            
    def validate2(self, P):
        agregadores = list(dic_agregadores.keys())
        if P in agregadores:
            self.auto_save_settings()
            return True
        else:
            return False
            
            
    def validate3(self, P):
        compact_extensions = {
            ".zip": "1", 
            ".rar": "2", 
            ".cbz": "3"
        }
        compact_extensions = list(dic_agregadores.keys())
        if P in compact_extensions:
            self.auto_save_settings()
            return True
        else:
            return False
            
            
    def validate4(self, P):
        extensions = {
            ".png": "1", 
            ".jpg": "2"
        }
        extensions = list(dic_agregadores.keys())
        if P in extensions:
            self.auto_save_settings()
            return True
        else:
            return False
            
            
    def update_checkboxes_save(self):
        self.save_settings()
            
            
    def update_checkboxes_sim(self):
        # Desmarca a caixa "Não" quando "Sim" é marcado
        if self.sim_var.get():
            self.nao_var.set(False)
        self.auto_save_settings()


    def update_checkboxes_nao(self):
        # Desmarca a caixa "Sim" quando "Não" é marcado
        if self.nao_var.get():
            self.sim_var.set(False)
        self.auto_save_settings()
            
            
    def auto_save_settings(self):
        # Salva as configurações apenas se o "Auto salvar" estiver ativado
        if self.auto_save.get():
            self.save_settings()
            
            
    def save_settings(self):
        settings = {
            "auto_save": self.auto_save.get(),
            "agregador": self.agregador_var.get(),
            "nome": self.nome_var.get(),
            "url": self.url_var.get(),
            "capitulo": self.capitulo_var.get(),
            "ate": self.ate_var.get(),
            "extensao": self.extension_var.get(),
            "compact_extension": self.compact_extension_var.get(),
            "nao_var": self.nao_var.get(),
            "sim_var": self.sim_var.get(),
            "debug": self.debug_var.get(),
            "headless": self.headless_var.get(),
            "folder_selected": self.folder_selected
            # Adicione outros dados que você deseja salvar automaticamente aqui
        }

        with open(f"{self.settings_dir}/settings.pickle", "wb") as file:
            pickle.dump(settings, file)
        print("✔ Configurações salvas")
    
    
    def load_settings(self):
        try:
            with open(f"{self.settings_dir}/settings.pickle", "rb") as file:
                settings = pickle.load(file)

            self.auto_save.set(settings["auto_save"])
            self.agregador_var.set(settings["agregador"])
            self.nome_var.set(settings["nome"])
            self.url_var.set(settings["url"])
            self.capitulo_var.set(settings["capitulo"])
            self.ate_var.set(settings["ate"])
            self.extension_var.set(settings["extensao"])
            self.compact_extension_var.set(settings["compact_extension"])
            self.nao_var.set(settings["nao_var"])
            self.sim_var.set(settings["sim_var"])
            self.debug_var.set(settings["debug"])
            self.headless_var.set(settings["headless"])
            self.folder_selected = settings["folder_selected"]
            print("✔ Configurações carregadas")

        except:
            # Usar valores padrão caso o arquivo de configurações não exista
            print("✘ Erro ao carregar as configurações. Usando valores padrão.")
            self.auto_save.set(False)
            self.agregador_var.set("")
            self.nome_var.set("")
            self.url_var.set("")
            self.capitulo_var.set("")
            self.ate_var.set("")
            self.extension_var.set(".jpg")
            self.compact_extension_var.set(".zip")
            self.nao_var.set(True)
            self.sim_var.set(False)
            self.debug_var.set(True)
            self.headless_var.set(True)
        
        
        
        
        
      
if __name__ == "__main__":
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
