import os
import re
import sys
import time
import webbrowser
import winsound
import requests
import win32api
import win32con
import shutil
import asyncio
import aiohttp
import zipfile
import pickle
import threading
import hashlib
import logging
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
import tkinter as tk
from tkinter import ttk, messagebox, filedialog, scrolledtext
from colorama import Fore, Style

# Importações da pasta 'src'
import src.imagemagick_check as imc
import src.folder_main as first
import src.load as load_settings
import src.save as save_settings
import src.theme as theme_set
import src.print as print_log
import src.time_zone as hora_agora
import src.execute_driver as ins_ext
import src.changelog as open_change


# Importações das URLs
import urls.br_mangas.main as agr_01
import urls.crystal_scan.main as agr_02
import urls.argos_comics.main as agr_03
import urls.argos_hentai.main as agr_04
import urls.mangás_chan.main as agr_05
import urls.ler_mangá.main as agr_06
import urls.tsuki.main as agr_07
import urls.yomumangás.main as agr_08
import urls.slimeread.main as agr_09
import urls.flower_manga.main as agr_10
import urls.ler_manga_online.main as agr_11
import urls.manga_br.main as agr_12
import urls.projeto_scanlator.main as agr_13


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


# Defiine o path da pasta confiigurações do app
settings_dir = first.setup()

# Carrega as configurações
auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, nao_var, sim_var, debug_var, debug2_var, headless_var, folder_selected, theme = load_settings.setup(settings_dir)


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


class AppMainTheme0():
    def __init__(self, root):
        self.root = root
        self.root.title("Mangá Downloader")
        self.style = ttk.Style(root)
    
        self.windows()
        
        self.settings_global()
        
        self.options()
        
        self.options_advanced()
        
        self.load_selenium()
            
        self.update_checkboxes_debug2()
        
        self.wait_check_selenium()
        
        open_change.setup(self.root, self.y)
        
    
    def wait_check_selenium(self):
        if not self.selenium_process_completed.is_set():
            self.root.after(100, self.wait_check_selenium)
        else:
            if self.selenium_working.get():
                self.start_download_button.config(state="normal")
        
    
    def load_selenium(self):
        self.selenium_process_completed = threading.Event()
        
        self.start_download_button.config(state="disabled")
        selenium_process_completed = threading.Thread(target=self.check_selenium)
        selenium_process_completed.start()
        
    
    def check_selenium(self):
        # Configurar as opções do Chrome
        temp_folder = os.environ['TEMP']
        profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
        download_folder = os.path.join(temp_folder, "Mangá Downloader Temp Download")
        extension_url = 'https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/Tampermonkey.4.19.0.0.crx'
        extension_name = "Tampermonkey.4.19.0.0.crx"
        extension_path = os.path.join(temp_folder, extension_name)
        
        if not os.path.exists(extension_path):
            response = requests.get(extension_url)
            
            with open(extension_path, 'wb') as file:
                file.write(response.content)
        
        
        os.makedirs(download_folder, exist_ok=True)
        
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Execute sem uma janela visível, se desejar
        chrome_options.add_argument("--disable-gpu")  # Desativar a aceleração de hardware, se necessário
        # chrome_options.add_argument(f"user-data-dir={profile_folder}")
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
    
    
    def save_settings(self):
        save_settings.setup(settings_dir, self.auto_save, self.agregador_var, self.nome_var, self.url_var, self.capitulo_var, self.ate_var, self.extension_var, self.compact_extension_var, self.nao_var, self.sim_var, self.debug_var, self.debug2_var, self.headless_var, self.folder_selected, self.theme)
    
        
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
        
        result = None
        
        if self.nome_var.get() == "":
            print("Erro: Nome inválido.")
            messagebox.showerror("Erro", "Nome inválido")
            result = 777
        
        elif self.url_var.get() == "":
            print("Erro: URL inválida.")
            messagebox.showerror("Erro", "URL inválida")
            result = 777
        
        elif self.capitulo_var.get() == "":
            print("Erro: Capítulo inválido.")
            messagebox.showerror("Erro", "Capítulo inválido")
            result = 777
        
        if result == 777:
            self.process_completed.set()
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
        
        nome_foler = nome.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace("\n", "").rstrip()
        
        carregar_imagens = [
            "Tsuki",
            "Mangás Chan",
        ]
        
        extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']
        extensoes_permitidas2 = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'apng', 'avif', 'bmp', 'tiff']
            
        if self.debug_var.get():
            self.baixando_label.config(text="Iniciando...")
            print_log.setup(
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
        extension_name = "Tampermonkey.4.19.0.0.crx"
        extension_path = os.path.join(temp_folder, extension_name)
        
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-notifications")
        if self.headless_var.get():
            chrome_options.add_argument("--headless=new")
            chrome_options.add_argument("--disable-web-security")
        # chrome_options.add_argument('--blink-settings=imagesEnabled=false') # Desativa a renderização de iamgens
        chrome_options.add_argument('--log-level=3')  # Nível 3 indica "sem logs"
        chrome_options.add_argument("--disable-gpu")
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument('--no-sandbox')
        if agregador_escolhido not in carregar_imagens:
            prefs = {"profile.managed_default_content_settings.images": 2}
            chrome_options.add_experimental_option("prefs", prefs)
        
        # chrome_options.add_argument(f"user-data-dir={profile_folder}")
        chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})
        
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        
        if agregador_escolhido in ['Tsuki']:
            chrome_options.add_extension(extension_path)
        
        # chrome_options.add_argument("--start-maximized")
        
        driver = webdriver.Chrome(options=chrome_options)
        
        dev_extand = False

        if dev_extand:
            # Emular uma conexão lenta usando o Chrome DevTools Protocol
            devtools_options = chrome_options.to_capabilities()
            devtools_options["goog:chromeOptions"]["perfLoggingPrefs"] = {
                "enableNetwork": True,
                "enablePage": False,
                "enableTimeline": False
            }
    
            # Configurar a condição de rede lenta (por exemplo, GPRS)
            driver.execute_cdp_cmd("Network.enable", {})
            driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
                "offline": False,
                "downloadThroughput": 500 * 1024,  # Velocidade de download em bytes por segundo
                "uploadThroughput": 200 * 1024,  # Velocidade de upload em bytes por segundo
                "latency": 500  # Atraso em milissegundos
            })
    
        if agregador_escolhido in ['Tsuki']:
            ins_ext.setup(driver)
        
        if self.debug_var.get():
            self.baixando_label.config(text="Aguarde...")
        print("\nAguarde...")
        
        
        
        for dic_name, dic_url in dic_agregadores.items():
            
            # Check
            if not dic_name in agregador_escolhido:
                continue
            
            # Num 01 (BR Mangás)
            elif "BR Mangás" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_01.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 02 (Crystal Scan)
            elif "Crystal Scan" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_02.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
                
            # Num 03 (Argos Comics)
            elif "Argos Comics" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_03.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 04 (Argos Hentai)
            elif "Argos Hentai" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_04.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 05 (Mangás Chan)
            elif "Mangás Chan" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_05.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 06 (Ler Mangá)
            elif "Ler Mangá" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_06.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 07 (Tsuki)
            elif "Tsuki" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_07.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 08 (YomuMangás)
            elif "YomuMangás" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_08.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 09 (SlimeRead)
            elif "SlimeRead" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_09.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 10 (Flower Manga)
            elif "Flower Manga" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_10.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 11 (Ler Manga Online)
            elif "Ler Manga Online" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_11.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 12 (Manga BR)
            elif "Manga BR" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_12.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
    
            # Num 13 (Projeto Scanlator)
            elif "Projeto Scanlator" in agregador_escolhido:
                if dic_url in url:
                    result = await agr_13.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension)
                    break
                else:
                    result = 1
                    print("Erro: URL inválida")
                    break
        


        if self.debug_var.get() and result == 0:
            self.baixando_label.config(text="Finalizado")
            winsound.Beep(1000, 500)  # O primeiro argumento é a frequência em Hz e o segundo é a duração em milissegundos
        
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
    
    
    def run_async_loop(self):
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.TkApp())
        loop.close()
    
    
    def wait_run_async_loop(self):
        if not self.process_completed.is_set():
            self.root.after(100, self.wait_run_async_loop)
        else:
            self.enable_gui()


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
        self.nav_check.config(state=tk.DISABLED)
        self.debug2_check.config(state=tk.DISABLED)
        self.debug_check.config(state=tk.DISABLED)
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
        self.debug2_check.config(state=tk.NORMAL)
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
    
    
    def select_folder_go(self):
        if self.folder_selected:
            webbrowser.open(self.folder_selected)
        else:
            print(hora_agora.setup(), "INFO:", "✘ Nenhuma pasta selecionada. Por favor, selecione uma pasta primeiro.")

    
    def select_folder(self):
        self.folder_selected = filedialog.askdirectory()
        self.selected_folder_text.config(state=tk.NORMAL)
        self.selected_folder_text.delete(0, tk.END)
        self.selected_folder_text.insert(0, self.folder_selected)
        self.selected_folder_text.config(state=tk.DISABLED)
        print(hora_agora.setup(), "INFO:", "✔ Pasta selecionada:", self.folder_selected)
        self.auto_save_settings()
        

    def update_checkboxes_debug(self):
        self.auto_save_settings()
    
    
    def update_checkboxes_debug2(self):
        if self.debug2_var.get():
            logging.disable(logging.NOTSET)
        else:
            logging.disable(logging.CRITICAL + 1)
        
        self.auto_save_settings()


    def update_checkboxes_nav(self):
        self.auto_save_settings()

    
    def site_url_open(self):
        agregador_escolhido = self.agregador_var.get()
        
        for dic_name, dic_url in dic_agregadores.items():
            
            if dic_name in agregador_escolhido:
                webbrowser.open(dic_url)
    
        
    def options_advanced(self):
        # Configurações
        config = tk.Label(self.root, text="Configurações", font=("Helvetica", 14))
        config.grid(row=0, column=3, padx=10, pady=5)
        
        # Auto save
        self.check_auto_save = tk.Checkbutton(self.root, text="Auto salvar", font=("Helvetica", 14), variable=self.auto_save, command=self.update_checkboxes_save)
        self.check_auto_save.grid(row=1, column=3, padx=0, pady=0)
        
        # Info
        self.debug_check = tk.Checkbutton(self.root, text="Info", font=("Helvetica", 14), variable=self.debug_var, command=self.update_checkboxes_debug)
        self.debug_check.grid(row=2, column=3, padx=0, pady=0)

        # DEBUG
        self.debug2_check = tk.Checkbutton(self.root, text="DEBUG", font=("Helvetica", 14), variable=self.debug2_var, command=self.update_checkboxes_debug2)
        self.debug2_check.grid(row=3, column=3, padx=0, pady=0)
        
        # Navegador
        self.nav_check = tk.Checkbutton(self.root, text="Navegador\nem segundo plano", font=("Helvetica", 14), variable=self.headless_var, command=self.update_checkboxes_nav)
        self.nav_check.grid(row=4, column=3, padx=0, pady=0)
        
        # Selecionar pasta
        self.select_folder_button = tk.Button(self.root, text="Selecionar pasta", font=("Helvetica", 14), command=self.select_folder)
        self.select_folder_button.grid(row=5, column=3, padx=10, pady=5)
        
        # Ir para a pasta selecionada
        self.select_folder_go_button = tk.Button(self.root, text="Ir para a pasta", font=("Helvetica", 14), command=self.select_folder_go)
        self.select_folder_go_button.grid(row=6, column=3, padx=10, pady=5)
        
        # Caixa de texto para exibir o caminho da pasta selecionada
        self.selected_folder_text = tk.Entry(self.root, font=("Helvetica", 12), width=40)
        self.selected_folder_text.grid(row=7, column=3, columnspan=2, padx=10, pady=5)
        self.selected_folder_text.insert(0, self.folder_selected)
        self.selected_folder_text.config(state=tk.DISABLED)
        
        # Label baixando
        self.baixando_label = tk.Label(self.root, text="", font=("Helvetica", 14))
        self.baixando_label.grid(row=9, column=3, padx=10, pady=5)
        
    
    def options(self):
        vcmd1 = (self.root.register(self.validate1))
        vcmd2 = (self.root.register(self.validate2))
        
        
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

    
    def settings_global(self):
        self.auto_save = auto_save
        self.agregador_var = agregador_var
        self.nome_var = nome_var
        self.url_var = url_var
        self.capitulo_var = capitulo_var
        self.ate_var = ate_var
        self.extension_var = extension_var
        self.compact_extension_var = compact_extension_var
        self.nao_var = nao_var
        self.sim_var = sim_var
        self.debug_var = debug_var
        self.debug2_var = debug2_var
        self.headless_var = headless_var
        self.folder_selected = folder_selected
        self.theme = theme
        
        self.auto_save = tk.BooleanVar(value=False)
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
        self.debug2_var = tk.BooleanVar(value=False)
        self.headless_var = tk.BooleanVar(value=True)
        self.selenium_working = tk.BooleanVar(value=False)
        
        self.auto_save.set(auto_save)
        self.agregador_var.set(agregador_var)
        self.nome_var.set(nome_var)
        self.url_var.set(url_var)
        self.capitulo_var.set(capitulo_var)
        self.ate_var.set(ate_var)
        self.extension_var.set(extension_var)
        self.compact_extension_var.set(compact_extension_var)
        self.nao_var.set(nao_var)
        self.sim_var.set(sim_var)
        self.debug_var.set(debug_var)
        self.debug2_var.set(debug2_var)
        self.headless_var.set(headless_var)
        
        
    def windows(self):
        # Bloquear redimensionamento da janela
        self.root.resizable(False, False)
        
        # Bloquear movimento da janela
        # Remove a barra de título e torna a janela não interativa
        self.root.overrideredirect(False)
        
        # Configuração para centralizar a janela
        window_width = 900
        window_height = 420
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.x = (screen_width - window_width) // 2
        self.y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{self.x}+{self.y}")



def setup():
    if theme == 0:
        root = tk.Tk()
        root.option_add("*tearOff", False)
        app = AppMainTheme0(root)
        
        theme_set.setup(root, theme)
        
        root.mainloop()
        
    else:
        print(hora_agora.setup(), "INFO:", "✘ Houve um erro ao iniciar a GUI.\n")
    
    