import os
import sys
import time
import shutil
import logging
import zipfile
import asyncio
import winsound
import requests
import threading
import webbrowser
from tkinter import *
import ttkbootstrap as tb
from datetime import datetime
from tkinter import ttk, messagebox, filedialog
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style


# Importações da pasta 'src'
import src.folder_main as first
import src.save as save_settings
import src.print as print_log
import src.time_zone as hora_agora
import src.execute_driver as ins_ext
import src.changelog as open_change
# import src.reload as reload_main
import src.clean as clean
import src.animation as anm
import src.folder_delete as del_folder


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
import urls.hentai_teca.main as agr_14
import urls.argos_scan.main as agr_15
import urls.nicomanga.main as agr_16
import urls.momo_no_hana.main as agr_17
import urls.manhastro.main as agr_18



# Ensines
import engine.default as engine_default
import engine.undetected as engine_undetected
import engine.cloudflare as engine_cloudflare



logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

os.system('cls')

# Defiine o path da pasta confiigurações do app
settings_dir = first.setup()

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
    "Hentai Teca": "https://hentaiteca.net/",
    "Argos Scan": "https://argosscan.com/",
    "NicoManga": "https://nicomanga.com/",
    "Momo no Hana": "https://momonohanascan.com/",
    "Manhastro": "https://manhastro.com/"
}

extensoes_permitidas = ['.png', '.jpg', '.jpeg', '.webp', '.gif', '.apng', '.avif', '.bmp', '.tiff']
extensoes_permitidas2 = ['png', 'jpg', 'jpeg', 'webp', 'gif', 'apng', 'avif', 'bmp', 'tiff']


version_ = 'Versão 2.7'
# icon = os.path.join()


# Extensão
temp_folder = os.environ['TEMP']
profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
download_folder = os.path.join(temp_folder, "Mangá Downloader Temp Download")
extension_url = 'https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/Tampermonkey.5.0.0.0.crx'
extension_zip_url = 'https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/Tampermonkey.5.0.0.0.zip'
extension_name = "Tampermonkey.5.0.0.0.crx"
extension_path = os.path.join(temp_folder, extension_name)
extension_folder_path = os.path.join(temp_folder, "Tampermonkey.5.0.0.0")



def abrir_link1(*args):
    webbrowser.open('https://github.com/OneDefauter/Manga-Downloader/blob/main/README.md')
    
def abrir_link2(*args):
    webbrowser.open('https://discordapp.com/users/367504043691606016')

class AppMain():
    def __init__(self, root, auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var, window_width, window_height, screen_width, screen_height, x, y):
        self.root = root
        self.auto_save = auto_save
        self.agregador_var = agregador_var
        self.nome_var = nome_var
        self.url_var = url_var
        self.capitulo_var = capitulo_var
        self.ate_var = ate_var
        self.extension_var = extension_var
        self.compact_extension_var = compact_extension_var
        self.compact_var = compact_var
        self.debug_var = debug_var
        self.debug2_var = debug2_var
        self.headless_var = headless_var
        self.folder_selected = folder_selected
        self.theme = theme
        self.net_option_var = net_option_var
        self.net_limit_down_var = net_limit_down_var
        self.net_limit_up_var = net_limit_up_var
        self.net_lat_var = net_lat_var
        
        # Tamanho da GUI
        self.change_log_var = change_log_var
        self.window_width = window_width
        self.window_height = window_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = x
        self.y = y
        
        self.ipo9 = True
        self.ian = False
        self.result = 0
        self.app_instance = anm.AnimationNotification(root, version_, self.ian)
        
        # self.root.title("Mangá Downloader")
        self.style = ttk.Style(root)
    
        # Style
        button_1 = tb.Style()
        button_1.configure('b1.TButton', font=("Segoe UI", 14, "bold"))
        button_1.configure('b2.TButton', font=("Segoe UI", 10, "bold"))
        
        button_1.configure('c1.TCheckbutton', font=("Segoe UI", 14, "bold"))
    
        self.root.bind("<Control-s>", self.save_shortcut)
        self.root.bind("<Control-i>", self.start_shortcut)
    
        button = tb.Button(self.root)
        button.place(relx=0.966, rely=0.0, height=40, width=40)
        button.configure(text='''X''')
        button.configure(command=self.close)
        button.configure(style="b1.TButton")
        
    
        # self.windows()
        
        self.settings_global()
        
        self.options_agreg()
            
        self.update_checkboxes_debug2()
        
        self.load_selenium()
        
        self.wait_check_selenium()
        
        if self.change_log_var.get():
            open_change.setup(self.root, self.y)
        
    def close(self):
        self.root.quit()
        sys.exit()
    
    def wait_check_selenium(self):
        if not self.selenium_process_completed.is_set():
            self.root.after(100, self.wait_check_selenium)
        else:
            if self.selenium_working.get():
                self.start_download_button.config(state="normal")
                
                self.app_instance.move_text_wait('Navegador pronto')
                
            self.ipo9 = False
            self.reset_config_button.config(state="normal")
            self.theme_0.config(state="normal")
            self.theme_1.config(state="normal")
            self.theme_2.config(state="normal")
            self.theme_3.config(state="normal")
            self.theme_4.config(state="normal")
            self.theme_5.config(state="normal")
            self.theme_6.config(state="normal")
            self.theme_7.config(state="normal")
            self.theme_8.config(state="normal")
            self.theme_9.config(state="normal")
            self.theme_10.config(state="normal")
            self.theme_11.config(state="normal")
            self.theme_12.config(state="normal")
            self.theme_13.config(state="normal")
            self.theme_14.config(state="normal")
            self.theme_15.config(state="normal")
            self.theme_16.config(state="normal")
            self.theme_17.config(state="normal")
            self.theme_18.config(state="normal")
    
    
    def load_selenium(self):
        self.selenium_process_completed = threading.Event()
        
        self.start_download_button.config(state="disabled")
        self.reset_config_button.config(state="disabled")
        self.theme_0.config(state="disabled")
        self.theme_1.config(state="disabled")
        self.theme_2.config(state="disabled")
        self.theme_3.config(state="disabled")
        self.theme_4.config(state="disabled")
        self.theme_5.config(state="disabled")
        self.theme_6.config(state="disabled")
        self.theme_7.config(state="disabled")
        self.theme_8.config(state="disabled")
        self.theme_9.config(state="disabled")
        self.theme_10.config(state="disabled")
        self.theme_11.config(state="disabled")
        self.theme_12.config(state="disabled")
        self.theme_13.config(state="disabled")
        self.theme_14.config(state="disabled")
        self.theme_15.config(state="disabled")
        self.theme_16.config(state="disabled")
        self.theme_17.config(state="disabled")
        self.theme_18.config(state="disabled")
            
        selenium_process_completed = threading.Thread(target=self.check_selenium)
        selenium_process_completed.start()
        
        self.root.after(2000, self.selenium_load_message)
        
    
    def check_selenium(self):
        try:
            shutil.rmtree(profile_folder)
        except:
            ...
        
        os.makedirs(profile_folder, exist_ok=True)
        
        if not os.path.exists(extension_path):
            response = requests.get(extension_url)
            
            with open(extension_path, 'wb') as file:
                file.write(response.content)
        
        if not os.path.exists(extension_folder_path):
            response = requests.get(extension_zip_url)
            
            with open(f'{extension_folder_path}.zip', 'wb') as file:
                file.write(response.content)
                
            os.makedirs(extension_folder_path, exist_ok=True)
            
            # Abre o arquivo ZIP
            with zipfile.ZipFile(f'{extension_folder_path}.zip', 'r') as zip_ref:
                # Extrai todos os arquivos na pasta de destino
                zip_ref.extractall(extension_folder_path)
        
        
        os.makedirs(download_folder, exist_ok=True)
        
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")  # Execute sem uma janela visível, se desejar
        chrome_options.add_argument("--disable-gpu")  # Desativar a aceleração de hardware, se necessário
        chrome_options.add_argument('--log-level=3')
        chrome_options.add_extension(extension_path)
        chrome_options.add_argument(f"user-data-dir={profile_folder}")
        chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})

        try:
            # Tente iniciar o driver do Chrome
            teste = webdriver.Chrome(options=chrome_options)
            # Abra uma página de teste para garantir que o Chrome está funcionando
            # teste.get("https://www.google.com")
            
            ins_ext.setup(teste)
            
            teste.quit()
            time.sleep(1)
            
            teste2 = webdriver.Chrome(options=chrome_options)
            teste2.get('https://www.google.com.br/')
    
            # Pega o tempo inicial
            tempo_inicial = datetime.now()

            # Define o limite de tempo em segundos (30 segundos no seu caso)
            limite_tempo_segundos = 10

            while True:
                janelas_abertas = teste2.window_handles

                if len(janelas_abertas) != 1:
                    teste2.switch_to.window(janelas_abertas[-1])
                    teste2.close()
                    janelas_abertas = teste2.window_handles
                    teste2.switch_to.window(janelas_abertas[0])
                    break
                else:
                    tempo_atual = datetime.now()
                    tempo_decorrido = tempo_atual - tempo_inicial

                    if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                        print("Tempo limite atingido. Saindo do loop.")
                        break
                    
            teste2.quit()
            time.sleep(1)
            
            # Se não houver exceção até aqui, o Chrome está funcionando
            self.selenium_working.set(True)
            self.selenium_process_completed.set()
            
        except:
            os.system("cls")
            if not self.selenium_working.get():
                self.baixando_label.config(text="Erro:\n Selenium não está\n funcionando corretamente")
                messagebox.showerror("Erro", "Selenium não está funcionando corretamente")
            self.selenium_working.set(False)
            self.selenium_process_completed.set()
    
    
    def save_settings(self):
        self.app_instance.move_text_wait(f'Configurações foram salvas')
        save_settings.setup(settings_dir, self.auto_save, self.agregador_var, self.nome_var, self.url_var, self.capitulo_var, self.ate_var, self.extension_var, self.compact_extension_var, self.compact_var, self.debug_var, self.debug2_var, self.headless_var, self.folder_selected, self.theme, self.net_option_var, self.net_limit_down_var, self.net_limit_up_var, self.net_lat_var, self.change_log_var)
    
        
    async def TkApp(self):
        os.system('cls')
        
        self.result = None
        
        print("Agregador escolhido:", self.agregador_var.get())
        print("Obra escolhida:", self.nome_var.get())
        print("URL da obra:", self.url_var.get())
        print("Capítulo escolhido:", self.capitulo_var.get())
        print("Até qual capítulo baixar:", self.ate_var.get())
        print("Compactar:", self.compact_var.get())
        print("Extensão da compactação:", self.compact_extension_var.get())
        print("Extensão de saída:", self.extension_var.get())
        print("Auto salvar:", self.auto_save.get())
        print("Debug:", self.debug_var.get())
        print("Navegador em segundo plano:", self.headless_var.get())
        print("\n")
        
        if self.nome_var.get() == "":
            print("Erro: Nome inválido.")
            self.app_instance.move_text_wait('Erro: Nome inválido')
            messagebox.showerror("Erro", "Nome inválido")
            self.result = 777
        
        elif self.url_var.get() == "":
            print("Erro: URL inválida.")
            self.app_instance.move_text_wait('Erro: URL inválida')
            messagebox.showerror("Erro", "URL inválida")
            self.result = 777
        
        elif self.capitulo_var.get() == "":
            print("Erro: Capítulo inválido.")
            self.app_instance.move_text_wait('Erro: Capítulo inválido')
            messagebox.showerror("Erro", "Capítulo inválido")
            self.result = 777
        
        if self.result == 777:
            self.process_completed.set()
        
        
        if self.result is None:
            if self.capitulo_var.get() == "" and self.ate_var.get() != "":
                 capítulo = 0.0
                 ate = float(self.ate_var.get())
            elif self.ate_var.get() == "" and self.capitulo_var.get() != "":
                capítulo = float(self.capitulo_var.get())
                ate = float(self.capitulo_var.get())
            else:
                capítulo = float(self.capitulo_var.get())
                ate = float(self.ate_var.get())
            
            chekin = True
            
            if ate < capítulo:
                self.app_instance.move_text_wait('Erro: Capítulo inválido')
                self.result = 777
                chekin = False
                self.process_completed.set()
        
        
        if chekin:
            agregador_escolhido = self.agregador_var.get()
            nome = self.nome_var.get()
            url = self.url_var.get()
            # capítulo = float(self.capitulo_var.get())
            compactar = self.compact_var.get()
            extension = self.extension_var.get()
            compact_extension = self.compact_extension_var.get()
            
            nome_foler = nome.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace("\n", "").rstrip()
            
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
            self.app_instance.move_text_wait('Iniciando')
            
            
            if not agregador_escolhido in ['Hentai Teca', 'Mangás Chan', 'Manhastro', 'Tsuki']:
                driver = engine_default.setup(self.headless_var.get(), agregador_escolhido, profile_folder, download_folder, extension_path, self.net_option_var.get(), self.net_limit_down_var.get(), self.net_limit_up_var.get(), self.net_lat_var.get())
            
            elif agregador_escolhido in ['Mangás Chan', 'Tsuki']:
                if self.headless_var.get():
                    print(f"{Fore.GREEN}AVISO: Esse agregador não suporta download em segundo plano.{Style.RESET_ALL}")
                driver = engine_cloudflare.setup()
            
            else:
                driver = engine_undetected.setup(self.headless_var.get(), agregador_escolhido, profile_folder, download_folder, extension_path, self.net_option_var.get(), self.net_limit_down_var.get(), self.net_limit_up_var.get(), self.net_lat_var.get())
            
            # Instala a extensão e os scripts
            # ins_ext.setup(driver)
            
            if self.debug_var.get():
                self.baixando_label.config(text="Aguarde...")
            print("\nAguarde...")
            
            clean.setup(download_folder)
            
            for dic_name, dic_url in dic_agregadores.items():
                
                # Check
                if not dic_name in agregador_escolhido:
                    continue
                
                # Num 01 (BR Mangás)
                elif "BR Mangás" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_01.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 02 (Crystal Scan)
                elif "Crystal Scan" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_02.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
                    
                # Num 03 (Argos Comics)
                elif "Argos Comics" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_03.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 04 (Argos Hentai)
                elif "Argos Hentai" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_04.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 05 (Mangás Chan)
                elif "Mangás Chan" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_05.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 06 (Ler Mangá)
                elif "Ler Mangá" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_06.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 07 (Tsuki)
                elif "Tsuki" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_07.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 08 (YomuMangás)
                elif "YomuMangás" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_08.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 09 (SlimeRead)
                elif "SlimeRead" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_09.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 10 (Flower Manga)
                elif "Flower Manga" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_10.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 11 (Ler Manga Online)
                elif "Ler Manga Online" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_11.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 12 (Manga BR)
                elif "Manga BR" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_12.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 13 (Projeto Scanlator)
                elif "Projeto Scanlator" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_13.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 14 (Hentai Teca)
                elif "Hentai Teca" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_14.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 15 (Argos Scan)
                elif "Argos Scan" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_15.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 16 (NicoManga)
                elif "NicoManga" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_16.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 17 (Momo no Hana)
                elif "Momo no Hana" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_17.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
        
                # Num 18 (Manhastro)
                elif "Manhastro" in agregador_escolhido:
                    if dic_url in url:
                        self.result = await agr_18.setup(driver, url, capítulo, ate, self.debug_var, self.baixando_label, self.folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, self.app_instance)
                        try:
                            driver.quit()
                        except:
                            ...
                        break
                    else:
                        self.result = 1
                        driver.quit()
                        print("Erro: URL inválida")
                        break
            
            folder_path = os.path.join(self.folder_selected, nome_foler)
            del_folder.delete_empty_folders(folder_path.replace('/', '\\'))
            
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
            # Resultado
            if self.debug_var.get():
                # Bem-sucedido
                if self.result == 0:
                    self.baixando_label.config(text="Finalizado")
                    winsound.Beep(1000, 500)
                    self.app_instance.move_text_wait('Processo finalizado')
                    
                # URL inválida
                if self.result == 1:
                    self.baixando_label.config(text="URL inválida")
                    self.app_instance.move_text_wait('Erro: URL inválida')
                
                # Nenhum capítulo encontrado
                elif self.result == 3:
                    self.baixando_label.config(text="Nenhum capítulo encontrado")
                    self.app_instance.move_text_wait('Nenhum capítulo encontrado')
                    
                # Capítulo não aprovado
                elif self.result == 4:
                    self.baixando_label.config(text="Capítulo não aprovado")
                    self.app_instance.move_text_wait('Capítulo não aprovado')
                
                # Erro 4xx
                elif self.result == 'e400':
                    self.baixando_label.config(text="Erro: URL inválida. Status code: 400")
                    self.app_instance.move_text_wait("Erro: URL inválida. Status code: 400")
                elif self.result == 'e401':
                    self.baixando_label.config(text="Erro: Sem acesso. Status code: 401")
                    self.app_instance.move_text_wait("Erro: Sem acesso. Status code: 401")
                elif self.result == 'e403':
                    self.baixando_label.config(text="Erro: Sem acesso. Status code: 403")
                    self.app_instance.move_text_wait("Erro: Sem acesso. Status code: 403")
                elif self.result == 'e404':
                    self.baixando_label.config(text="Erro: URL inválida. Status code: 404")
                    self.app_instance.move_text_wait("Erro: URL inválida. Status code: 404")
                    
                # Erro 5xx
                elif self.result == 'e500':
                    self.baixando_label.config(text="Erro: Serviço indisponível. Status code: 500")
                    self.app_instance.move_text_wait("Erro: Serviço indisponível. Status code: 500")
                elif self.result == 'e502':
                    self.baixando_label.config(text="Erro: Serviço indisponível. Status code: 502")
                    self.app_instance.move_text_wait("Erro: Serviço indisponível. Status code: 502")
                elif self.result == 'e403':
                    self.baixando_label.config(text="Erro: Serviço indisponível. Status code: 503")
                    self.app_instance.move_text_wait("Erro: Serviço indisponível. Status code: 503")
                elif self.result == 'e523':
                    self.baixando_label.config(text="Erro: Acesso bloqueado. Status code: 523")
                    self.app_instance.move_text_wait("Erro: Acesso bloqueado. Status code: 523")
                
            else:
                # Bem-sucedido
                if self.result == 0:
                    winsound.Beep(1000, 500)
                    self.app_instance.move_text_wait('Processo finalizado')
                
                # URL inválida
                if self.result == 1:
                    self.app_instance.move_text_wait('Erro: URL inválida')
                
                # Nenhum capítulo encontrado
                elif self.result == 3:
                    self.app_instance.move_text_wait('Nenhum capítulo encontrado')
                    
                # Capítulo não aprovado
                elif self.result == 4:
                    self.app_instance.move_text_wait('Capítulo não aprovado')
                
                # Erro 4xx
                elif self.result == 'e400':
                    self.app_instance.move_text_wait("Erro: URL inválida. Status code: 400")
                elif self.result == 'e401':
                    self.app_instance.move_text_wait("Erro: Sem acesso. Status code: 401")
                elif self.result == 'e403':
                    self.app_instance.move_text_wait("Erro: Sem acesso. Status code: 403")
                elif self.result == 'e404':
                    self.app_instance.move_text_wait("Erro: URL inválida. Status code: 404")
                    
                # Erro 5xx
                elif self.result == 'e500':
                    self.app_instance.move_text_wait("Erro: Serviço indisponível. Status code: 500")
                elif self.result == 'e502':
                    self.app_instance.move_text_wait("Erro: Serviço indisponível. Status code: 502")
                elif self.result == 'e403':
                    self.app_instance.move_text_wait("Erro: Serviço indisponível. Status code: 503")
                elif self.result == 'e523':
                    self.app_instance.move_text_wait("Erro: Acesso bloqueado. Status code: 523")
                
                self.driver
                
            self.enable_gui()


    def disable_gui(self):
        self.ipo9 = True
        # Desabilitar os elementos da GUI durante o processamento
        # ... (desabilitar elementos conforme necessário)
        self.start_download_button.config(state=tb.DISABLED)
        self.save_button.config(state=tb.DISABLED)
        self.check_auto_save.config(state=tb.DISABLED)
        self.extension_combobox.config(state=tb.DISABLED)
        self.comapct_extension_combobox.config(state=tb.DISABLED)
        self.comapt_check.config(state=tb.DISABLED)
        self.ate.config(state=tb.DISABLED)
        self.cap.config(state=tb.DISABLED)
        self.name.config(state=tb.DISABLED)
        self.agregador_combobox.config(state=tb.DISABLED)
        self.url.config(state=tb.DISABLED)
        self.nav_check.config(state=tb.DISABLED)
        self.debug2_check.config(state=tb.DISABLED)
        self.debug_check.config(state=tb.DISABLED)
        self.select_folder_button.config(state=tb.DISABLED)
        self.net_option.config(state=tb.DISABLED)
        self.net_limit_down.config(state=tb.DISABLED)
        self.net_limit_up.config(state=tb.DISABLED)
        self.net_lat.config(state=tb.DISABLED)
        self.reset_config_button.config(state=tb.DISABLED)
        self.theme_0.config(state=tb.DISABLED)
        self.theme_1.config(state=tb.DISABLED)
        self.theme_2.config(state=tb.DISABLED)
        self.theme_3.config(state=tb.DISABLED)
        self.theme_4.config(state=tb.DISABLED)
        self.theme_5.config(state=tb.DISABLED)
        self.theme_6.config(state=tb.DISABLED)
        self.theme_7.config(state=tb.DISABLED)
        self.theme_8.config(state=tb.DISABLED)
        self.theme_9.config(state=tb.DISABLED)
        self.theme_10.config(state=tb.DISABLED)
        self.theme_11.config(state=tb.DISABLED)
        self.theme_12.config(state=tb.DISABLED)
        self.theme_13.config(state=tb.DISABLED)
        self.theme_14.config(state=tb.DISABLED)
        self.theme_15.config(state=tb.DISABLED)
        self.theme_16.config(state=tb.DISABLED)
        self.theme_17.config(state=tb.DISABLED)
        self.theme_18.config(state=tb.DISABLED)


    def enable_gui(self):
        self.ipo9 = False
        # Habilitar os elementos da GUI que estavam desabilitados durante o processamento
        # ... (habilitar elementos conforme necessário)
        self.start_download_button.config(state=tb.NORMAL)
        self.save_button.config(state=tb.NORMAL)
        self.check_auto_save.config(state=tb.NORMAL)
        self.extension_combobox.config(state=tb.NORMAL)
        self.comapct_extension_combobox.config(state=tb.NORMAL)
        self.comapt_check.config(state=tb.NORMAL)
        self.ate.config(state=tb.NORMAL)
        self.cap.config(state=tb.NORMAL)
        self.name.config(state=tb.NORMAL)
        self.agregador_combobox.config(state=tb.NORMAL)
        self.url.config(state=tb.NORMAL)
        self.debug_check.config(state=tb.NORMAL)
        self.nav_check.config(state=tb.NORMAL)
        self.debug2_check.config(state=tb.NORMAL)
        self.select_folder_button.config(state=tb.NORMAL)
        self.net_option.config(state=tb.NORMAL)
        self.net_limit_down.config(state=tb.NORMAL)
        self.net_limit_up.config(state=tb.NORMAL)
        self.net_lat.config(state=tb.NORMAL)
        self.reset_config_button.config(state=tb.NORMAL)
        self.theme_0.config(state=tb.NORMAL)
        self.theme_1.config(state=tb.NORMAL)
        self.theme_2.config(state=tb.NORMAL)
        self.theme_3.config(state=tb.NORMAL)
        self.theme_4.config(state=tb.NORMAL)
        self.theme_5.config(state=tb.NORMAL)
        self.theme_6.config(state=tb.NORMAL)
        self.theme_7.config(state=tb.NORMAL)
        self.theme_8.config(state=tb.NORMAL)
        self.theme_9.config(state=tb.NORMAL)
        self.theme_10.config(state=tb.NORMAL)
        self.theme_11.config(state=tb.NORMAL)
        self.theme_12.config(state=tb.NORMAL)
        self.theme_13.config(state=tb.NORMAL)
        self.theme_14.config(state=tb.NORMAL)
        self.theme_15.config(state=tb.NORMAL)
        self.theme_16.config(state=tb.NORMAL)
        self.theme_17.config(state=tb.NORMAL)
        self.theme_18.config(state=tb.NORMAL)

            
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
            
            
    def update_checkboxes_compact(self):
        self.auto_save_settings()
            
            
    def auto_save_settings(self):
        # Salva as configurações apenas se o "Auto salvar" estiver ativado
        if self.auto_save.get():
            save_settings.setup(settings_dir, self.auto_save, self.agregador_var, self.nome_var, self.url_var, self.capitulo_var, self.ate_var, self.extension_var, self.compact_extension_var, self.compact_var, self.debug_var, self.debug2_var, self.headless_var, self.folder_selected, self.theme, self.net_option_var, self.net_limit_down_var, self.net_limit_up_var, self.net_lat_var, self.change_log_var)
    
    
    def select_folder_go(self):
        if self.folder_selected:
            webbrowser.open(self.folder_selected)
        else:
            print(hora_agora.setup(), "INFO:", "✘ Nenhuma pasta selecionada. Por favor, selecione uma pasta primeiro.")

    
    def select_folder(self):
        self.folder_selected = filedialog.askdirectory()
        self.selected_folder_text.config(state=tb.NORMAL)
        self.selected_folder_text.delete(0, tb.END)
        self.selected_folder_text.insert(0, self.folder_selected)
        self.selected_folder_text.config(state=tb.READONLY)
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
    
    
    def options_agreg(self):
        self.vcmd1 = (self.root.register(self.validate1))
        self.vcmd2 = (self.root.register(self.validate2))
        
        
        
        # Agregadores
        self.agregador_text = tb.Label(self.root)
        self.agregador_text.place(relx=0.036, rely=0.021, height=63, width=195)
        # self.agregador_text.configure(activebackground="#f0f0f0")
        self.agregador_text.configure(anchor='w')
        # self.agregador_text.configure(background="#f0f0f0")
        self.agregador_text.configure(compound='left')
        # self.agregador_text.configure(disabledforeground="#a3a3a3")
        self.agregador_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.agregador_text.configure(foreground="#000000")
        # self.agregador_text.configure(highlightbackground="#d9d9d9")
        # self.agregador_text.configure(highlightcolor="black")
        self.agregador_text.configure(text='''Agregador''')
        
        agregadores = list(dic_agregadores.keys())
        
        self.agregador_combobox = ttk.Combobox(self.root)
        self.agregador_combobox.place(relx=0.036, rely=0.129, relheight=0.071
                , relwidth=0.386)
        self.agregador_combobox.configure(font="-family {Arial} -size 14 -weight bold")
        self.agregador_combobox.configure(textvariable=self.agregador_var)
        self.agregador_combobox.configure(values=agregadores)
        self.agregador_combobox.configure(validate='all')
        self.agregador_combobox.configure(validatecommand=(self.vcmd2, '%P'))
        
        
        
        # Nome da obra
        self.nome_obra = tb.Label(self.root)
        self.nome_obra.place(relx=0.036, rely=0.2, height=64, width=195)
        # self.nome_obra.configure(activebackground="#f9f9f9")
        self.nome_obra.configure(anchor='w')
        # self.nome_obra.configure(background="#f0f0f0")
        self.nome_obra.configure(compound='left')
        # self.nome_obra.configure(disabledforeground="#a3a3a3")
        self.nome_obra.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.nome_obra.configure(foreground="#000000")
        # self.nome_obra.configure(highlightbackground="#d9d9d9")
        # self.nome_obra.configure(highlightcolor="black")
        self.nome_obra.configure(text='''Nome da obra''')
        
        self.name = tb.Entry(self.root)
        self.name.place(relx=0.036, rely=0.311, height=30
                , relwidth=0.386)
        # self.name.configure(background="white")
        # self.name.configure(disabledforeground="#a3a3a3")
        self.name.configure(font="-family {Arial} -size 14 -weight bold")
        # self.name.configure(foreground="#000000")
        # self.name.configure(highlightbackground="#d9d9d9")
        # self.name.configure(highlightcolor="black")
        # self.name.configure(insertbackground="black")
        # self.name.configure(selectbackground="#c4c4c4")
        # self.name.configure(selectforeground="black")
        self.name.configure(textvariable=self.nome_var)
        
        
        
        # URL da obra
        self.url_obra = tb.Label(self.root)
        self.url_obra.place(relx=0.036, rely=0.378, height=64, width=195)
        # self.url_obra.configure(activebackground="#f9f9f9")
        self.url_obra.configure(anchor='w')
        # self.url_obra.configure(background="#f0f0f0")
        self.url_obra.configure(compound='left')
        # self.url_obra.configure(disabledforeground="#a3a3a3")
        self.url_obra.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.url_obra.configure(foreground="#000000")
        # self.url_obra.configure(highlightbackground="#d9d9d9")
        # self.url_obra.configure(highlightcolor="black")
        self.url_obra.configure(text='''URL da obra''')
        
        self.url = tb.Entry(self.root)
        self.url.place(relx=0.036, rely=0.489, height=30
                , relwidth=0.386)
        # self.url.configure(background="white")
        # self.url.configure(disabledforeground="#a3a3a3")
        self.url.configure(font="-family {Arial} -size 14 -weight bold")
        # self.url.configure(foreground="#000000")
        # self.url.configure(highlightbackground="#d9d9d9")
        # self.url.configure(highlightcolor="black")
        # self.url.configure(insertbackground="black")
        # self.url.configure(selectbackground="#c4c4c4")
        # self.url.configure(selectforeground="black")
        self.url.configure(textvariable=self.url_var)
        
        
        
        # Capítulo
        self.cap_obra = tb.Label(self.root)
        self.cap_obra.place(relx=0.036, rely=0.558, height=48, width=195)
        # self.cap_obra.configure(activebackground="#f9f9f9")
        self.cap_obra.configure(anchor='w')
        # self.cap_obra.configure(background="#f0f0f0")
        self.cap_obra.configure(compound='left')
        # self.cap_obra.configure(disabledforeground="#a3a3a3")
        self.cap_obra.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.cap_obra.configure(foreground="#000000")
        # self.cap_obra.configure(highlightbackground="#d9d9d9")
        # self.cap_obra.configure(highlightcolor="black")
        self.cap_obra.configure(text='''Capítulo''')
        
        self.cap = tb.Entry(self.root)
        self.cap.place(relx=0.036, rely=0.667, height=30
                , relwidth=0.386)
        # self.cap.configure(background="white")
        # self.cap.configure(disabledforeground="#a3a3a3")
        self.cap.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.cap.configure(foreground="#000000")
        # self.cap.configure(highlightbackground="#d9d9d9")
        # self.cap.configure(highlightcolor="black")
        # self.cap.configure(insertbackground="black")
        # self.cap.configure(selectbackground="#c4c4c4")
        # self.cap.configure(selectforeground="black")
        self.cap.configure(textvariable=self.capitulo_var)
        self.cap.configure(validate='all')
        self.cap.configure(validatecommand=(self.vcmd1, '%P'))
        
        
        
        # Até qual capítulo baixar
        self.ate_text = tb.Label(self.root)
        self.ate_text.place(relx=0.036, rely=0.734, height=63, width=195)
        # self.ate_text.configure(activebackground="#f9f9f9")
        self.ate_text.configure(anchor='w')
        # self.ate_text.configure(background="#f0f0f0")
        self.ate_text.configure(compound='left')
        # self.ate_text.configure(disabledforeground="#a3a3a3")
        self.ate_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.ate_text.configure(foreground="#000000")
        # self.ate_text.configure(highlightbackground="#d9d9d9")
        # self.ate_text.configure(highlightcolor="black")
        self.ate_text.configure(text='''Até qual capítulo''')
        
        self.ate = tb.Entry(self.root)
        self.ate.place(relx=0.036, rely=0.843, height=30
                , relwidth=0.386)
        # self.ate.configure(background="white")
        # self.ate.configure(disabledforeground="#a3a3a3")
        self.ate.configure(font="-family {Arial} -size 14 -weight bold")
        # self.ate.configure(foreground="#000000")
        # self.ate.configure(highlightbackground="#d9d9d9")
        # self.ate.configure(highlightcolor="black")
        # self.ate.configure(insertbackground="black")
        # self.ate.configure(selectbackground="#c4c4c4")
        # self.ate.configure(selectforeground="black")
        self.ate.configure(textvariable=self.ate_var)
        self.ate.configure(validate='all')
        self.ate.configure(validatecommand=(self.vcmd1, '%P'))
        
        
        
        # Caixa de texto para exibir o caminho da pasta selecionada
        self.selected_folder_text = tb.Entry(self.root)
        self.selected_folder_text.place(relx=0.454, rely=0.751, height=40, relwidth=0.511)
        # self.selected_folder_text.configure(background="white")
        # self.selected_folder_text.configure(disabledforeground="#a3a3a3")
        self.selected_folder_text.configure(font="-family {Arial} -size 14 -weight bold")
        self.selected_folder_text.configure(font="TkFixedFont")
        # self.selected_folder_text.configure(foreground="#000000")
        # self.selected_folder_text.configure(highlightbackground="#d9d9d9")
        # self.selected_folder_text.configure(highlightcolor="black")
        # self.selected_folder_text.configure(insertbackground="black")
        # self.selected_folder_text.configure(selectbackground="#c4c4c4")
        # self.selected_folder_text.configure(selectforeground="black")
        self.selected_folder_text.insert(0, self.folder_selected)
        self.selected_folder_text.configure(state='readonly')
        
        
        
        # Iniciar download
        self.start_download_button = tb.Button(self.root)
        self.start_download_button.place(relx=0.498, rely=0.88, height=44, width=207)
        # self.start_download_button.configure(activebackground="#f0f0f0")
        # self.start_download_button.configure(activeforeground="black")
        # self.start_download_button.configure(background="#f0f0f0")
        self.start_download_button.configure(compound='left')
        # self.start_download_button.configure(disabledforeground="#a3a3a3")
        # self.start_download_button.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.start_download_button.configure(foreground="#000000")
        # self.start_download_button.configure(highlightbackground="#d9d9d9")
        # self.start_download_button.configure(highlightcolor="black")
        # self.start_download_button.configure(pady="0")
        self.start_download_button.configure(text='''Iniciar Download''')
        self.start_download_button.configure(command=self.start_download)
        self.start_download_button.configure(style="b1.TButton")
        
        
        
        # Salvar configurações
        self.save_button = tb.Button(self.root)
        self.save_button.place(relx=0.712, rely=0.88, height=44, width=237)
        # self.save_button.configure(activebackground="#f0f0f0")
        # self.save_button.configure(activeforeground="black")
        # self.save_button.configure(background="#f0f0f0")
        # self.save_button.configure(compound='left')
        # self.save_button.configure(disabledforeground="#a3a3a3")
        # self.save_button.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.save_button.configure(foreground="#000000")
        # self.save_button.configure(highlightbackground="#d9d9d9")
        # self.save_button.configure(highlightcolor="black")
        # self.save_button.configure(pady="0")
        self.save_button.configure(text='''Salvar Configurações''')
        self.save_button.configure(command=self.save_settings)
        self.save_button.configure(style="b1.TButton")
        
        
        # Carrega os abas de opções
        self.not_options()
        
        # Carrega as opções
        self.options_agreg_config()
        self.options_config()
        self.options_config_rede()
        self.options_theme()
        self.options_info()
        self.options_about()
        
        # Animação text
        self.app_instance.animation_text()
        
    
    def not_options(self):
        # Lista de opções
        self.TNotebook1 = ttk.Notebook(self.root)
        self.TNotebook1.place(relx=0.454, rely=0.043, relheight=0.657
                , relwidth=0.512)
        self.TNotebook1.configure(takefocus="")
        
        
        
        # Configure o tamanho da fonte para as abas do notebook
        estilo_abas = ttk.Style()
        estilo_abas.configure('TNotebook.Tab', font=('Arial', 11, 'bold'))  # Substitua 'Arial' pelo tipo de fonte desejado e 12 pelo tamanho desejado
        
        
        
        self.TNotebook1_t1 = tb.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t1, padding=3)
        self.TNotebook1.tab(0, text='''Agregador''', compound="left"
                ,underline='''-1''', )
        # self.TNotebook1_t1.configure(background="#f0f0f0")
        # self.TNotebook1_t1.configure(highlightbackground="#d9d9d9")
        # self.TNotebook1_t1.configure(highlightcolor="black")
        
        
        
        self.TNotebook1_t2 = tb.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t2, padding=3)
        self.TNotebook1.tab(1, text='''Configurações''', compound="left"
                ,underline='''-1''', )
        # self.TNotebook1_t2.configure(background="#f0f0f0")
        # self.TNotebook1_t2.configure(highlightbackground="#d9d9d9")
        # self.TNotebook1_t2.configure(highlightcolor="black")
        
        
        
        self.TNotebook1_t3 = tb.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t3, padding=3)
        self.TNotebook1.tab(2, text='''Configurações de rede''', compound="left"
                ,underline='''-1''', )
        # self.TNotebook1_t3.configure(background="#f0f0f0")
        # self.TNotebook1_t3.configure(highlightbackground="#d9d9d9")
        # self.TNotebook1_t3.configure(highlightcolor="black")
        
        
        
        self.TNotebook1_t4 = tb.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t4, padding=3)
        self.TNotebook1.tab(3, text='''Temas''', compound="left"
                ,underline='''-1''', )
        # self.TNotebook1_t4.configure(background="#f0f0f0")
        # self.TNotebook1_t4.configure(highlightbackground="#d9d9d9")
        # self.TNotebook1_t4.configure(highlightcolor="black")
        
        
        
        self.TNotebook1_t5 = tb.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t5, padding=3)
        self.TNotebook1.tab(4, text='''Info''', compound="left"
                ,underline='''-1''', )
        # self.TNotebook1_t5.configure(background="#f0f0f0")
        # self.TNotebook1_t5.configure(highlightbackground="#d9d9d9")
        # self.TNotebook1_t5.configure(highlightcolor="black")
        
        
        
        self.TNotebook1_t6 = tb.Frame(self.TNotebook1)
        self.TNotebook1.add(self.TNotebook1_t6, padding=3)
        self.TNotebook1.tab(5, text='''Sobre''', compound="left"
                ,underline='''-1''', )
        # self.TNotebook1_t5.configure(background="#f0f0f0")
        # self.TNotebook1_t5.configure(highlightbackground="#d9d9d9")
        # self.TNotebook1_t5.configure(highlightcolor="black")
    
    
    def options_agreg_config(self):
        # Compactar
        self.comapt_text = tb.Label(self.TNotebook1_t1)
        self.comapt_text.place(relx=0.035, rely=0.036, height=64, width=195)
        # self.comapt_text.configure(activebackground="#f9f9f9")
        self.comapt_text.configure(anchor='w')
        # self.comapt_text.configure(background="#f0f0f0")
        self.comapt_text.configure(compound='left')
        # self.comapt_text.configure(disabledforeground="#a3a3a3")
        self.comapt_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.comapt_text.configure(foreground="#000000")
        # self.comapt_text.configure(highlightbackground="#d9d9d9")
        # self.comapt_text.configure(highlightcolor="black")
        self.comapt_text.configure(text='''Compactar''')
        
        self.comapt_check = tb.Checkbutton(self.TNotebook1_t1)
        self.comapt_check.place(relx=0.053, rely=0.211, relheight=0.089
                , relwidth=0.263)
        # self.comapt_check.configure(activebackground="#f0f0f0")
        # self.comapt_check.configure(activeforeground="black")
        # self.comapt_check.configure(anchor='w')
        # self.comapt_check.configure(background="#f0f0f0")
        self.comapt_check.configure(compound='left')
        # self.comapt_check.configure(disabledforeground="#a3a3a3")
        # self.comapt_check.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.comapt_check.configure(foreground="#000000")
        # self.comapt_check.configure(highlightbackground="#d9d9d9")
        # self.comapt_check.configure(highlightcolor="black")
        # self.comapt_check.configure(justify='left')
        # self.comapt_check.configure(selectcolor="#f0f0f0")
        self.comapt_check.configure(text='''Compactar''')
        self.comapt_check.configure(variable=self.compact_var)
        self.comapt_check.configure(command=self.update_checkboxes_compact)
        self.comapt_check.configure(style="c1.TCheckbutton")
        
        
        
        # Lista com as extensões de compactação disponíveis
        self.compact_extensions_text = tb.Label(self.TNotebook1_t1)
        self.compact_extensions_text.place(relx=0.053, rely=0.321, height=64, width=266)
        # self.compact_extensions_text.configure(activebackground="#f9f9f9")
        self.compact_extensions_text.configure(anchor='w')
        # self.compact_extensions_text.configure(background="#f0f0f0")
        self.compact_extensions_text.configure(compound='left')
        # self.compact_extensions_text.configure(disabledforeground="#a3a3a3")
        self.compact_extensions_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.compact_extensions_text.configure(foreground="#000000")
        # self.compact_extensions_text.configure(highlightbackground="#d9d9d9")
        # self.compact_extensions_text.configure(highlightcolor="black")
        self.compact_extensions_text.configure(text='''Extensão da compactação''')
        
        compact_extensions = [".zip", ".rar", ".cbz"]
        
        self.comapct_extension_combobox = ttk.Combobox(self.TNotebook1_t1)
        self.comapct_extension_combobox.place(relx=0.053, rely=0.5, relheight=0.118
                , relwidth=0.462)
        self.comapct_extension_combobox.configure(font="-family {Arial} -size 12 -weight bold")
        self.comapct_extension_combobox.configure(textvariable=self.compact_extension_var)
        self.comapct_extension_combobox.configure(values=compact_extensions)
        self.comapct_extension_combobox.configure(validate='all')
        self.comapct_extension_combobox.configure(validatecommand=(self.vcmd1, '%P'))
        
        
        
        # Lista com as extensões de saída disponíveis
        self.extension_text = tb.Label(self.TNotebook1_t1)
        self.extension_text.place(relx=0.053, rely=0.607, height=64, width=266)
        # self.extension_text.configure(activebackground="#f9f9f9")
        self.extension_text.configure(anchor='w')
        # self.extension_text.configure(background="#f0f0f0")
        self.extension_text.configure(compound='left')
        # self.extension_text.configure(disabledforeground="#a3a3a3")
        self.extension_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.extension_text.configure(foreground="#000000")
        # self.extension_text.configure(highlightbackground="#d9d9d9")
        # self.extension_text.configure(highlightcolor="black")
        self.extension_text.configure(text='''Extensão da saída''')
        
        extensions = [".png", ".jpg"]
        
        self.extension_combobox = ttk.Combobox(self.TNotebook1_t1)
        self.extension_combobox.place(relx=0.053, rely=0.786, relheight=0.118
                , relwidth=0.462)
        self.extension_combobox.configure(font="-family {Arial} -size 12 -weight bold")
        self.extension_combobox.configure(textvariable=self.extension_var)
        self.extension_combobox.configure(values=extensions)
        self.extension_combobox.configure(validate='all')
        self.extension_combobox.configure(validatecommand=(self.vcmd1, '%P'))
        
        
        
        # Agregador site
        self.url_open = tb.Button(self.TNotebook1_t1)
        self.url_open.place(relx=0.648, rely=0.143, height=44, width=137)
        # self.url_open.configure(activebackground="#f0f0f0")
        # self.url_open.configure(activeforeground="black")
        # self.url_open.configure(background="#f0f0f0")
        self.url_open.configure(compound='left')
        # self.url_open.configure(disabledforeground="#a3a3a3")
        # self.url_open.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.url_open.configure(foreground="#000000")
        # self.url_open.configure(highlightbackground="#d9d9d9")
        # self.url_open.configure(highlightcolor="black")
        # self.url_open.configure(pady="0")
        self.url_open.configure(text='''Ir para o site''')
        self.url_open.configure(command=self.site_url_open)
        self.url_open.configure(style="b1.TButton")
        
        
        
        # Selecionar pasta
        self.select_folder_button = tb.Button(self.TNotebook1_t1)
        self.select_folder_button.place(relx=0.613, rely=0.429, height=44, width=177)
        # self.select_folder_button.configure(activebackground="#f0f0f0")
        # self.select_folder_button.configure(activeforeground="black")
        # self.select_folder_button.configure(background="#f0f0f0")
        self.select_folder_button.configure(compound='left')
        # self.select_folder_button.configure(disabledforeground="#a3a3a3")
        # self.select_folder_button.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.select_folder_button.configure(foreground="#000000")
        # self.select_folder_button.configure(highlightbackground="#d9d9d9")
        # self.select_folder_button.configure(highlightcolor="black")
        # self.select_folder_button.configure(pady="0")
        self.select_folder_button.configure(text='''Selecionar pasta''')
        self.select_folder_button.configure(command=self.select_folder)
        self.select_folder_button.configure(style="b1.TButton")
        
        
        
        # Ir para a pasta selecionada
        self.select_folder_go_button = tb.Button(self.TNotebook1_t1)
        self.select_folder_go_button.place(relx=0.639, rely=0.714, height=44, width=147)
        # self.select_folder_go_button.configure(activebackground="#f0f0f0")
        # self.select_folder_go_button.configure(activeforeground="black")
        # self.select_folder_go_button.configure(background="#f0f0f0")
        self.select_folder_go_button.configure(compound='left')
        # self.select_folder_go_button.configure(disabledforeground="#a3a3a3")
        # self.select_folder_go_button.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.select_folder_go_button.configure(foreground="#000000")
        # self.select_folder_go_button.configure(highlightbackground="#d9d9d9")
        # self.select_folder_go_button.configure(highlightcolor="black")
        # self.select_folder_go_button.configure(pady="0")
        self.select_folder_go_button.configure(text='''Ir para a pasta''')
        self.select_folder_go_button.configure(command=self.select_folder_go)
        self.select_folder_go_button.configure(style="b1.TButton")


    def options_config(self):
        # Auto save
        self.check_auto_save_text = tb.Label(self.TNotebook1_t2)
        self.check_auto_save_text.place(relx=0.035, rely=0.036, height=64, width=196)
        # self.check_auto_save_text.configure(activebackground="#f0f0f0")
        self.check_auto_save_text.configure(anchor='w')
        # self.check_auto_save_text.configure(background="#f0f0f0")
        self.check_auto_save_text.configure(compound='left')
        # self.check_auto_save_text.configure(disabledforeground="#a3a3a3")
        self.check_auto_save_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.check_auto_save_text.configure(foreground="#000000")
        # self.check_auto_save_text.configure(highlightbackground="#d9d9d9")
        # self.check_auto_save_text.configure(highlightcolor="black")
        self.check_auto_save_text.configure(text='''Auto salvar''')
        
        self.check_auto_save = tb.Checkbutton(self.TNotebook1_t2)
        self.check_auto_save.place(relx=0.07, rely=0.2, relheight=0.089
                , relwidth=0.264)
        # self.check_auto_save.configure(activebackground="#f0f0f0")
        # self.check_auto_save.configure(activeforeground="black")
        # self.check_auto_save.configure(anchor='w')
        # self.check_auto_save.configure(background="#f0f0f0")
        self.check_auto_save.configure(compound='left')
        # self.check_auto_save.configure(disabledforeground="#a3a3a3")
        # self.check_auto_save.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.check_auto_save.configure(foreground="#000000")
        # self.check_auto_save.configure(highlightbackground="#d9d9d9")
        # self.check_auto_save.configure(highlightcolor="black")
        # self.check_auto_save.configure(justify='left')
        # self.check_auto_save.configure(selectcolor="#f0f0f0")
        self.check_auto_save.configure(text='''Auto salvar''')
        self.check_auto_save.configure(variable=self.auto_save)
        self.check_auto_save.configure(command=self.update_checkboxes_save)
        self.check_auto_save.configure(style="c1.TCheckbutton")
        
        
        
        # Info
        self.debug_check_text = tb.Label(self.TNotebook1_t2)
        self.debug_check_text.place(relx=0.035, rely=0.286, height=64, width=196)
        # self.debug_check_text.configure(activebackground="#f0f0f0")
        self.debug_check_text.configure(anchor='w')
        # self.debug_check_text.configure(background="#f0f0f0")
        self.debug_check_text.configure(compound='left')
        # self.debug_check_text.configure(disabledforeground="#a3a3a3")
        self.debug_check_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.debug_check_text.configure(foreground="#000000")
        # self.debug_check_text.configure(highlightbackground="#d9d9d9")
        # self.debug_check_text.configure(highlightcolor="black")
        self.debug_check_text.configure(text='''Info''')
        
        self.debug_check = tb.Checkbutton(self.TNotebook1_t2)
        self.debug_check.place(relx=0.053, rely=0.464, relheight=0.089
                , relwidth=0.264)
        # self.debug_check.configure(activebackground="#f0f0f0")
        # self.debug_check.configure(activeforeground="black")
        # self.debug_check.configure(anchor='w')
        # self.debug_check.configure(background="#f0f0f0")
        self.debug_check.configure(compound='left')
        # self.debug_check.configure(disabledforeground="#a3a3a3")
        # self.debug_check.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.debug_check.configure(foreground="#000000")
        # self.debug_check.configure(highlightbackground="#d9d9d9")
        # self.debug_check.configure(highlightcolor="black")
        # self.debug_check.configure(justify='left')
        # self.debug_check.configure(selectcolor="#f0f0f0")
        self.debug_check.configure(text='''Info''')
        self.debug_check.configure(variable=self.debug_var)
        self.debug_check.configure(command=self.update_checkboxes_debug)
        self.debug_check.configure(style="c1.TCheckbutton")
        
        
        
        # Debug
        self.debug2_check_text = tb.Label(self.TNotebook1_t2)
        self.debug2_check_text.place(relx=0.035, rely=0.571, height=64, width=196)
        # self.debug2_check_text.configure(activebackground="#f0f0f0")
        self.debug2_check_text.configure(anchor='w')
        # self.debug2_check_text.configure(background="#f0f0f0")
        self.debug2_check_text.configure(compound='left')
        # self.debug2_check_text.configure(disabledforeground="#a3a3a3")
        self.debug2_check_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.debug2_check_text.configure(foreground="#000000")
        # self.debug2_check_text.configure(highlightbackground="#d9d9d9")
        # self.debug2_check_text.configure(highlightcolor="black")
        self.debug2_check_text.configure(text='''Debug''')
        
        self.debug2_check = tb.Checkbutton(self.TNotebook1_t2)
        self.debug2_check.place(relx=0.053, rely=0.75, relheight=0.089
                , relwidth=0.264)
        # self.debug2_check.configure(activebackground="#f0f0f0")
        # self.debug2_check.configure(activeforeground="black")
        # self.debug2_check.configure(anchor='w')
        # self.debug2_check.configure(background="#f0f0f0")
        self.debug2_check.configure(compound='left')
        # self.debug2_check.configure(disabledforeground="#a3a3a3")
        # self.debug2_check.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.debug2_check.configure(foreground="#000000")
        # self.debug2_check.configure(highlightbackground="#d9d9d9")
        # self.debug2_check.configure(highlightcolor="black")
        # self.debug2_check.configure(justify='left')
        # self.debug2_check.configure(selectcolor="#f0f0f0")
        self.debug2_check.configure(text='''Debug''')
        self.debug2_check.configure(variable=self.debug2_var)
        self.debug2_check.configure(command=self.update_checkboxes_debug2)
        self.debug2_check.configure(style="c1.TCheckbutton")
        
        
        
        # Navegador
        self.nav_check_text = tb.Label(self.TNotebook1_t2)
        self.nav_check_text.place(relx=0.438, rely=0.036, height=64, width=306)
        # self.nav_check_text.configure(activebackground="#f0f0f0")
        self.nav_check_text.configure(anchor='w')
        # self.nav_check_text.configure(background="#f0f0f0")
        self.nav_check_text.configure(compound='left')
        # self.nav_check_text.configure(disabledforeground="#a3a3a3")
        self.nav_check_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.nav_check_text.configure(foreground="#000000")
        # self.nav_check_text.configure(highlightbackground="#d9d9d9")
        # self.nav_check_text.configure(highlightcolor="black")
        self.nav_check_text.configure(text='''Navegador em segundo plano''')
        
        self.nav_check = tb.Checkbutton(self.TNotebook1_t2)
        self.nav_check.place(relx=0.455, rely=0.214, relheight=0.089
                , relwidth=0.545)
        # self.nav_check.configure(activebackground="#f0f0f0")
        # self.nav_check.configure(activeforeground="black")
        # self.nav_check.configure(anchor='w')
        # self.nav_check.configure(background="#f0f0f0")
        self.nav_check.configure(compound='left')
        # self.nav_check.configure(disabledforeground="#a3a3a3")
        # self.nav_check.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.nav_check.configure(foreground="#000000")
        # self.nav_check.configure(highlightbackground="#d9d9d9")
        # self.nav_check.configure(highlightcolor="black")
        # self.nav_check.configure(justify='left')
        # self.nav_check.configure(selectcolor="#f0f0f0")
        self.nav_check.configure(text='''Navegador em segundo plano''')
        self.nav_check.configure(variable=self.headless_var)
        self.nav_check.configure(command=self.update_checkboxes_nav)
        self.nav_check.configure(style="c1.TCheckbutton")
        
        
        
        # Change log
        self.change_log_text = tb.Label(self.TNotebook1_t2)
        self.change_log_text.place(relx=0.438, rely=0.286, height=64, width=196)
        # self.change_log_text.configure(activebackground="#f0f0f0")
        self.change_log_text.configure(anchor='w')
        # self.change_log_text.configure(background="#f0f0f0")
        self.change_log_text.configure(compound='left')
        # self.change_log_text.configure(disabledforeground="#a3a3a3")
        self.change_log_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.change_log_text.configure(foreground="#000000")
        # self.change_log_text.configure(highlightbackground="#d9d9d9")
        # self.change_log_text.configure(highlightcolor="black")
        self.change_log_text.configure(text='''Change Log''')
        
        self.change_log = tb.Checkbutton(self.TNotebook1_t2)
        self.change_log.place(relx=0.455, rely=0.464, relheight=0.089
                , relwidth=0.264)
        # self.change_log.configure(activebackground="#f0f0f0")
        # self.change_log.configure(activeforeground="black")
        # self.change_log.configure(anchor='w')
        # self.change_log.configure(background="#f0f0f0")
        self.change_log.configure(compound='left')
        # self.change_log.configure(disabledforeground="#a3a3a3")
        # self.change_log.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.change_log.configure(foreground="#000000")
        # self.change_log.configure(highlightbackground="#d9d9d9")
        # self.change_log.configure(highlightcolor="black")
        # self.change_log.configure(justify='left')
        # self.change_log.configure(selectcolor="#f0f0f0")
        self.change_log.configure(text='''Change Log''')
        self.change_log.configure(variable=self.change_log_var)
        self.change_log.configure(command=self.update_checkboxes_debug)
        self.change_log.configure(style="c1.TCheckbutton")
        
        
        
        # Resetar Configurações
        self.reset_config_button = tb.Button(self.TNotebook1_t2)
        self.reset_config_button.place(relx=0.49, rely=0.679, height=44, width=247)
        # self.reset_config_button.configure(activebackground="#f0f0f0")
        # self.reset_config_button.configure(activeforeground="black")
        # self.reset_config_button.configure(background="#f0f0f0")
        self.reset_config_button.configure(compound='left')
        # self.reset_config_button.configure(disabledforeground="#a3a3a3")
        # self.reset_config_button.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.reset_config_button.configure(foreground="#000000")
        # self.reset_config_button.configure(highlightbackground="#d9d9d9")
        # self.reset_config_button.configure(highlightcolor="black")
        # self.reset_config_button.configure(pady="0")
        self.reset_config_button.configure(text='''Resetar Configurações''')
        self.reset_config_button.configure(command=self.reset_config)
        self.reset_config_button.configure(style="b1.TButton")


    def options_config_rede(self):
        # Opções de rede
        self.net_option_text = tb.Label(self.TNotebook1_t3)
        self.net_option_text.place(relx=0.053, rely=0.071, height=34, width=246)
        # self.net_option_text.configure(activebackground="#f0f0f0")
        self.net_option_text.configure(anchor='w')
        # self.net_option_text.configure(background="#f0f0f0")
        self.net_option_text.configure(compound='left')
        # self.net_option_text.configure(disabledforeground="#a3a3a3")
        self.net_option_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.net_option_text.configure(foreground="#000000")
        # self.net_option_text.configure(highlightbackground="#d9d9d9")
        # self.net_option_text.configure(highlightcolor="black")
        self.net_option_text.configure(text='''Ativar opções de rede''')
        
        self.net_option = tb.Checkbutton(self.TNotebook1_t3)
        self.net_option.place(relx=0.07, rely=0.214, relheight=0.089
                , relwidth=0.422)
        # self.net_option.configure(activebackground="#f0f0f0")
        # self.net_option.configure(activeforeground="black")
        # self.net_option.configure(anchor='w')
        # self.net_option.configure(background="#f0f0f0")
        self.net_option.configure(compound='left')
        # self.net_option.configure(disabledforeground="#a3a3a3")
        # self.net_option.configure(font="-family {Segoe UI} -size 14 -weight bold")
        # self.net_option.configure(foreground="#000000")
        # self.net_option.configure(highlightbackground="#d9d9d9")
        # self.net_option.configure(highlightcolor="black")
        # self.net_option.configure(justify='left')
        # self.net_option.configure(selectcolor="#f0f0f0")
        self.net_option.configure(text='''Ativar opções de rede''')
        self.net_option.configure(variable=self.net_option_var)
        self.net_option.configure(style="c1.TCheckbutton")
        
        
        
        # Limitar download
        self.net_limit_down_text = tb.Label(self.TNotebook1_t3)
        self.net_limit_down_text.place(relx=0.053, rely=0.393, height=34, width=246)
        # self.net_limit_down_text.configure(activebackground="#f0f0f0")
        self.net_limit_down_text.configure(anchor='w')
        # self.net_limit_down_text.configure(background="#f0f0f0")
        self.net_limit_down_text.configure(compound='left')
        # self.net_limit_down_text.configure(disabledforeground="#a3a3a3")
        self.net_limit_down_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.net_limit_down_text.configure(foreground="#000000")
        # self.net_limit_down_text.configure(highlightbackground="#d9d9d9")
        # self.net_limit_down_text.configure(highlightcolor="black")
        self.net_limit_down_text.configure(text='''Limitar download''')
        
        self.net_limit_down = tb.Spinbox(self.TNotebook1_t3, from_=1.0, to=999999999.0)
        self.net_limit_down.place(relx=0.088, rely=0.536, relheight=0.1
                , relwidth=0.236)
        # self.net_limit_down.configure(activebackground="#f9f9f9")
        # self.net_limit_down.configure(background="white")
        # self.net_limit_down.configure(buttonbackground="#d9d9d9")
        # self.net_limit_down.configure(disabledforeground="#a3a3a3")
        self.net_limit_down.configure(font=("Segoe UI", 10, 'bold'))
        # self.net_limit_down.configure(foreground="black")
        # self.net_limit_down.configure(highlightbackground="black")
        # self.net_limit_down.configure(highlightcolor="black")
        # self.net_limit_down.configure(insertbackground="black")
        # self.net_limit_down.configure(selectbackground="#c4c4c4")
        # self.net_limit_down.configure(selectforeground="black")
        self.net_limit_down.configure(textvariable=self.net_limit_down_var)
        self.net_limit_down.configure(validate='all')
        self.net_limit_down.configure(validatecommand=(self.vcmd1, '%P'))
        
        
        
        # Limitar upload
        self.net_limit_up_text = tb.Label(self.TNotebook1_t3)
        self.net_limit_up_text.place(relx=0.053, rely=0.679, height=34, width=246)
        # self.net_limit_up_text.configure(activebackground="#f0f0f0")
        self.net_limit_up_text.configure(anchor='w')
        # self.net_limit_up_text.configure(background="#f0f0f0")
        self.net_limit_up_text.configure(compound='left')
        # self.net_limit_up_text.configure(disabledforeground="#a3a3a3")
        self.net_limit_up_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.net_limit_up_text.configure(foreground="#000000")
        # self.net_limit_up_text.configure(highlightbackground="#d9d9d9")
        # self.net_limit_up_text.configure(highlightcolor="black")
        self.net_limit_up_text.configure(text='''Limitar upload''')
        
        self.net_limit_up = tb.Spinbox(self.TNotebook1_t3, from_=1.0, to=999999999.0)
        self.net_limit_up.place(relx=0.088, rely=0.821, relheight=0.1
                , relwidth=0.236)
        # self.net_limit_up.configure(activebackground="#f9f9f9")
        # self.net_limit_up.configure(background="white")
        # self.net_limit_up.configure(buttonbackground="#d9d9d9")
        # self.net_limit_up.configure(disabledforeground="#a3a3a3")
        self.net_limit_up.configure(font=("Segoe UI", 10, 'bold'))
        # self.net_limit_up.configure(foreground="black")
        # self.net_limit_up.configure(highlightbackground="black")
        # self.net_limit_up.configure(highlightcolor="black")
        # self.net_limit_up.configure(insertbackground="black")
        # self.net_limit_up.configure(selectbackground="#c4c4c4")
        # self.net_limit_up.configure(selectforeground="black")
        self.net_limit_up.configure(textvariable=self.net_limit_up_var)
        self.net_limit_up.configure(validate='all')
        self.net_limit_up.configure(validatecommand=(self.vcmd1, '%P'))
        
        
        
        # Latência
        self.net_lat_text = tb.Label(self.TNotebook1_t3)
        self.net_lat_text.place(relx=0.543, rely=0.071, height=34, width=246)
        # self.net_lat_text.configure(activebackground="#f0f0f0")
        self.net_lat_text.configure(anchor='w')
        # self.net_lat_text.configure(background="#f0f0f0")
        self.net_lat_text.configure(compound='left')
        # self.net_lat_text.configure(disabledforeground="#a3a3a3")
        self.net_lat_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.net_lat_text.configure(foreground="#000000")
        # self.net_lat_text.configure(highlightbackground="#d9d9d9")
        # self.net_lat_text.configure(highlightcolor="black")
        self.net_lat_text.configure(text='''Latência''')
        
        self.net_lat = tb.Spinbox(self.TNotebook1_t3, from_=1.0, to=999999.0)
        self.net_lat.place(relx=0.578, rely=0.214, relheight=0.1
                , relwidth=0.236)
        # self.net_lat.configure(activebackground="#f9f9f9")
        # self.net_lat.configure(background="white")
        # self.net_lat.configure(buttonbackground="#d9d9d9")
        # self.net_lat.configure(disabledforeground="#a3a3a3")
        self.net_lat.configure(font=("Segoe UI", 10, 'bold'))
        # self.net_lat.configure(foreground="black")
        # self.net_lat.configure(highlightbackground="black")
        # self.net_lat.configure(highlightcolor="black")
        # self.net_lat.configure(insertbackground="black")
        # self.net_lat.configure(selectbackground="#c4c4c4")
        # self.net_lat.configure(selectforeground="black")
        self.net_lat.configure(textvariable=self.net_lat_var)
        self.net_lat.configure(validate='all')
        self.net_lat.configure(validatecommand=(self.vcmd1, '%P'))

    
    def options_theme(self):
        # Temas
        self.light_text = tb.Label(self.TNotebook1_t4)
        self.light_text.place(relx=0.088, rely=0.0, height=33, width=66)
        # self.light_text.configure(activebackground="#f0f0f0")
        self.light_text.configure(anchor='w')
        # self.light_text.configure(background="#f0f0f0")
        self.light_text.configure(compound='left')
        # self.light_text.configure(disabledforeground="#a3a3a3")
        self.light_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.light_text.configure(foreground="#000000")
        # self.light_text.configure(highlightbackground="#d9d9d9")
        # self.light_text.configure(highlightcolor="black")
        self.light_text.configure(text='''Light''')
        
        self.dark_text = tb.Label(self.TNotebook1_t4)
        self.dark_text.place(relx=0.788, rely=0.0, height=33, width=56)
        # self.dark_text.configure(activebackground="#f0f0f0")
        self.dark_text.configure(anchor='w')
        # self.dark_text.configure(background="#f0f0f0")
        self.dark_text.configure(compound='left')
        # self.dark_text.configure(disabledforeground="#a3a3a3")
        self.dark_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.dark_text.configure(foreground="#000000")
        # self.dark_text.configure(highlightbackground="#d9d9d9")
        # self.dark_text.configure(highlightcolor="black")
        self.dark_text.configure(text='''Dark''')
        
        
        
        self.theme_1 = tb.Button(self.TNotebook1_t4)
        self.theme_1.place(relx=0.035, rely=0.143, height=34, width=97)
        # self.theme_1.configure(activebackground="#f0f0f0")
        # self.theme_1.configure(activeforeground="black")
        # self.theme_1.configure(background="#f0f0f0")
        self.theme_1.configure(compound='left')
        # self.theme_1.configure(disabledforeground="#a3a3a3")
        # self.theme_1.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_1.configure(foreground="#000000")
        # self.theme_1.configure(highlightbackground="#d9d9d9")
        # self.theme_1.configure(highlightcolor="black")
        # self.theme_1.configure(pady="0")
        self.theme_1.configure(text='''Cosmo''')
        self.theme_1.configure(command=self.theme_1_b)
        self.theme_1.configure(style="b2.TButton")
        
        
        self.theme_2 = tb.Button(self.TNotebook1_t4)
        self.theme_2.place(relx=0.245, rely=0.143, height=34, width=97)
        # self.theme_2.configure(activebackground="#f0f0f0")
        # self.theme_2.configure(activeforeground="black")
        # self.theme_2.configure(background="#f0f0f0")
        self.theme_2.configure(compound='left')
        # self.theme_2.configure(disabledforeground="#a3a3a3")
        # self.theme_2.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_2.configure(foreground="#000000")
        # self.theme_2.configure(highlightbackground="#d9d9d9")
        # self.theme_2.configure(highlightcolor="black")
        # self.theme_2.configure(pady="0")
        self.theme_2.configure(text='''Flatly''')
        self.theme_2.configure(command=self.theme_2_b)
        self.theme_2.configure(style="b2.TButton")
        
        
        self.theme_3 = tb.Button(self.TNotebook1_t4)
        self.theme_3.place(relx=0.035, rely=0.286, height=34, width=97)
        # self.theme_3.configure(activebackground="#f0f0f0")
        # self.theme_3.configure(activeforeground="black")
        # self.theme_3.configure(background="#f0f0f0")
        self.theme_3.configure(compound='left')
        # self.theme_3.configure(disabledforeground="#a3a3a3")
        # self.theme_3.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_3.configure(foreground="#000000")
        # self.theme_3.configure(highlightbackground="#d9d9d9")
        # self.theme_3.configure(highlightcolor="black")
        # self.theme_3.configure(pady="0")
        self.theme_3.configure(text='''Litera''')
        self.theme_3.configure(command=self.theme_3_b)
        self.theme_3.configure(style="b2.TButton")
        
        
        self.theme_4 = tb.Button(self.TNotebook1_t4)
        self.theme_4.place(relx=0.245, rely=0.286, height=34, width=97)
        # self.theme_4.configure(activebackground="#f0f0f0")
        # self.theme_4.configure(activeforeground="black")
        # self.theme_4.configure(background="#f0f0f0")
        self.theme_4.configure(compound='left')
        # self.theme_4.configure(disabledforeground="#a3a3a3")
        # self.theme_4.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_4.configure(foreground="#000000")
        # self.theme_4.configure(highlightbackground="#d9d9d9")
        # self.theme_4.configure(highlightcolor="black")
        # self.theme_4.configure(pady="0")
        self.theme_4.configure(text='''Journal''')
        self.theme_4.configure(command=self.theme_4_b)
        self.theme_4.configure(style="b2.TButton")
        
        
        self.theme_5 = tb.Button(self.TNotebook1_t4)
        self.theme_5.place(relx=0.035, rely=0.429, height=34, width=97)
        # self.theme_5.configure(activebackground="#f0f0f0")
        # self.theme_5.configure(activeforeground="black")
        # self.theme_5.configure(background="#f0f0f0")
        self.theme_5.configure(compound='left')
        # self.theme_5.configure(disabledforeground="#a3a3a3")
        # self.theme_5.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_5.configure(foreground="#000000")
        # self.theme_5.configure(highlightbackground="#d9d9d9")
        # self.theme_5.configure(highlightcolor="black")
        # self.theme_5.configure(pady="0")
        self.theme_5.configure(text='''Lumen''')
        self.theme_5.configure(command=self.theme_5_b)
        self.theme_5.configure(style="b2.TButton")
        
        
        self.theme_6 = tb.Button(self.TNotebook1_t4)
        self.theme_6.place(relx=0.245, rely=0.429, height=34, width=97)
        # self.theme_6.configure(activebackground="#f0f0f0")
        # self.theme_6.configure(activeforeground="black")
        # self.theme_6.configure(background="#f0f0f0")
        self.theme_6.configure(compound='left')
        # self.theme_6.configure(disabledforeground="#a3a3a3")
        # self.theme_6.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_6.configure(foreground="#000000")
        # self.theme_6.configure(highlightbackground="#d9d9d9")
        # self.theme_6.configure(highlightcolor="black")
        # self.theme_6.configure(pady="0")
        self.theme_6.configure(text='''Minty''')
        self.theme_6.configure(command=self.theme_6_b)
        self.theme_6.configure(style="b2.TButton")
        
        
        self.theme_7 = tb.Button(self.TNotebook1_t4)
        self.theme_7.place(relx=0.035, rely=0.571, height=34, width=97)
        # self.theme_7.configure(activebackground="#f0f0f0")
        # self.theme_7.configure(activeforeground="black")
        # self.theme_7.configure(background="#f0f0f0")
        self.theme_7.configure(compound='left')
        # self.theme_7.configure(disabledforeground="#a3a3a3")
        # self.theme_7.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_7.configure(foreground="#000000")
        # self.theme_7.configure(highlightbackground="#d9d9d9")
        # self.theme_7.configure(highlightcolor="black")
        # self.theme_7.configure(pady="0")
        self.theme_7.configure(text='''Pulse''')
        self.theme_7.configure(command=self.theme_7_b)
        self.theme_7.configure(style="b2.TButton")
        
        
        self.theme_8 = tb.Button(self.TNotebook1_t4)
        self.theme_8.place(relx=0.245, rely=0.571, height=34, width=97)
        # self.theme_8.configure(activebackground="#f0f0f0")
        # self.theme_8.configure(activeforeground="black")
        # self.theme_8.configure(background="#f0f0f0")
        self.theme_8.configure(compound='left')
        # self.theme_8.configure(disabledforeground="#a3a3a3")
        # self.theme_8.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_8.configure(foreground="#000000")
        # self.theme_8.configure(highlightbackground="#d9d9d9")
        # self.theme_8.configure(highlightcolor="black")
        # self.theme_8.configure(pady="0")
        self.theme_8.configure(text='''SandStone''')
        self.theme_8.configure(command=self.theme_8_b)
        self.theme_8.configure(style="b2.TButton")
        
        
        self.theme_9 = tb.Button(self.TNotebook1_t4)
        self.theme_9.place(relx=0.035, rely=0.714, height=34, width=97)
        # self.theme_9.configure(activebackground="#f0f0f0")
        # self.theme_9.configure(activeforeground="black")
        # self.theme_9.configure(background="#f0f0f0")
        self.theme_9.configure(compound='left')
        # self.theme_9.configure(disabledforeground="#a3a3a3")
        # self.theme_9.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_9.configure(foreground="#000000")
        # self.theme_9.configure(highlightbackground="#d9d9d9")
        # self.theme_9.configure(highlightcolor="black")
        # self.theme_9.configure(pady="0")
        self.theme_9.configure(text='''United''')
        self.theme_9.configure(command=self.theme_9_b)
        self.theme_9.configure(style="b2.TButton")
        
        
        self.theme_10 = tb.Button(self.TNotebook1_t4)
        self.theme_10.place(relx=0.245, rely=0.714, height=34, width=97)
        # self.theme_10.configure(activebackground="#f0f0f0")
        # self.theme_10.configure(activeforeground="black")
        # self.theme_10.configure(background="#f0f0f0")
        self.theme_10.configure(compound='left')
        # self.theme_10.configure(disabledforeground="#a3a3a3")
        # self.theme_10.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_10.configure(foreground="#000000")
        # self.theme_10.configure(highlightbackground="#d9d9d9")
        # self.theme_10.configure(highlightcolor="black")
        # self.theme_10.configure(pady="0")
        self.theme_10.configure(text='''Yeti''')
        self.theme_10.configure(command=self.theme_10_b)
        self.theme_10.configure(style="b2.TButton")
        
        
        self.theme_11 = tb.Button(self.TNotebook1_t4)
        self.theme_11.place(relx=0.035, rely=0.857, height=34, width=97)
        # self.theme_11.configure(activebackground="#f0f0f0")
        # self.theme_11.configure(activeforeground="black")
        # self.theme_11.configure(background="#f0f0f0")
        self.theme_11.configure(compound='left')
        # self.theme_11.configure(disabledforeground="#a3a3a3")
        # self.theme_11.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_11.configure(foreground="#000000")
        # self.theme_11.configure(highlightbackground="#d9d9d9")
        # self.theme_11.configure(highlightcolor="black")
        # self.theme_11.configure(pady="0")
        self.theme_11.configure(text='''Morph''')
        self.theme_11.configure(command=self.theme_11_b)
        self.theme_11.configure(style="b2.TButton")
        
        
        self.theme_12 = tb.Button(self.TNotebook1_t4)
        self.theme_12.place(relx=0.245, rely=0.857, height=34, width=97)
        # self.theme_12.configure(activebackground="#f0f0f0")
        # self.theme_12.configure(activeforeground="black")
        # self.theme_12.configure(background="#f0f0f0")
        self.theme_12.configure(compound='left')
        # self.theme_12.configure(disabledforeground="#a3a3a3")
        # self.theme_12.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_12.configure(foreground="#000000")
        # self.theme_12.configure(highlightbackground="#d9d9d9")
        # self.theme_12.configure(highlightcolor="black")
        # self.theme_12.configure(pady="0")
        self.theme_12.configure(text='''Simplex''')
        self.theme_12.configure(command=self.theme_12_b)
        self.theme_12.configure(style="b2.TButton")
        
        
        self.theme_13 = tb.Button(self.TNotebook1_t4)
        self.theme_13.place(relx=0.438, rely=0.143, height=34, width=97)
        # self.theme_13.configure(activebackground="#f0f0f0")
        # self.theme_13.configure(activeforeground="black")
        # self.theme_13.configure(background="#f0f0f0")
        self.theme_13.configure(compound='left')
        # self.theme_13.configure(disabledforeground="#a3a3a3")
        # self.theme_13.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_13.configure(foreground="#000000")
        # self.theme_13.configure(highlightbackground="#d9d9d9")
        # self.theme_13.configure(highlightcolor="black")
        # self.theme_13.configure(pady="0")
        self.theme_13.configure(text='''Cerculean''')
        self.theme_13.configure(command=self.theme_13_b)
        self.theme_13.configure(style="b2.TButton")
        
        
        self.theme_0 = tb.Button(self.TNotebook1_t4)
        self.theme_0.place(relx=0.438, rely=0.286, height=34, width=97)
        # self.theme_0.configure(activebackground="#f0f0f0")
        # self.theme_0.configure(activeforeground="black")
        # self.theme_0.configure(background="#f0f0f0")
        self.theme_0.configure(compound='left')
        # self.theme_0.configure(disabledforeground="#a3a3a3")
        # self.theme_0.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_0.configure(foreground="#000000")
        # self.theme_0.configure(highlightbackground="#d9d9d9")
        # self.theme_0.configure(highlightcolor="black")
        # self.theme_0.configure(pady="0")
        self.theme_0.configure(text='''Padrão''')
        self.theme_0.configure(command=self.theme_default)
        self.theme_0.configure(style="b2.TButton")
        
        
        
        
        
        self.theme_14 = tb.Button(self.TNotebook1_t4)
        self.theme_14.place(relx=0.753, rely=0.143, height=34, width=97)
        # self.theme_14.configure(activebackground="#f0f0f0")
        # self.theme_14.configure(activeforeground="black")
        # self.theme_14.configure(background="#f0f0f0")
        self.theme_14.configure(compound='left')
        # self.theme_14.configure(disabledforeground="#a3a3a3")
        # self.theme_14.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_14.configure(foreground="#000000")
        # self.theme_14.configure(highlightbackground="#d9d9d9")
        # self.theme_14.configure(highlightcolor="black")
        # self.theme_14.configure(pady="0")
        self.theme_14.configure(text='''Solar''')
        self.theme_14.configure(command=self.theme_14_b)
        self.theme_14.configure(style="b2.TButton")
        
        
        self.theme_15 = tb.Button(self.TNotebook1_t4)
        self.theme_15.place(relx=0.753, rely=0.286, height=34, width=97)
        # self.theme_15.configure(activebackground="#f0f0f0")
        # self.theme_15.configure(activeforeground="black")
        # self.theme_15.configure(background="#f0f0f0")
        self.theme_15.configure(compound='left')
        # self.theme_15.configure(disabledforeground="#a3a3a3")
        # self.theme_15.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_15.configure(foreground="#000000")
        # self.theme_15.configure(highlightbackground="#d9d9d9")
        # self.theme_15.configure(highlightcolor="black")
        # self.theme_15.configure(pady="0")
        self.theme_15.configure(text='''Superhero''')
        self.theme_15.configure(command=self.theme_15_b)
        self.theme_15.configure(style="b2.TButton")
        
        
        self.theme_16 = tb.Button(self.TNotebook1_t4)
        self.theme_16.place(relx=0.753, rely=0.429, height=34, width=97)
        # self.theme_16.configure(activebackground="#f0f0f0")
        # self.theme_16.configure(activeforeground="black")
        # self.theme_16.configure(background="#f0f0f0")
        self.theme_16.configure(compound='left')
        # self.theme_16.configure(disabledforeground="#a3a3a3")
        # self.theme_16.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_16.configure(foreground="#000000")
        # self.theme_16.configure(highlightbackground="#d9d9d9")
        # self.theme_16.configure(highlightcolor="black")
        # self.theme_16.configure(pady="0")
        self.theme_16.configure(text='''Darkly''')
        self.theme_16.configure(command=self.theme_16_b)
        self.theme_16.configure(style="b2.TButton")
        
        
        self.theme_17 = tb.Button(self.TNotebook1_t4)
        self.theme_17.place(relx=0.753, rely=0.571, height=34, width=97)
        # self.theme_17.configure(activebackground="#f0f0f0")
        # self.theme_17.configure(activeforeground="black")
        # self.theme_17.configure(background="#f0f0f0")
        self.theme_17.configure(compound='left')
        # self.theme_17.configure(disabledforeground="#a3a3a3")
        # self.theme_17.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_17.configure(foreground="#000000")
        # self.theme_17.configure(highlightbackground="#d9d9d9")
        # self.theme_17.configure(highlightcolor="black")
        # self.theme_17.configure(pady="0")
        self.theme_17.configure(text='''Cyborg''')
        self.theme_17.configure(command=self.theme_17_b)
        self.theme_17.configure(style="b2.TButton")
        
        
        self.theme_18 = tb.Button(self.TNotebook1_t4)
        self.theme_18.place(relx=0.753, rely=0.714, height=34, width=97)
        # self.theme_18.configure(activebackground="#f0f0f0")
        # self.theme_18.configure(activeforeground="black")
        # self.theme_18.configure(background="#f0f0f0")
        self.theme_18.configure(compound='left')
        # self.theme_18.configure(disabledforeground="#a3a3a3")
        # self.theme_18.configure(font="-family {Segoe UI} -size 12 -weight bold")
        # self.theme_18.configure(foreground="#000000")
        # self.theme_18.configure(highlightbackground="#d9d9d9")
        # self.theme_18.configure(highlightcolor="black")
        # self.theme_18.configure(pady="0")
        self.theme_18.configure(text='''Vapor''')
        self.theme_18.configure(command=self.theme_18_b)
        self.theme_18.configure(style="b2.TButton")
    
    
    def options_info(self):
        # Label baixando
        self.baixando_label = tb.Label(self.TNotebook1_t5)
        self.baixando_label.place(relx=0.035, rely=0.071, height=241, width=534)
        self.baixando_label.configure(anchor='center')
        # self.baixando_label.configure(background="#f0f0f0")
        self.baixando_label.configure(font=("Helvetica", 14, 'bold'))
        self.baixando_label.configure(compound='left')
        # self.baixando_label.configure(disabledforeground="#a3a3a3")
        # self.baixando_label.configure(foreground="#000000")
        self.baixando_label.configure(justify='center')
        self.baixando_label.configure(text='''''')
    
    
    def options_about(self):
        self.version_text = tb.Label(self.TNotebook1_t6)
        self.version_text.place(relx=0.07, rely=0.05, height=75, width=350)
        # self.version_text.configure(activebackground="#f0f0f0")
        self.version_text.configure(anchor='w')
        # self.version_text.configure(background="#f0f0f0")
        self.version_text.configure(compound='left')
        self.version_text.configure(cursor="hand2")
        # self.version_text.configure(disabledforeground="#a3a3a3")
        self.version_text.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.version_text.configure(foreground="#000000")
        # self.version_text.configure(highlightbackground="#d9d9d9")
        # self.version_text.configure(highlightcolor="black")
        self.version_text.configure(justify='left')
        self.version_text.configure(text=f'''Mangá Downloader\n{version_}''')
        self.version_text.bind('<Button-1>', abrir_link1)
        
        
        
        self.version_text_1 = tb.Label(self.TNotebook1_t6)
        self.version_text_1.place(relx=0.07, rely=0.5, height=43, width=196)
        # self.version_text_1.configure(activebackground="#f9f9f9")
        self.version_text_1.configure(anchor='center')
        # self.version_text_1.configure(background="#f0f0f0")
        self.version_text_1.configure(compound='left')
        self.version_text_1.configure(cursor="hand2")
        # self.version_text_1.configure(disabledforeground="#a3a3a3")
        self.version_text_1.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.version_text_1.configure(foreground="#000000")
        # self.version_text_1.configure(highlightbackground="#d9d9d9")
        # self.version_text_1.configure(highlightcolor="black")
        self.version_text_1.configure(justify='center')
        self.version_text_1.configure(text='''Github''')
        self.version_text_1.bind('<Button-1>', abrir_link1)
        
        
        
        self.version_text_1_1 = tb.Label(self.TNotebook1_t6)
        self.version_text_1_1.place(relx=0.578, rely=0.5, height=43, width=196)
        # self.version_text_1_1.configure(activebackground="#f9f9f9")
        self.version_text_1_1.configure(anchor='center')
        # self.version_text_1_1.configure(background="#f0f0f0")
        self.version_text_1_1.configure(compound='left')
        self.version_text_1_1.configure(cursor="hand2")
        # self.version_text_1_1.configure(disabledforeground="#a3a3a3")
        self.version_text_1_1.configure(font="-family {Segoe UI} -size 16 -weight bold")
        # self.version_text_1_1.configure(foreground="#000000")
        # self.version_text_1_1.configure(highlightbackground="#d9d9d9")
        # self.version_text_1_1.configure(highlightcolor="black")
        self.version_text_1_1.configure(justify='center')
        self.version_text_1_1.configure(text='''Discord''')
        self.version_text_1_1.bind('<Button-1>', abrir_link2)
    
    
    def settings_global(self):
        auto_save = self.auto_save
        agregador_var = self.agregador_var
        nome_var = self.nome_var
        url_var = self.url_var
        capitulo_var = self.capitulo_var
        ate_var = self.ate_var
        extension_var = self.extension_var
        compact_extension_var = self.compact_extension_var
        compact_var = self.compact_var
        debug_var = self.debug_var
        debug2_var = self.debug2_var
        headless_var = self.headless_var
        net_option_var = self.net_option_var
        net_limit_down_var = self.net_limit_down_var
        net_limit_up_var = self.net_limit_up_var
        net_lat_var = self.net_lat_var
        change_log_var = self.change_log_var
        
        self.auto_save = tb.BooleanVar(value=False)
        self.agregador_var = tb.StringVar(value="BR Mangás")
        self.nome_var = tb.StringVar()
        self.url_var = tb.StringVar()
        self.capitulo_var = tb.StringVar()
        self.ate_var = tb.StringVar()
        self.extension_var = tb.StringVar(value=".jpg")
        self.compact_extension_var = tb.StringVar(value=".zip")
        self.compact_var = tb.BooleanVar(value=False)
        self.debug_var = tb.BooleanVar(value=True)
        self.debug2_var = tb.BooleanVar(value=False)
        self.headless_var = tb.BooleanVar(value=True)
        self.selenium_working = tb.BooleanVar(value=False)
        self.net_option_var = tb.BooleanVar(value=False)
        self.net_limit_down_var = tb.StringVar(value="1024")
        self.net_limit_up_var = tb.StringVar(value="1024")
        self.net_lat_var = tb.StringVar(value="50")
        self.change_log_var = tb.BooleanVar(value=True)
        
        self.auto_save.set(auto_save)
        self.agregador_var.set(agregador_var)
        self.nome_var.set(nome_var)
        self.url_var.set(url_var)
        self.capitulo_var.set(capitulo_var)
        self.ate_var.set(ate_var)
        self.extension_var.set(extension_var)
        self.compact_extension_var.set(compact_extension_var)
        self.compact_var.set(compact_var)
        self.debug_var.set(debug_var)
        self.debug2_var.set(debug2_var)
        self.headless_var.set(headless_var)
        self.net_option_var.set(net_option_var)
        self.net_limit_down_var.set(net_limit_down_var)
        self.net_limit_up_var.set(net_limit_up_var)
        self.net_lat_var.set(net_lat_var)
        self.change_log_var.set(change_log_var)
        
        
    def windows(self):
        # Bloquear redimensionamento da janela
        self.root.resizable(False, False)
        
        # Bloquear movimento da janela
        # Remove a barra de título e torna a janela não interativa
        self.root.overrideredirect(False)
        
        # Configuração para centralizar a janela
        window_width = 1124
        window_height = 466
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.x = (screen_width - window_width) // 2
        self.y = (screen_height - window_height) // 2
        self.root.geometry(f"{window_width}x{window_height}+{self.x}+{self.y}")


    def theme_default(self):
        self.theme = 'litera'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_1_b(self):
        self.theme = 'cosmo'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_2_b(self):
        self.theme = 'flatly'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_3_b(self):
        self.theme = 'litera'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_4_b(self):
        self.theme = 'journal'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_5_b(self):
        self.theme = 'lumen'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_6_b(self):
        self.theme = 'minty'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_7_b(self):
        self.theme = 'pulse'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_8_b(self):
        self.theme = 'sandstone'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_9_b(self):
        self.theme = 'united'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_10_b(self):
        self.theme = 'yeti'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_11_b(self):
        self.theme = 'morph'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_12_b(self):
        self.theme = 'simplex'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_13_b(self):
        self.theme = 'cerculean'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_14_b(self):
        self.theme = 'solar'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_15_b(self):
        self.theme = 'superhero'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_16_b(self):
        self.theme = 'darkly'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_17_b(self):
        self.theme = 'cyborg'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
        
    def theme_18_b(self):
        self.theme = 'vapor'
        self.save_settings()
        self.root.destroy()
        # reload_main.setup()
        sys.exit()
    
        
    def reset_config(self):
        print(hora_agora.setup(), "INFO:", "✔ Configurações resetadas. Reiniciando aplicativo.")
        auto_save = False
        agregador_var = ""
        nome_var = ""
        url_var = ""
        capitulo_var = ""
        ate_var = ""
        extension_var = ".jpg"
        compact_extension_var = ".zip"
        compact_var = False
        debug_var = True
        debug2_var = False
        headless_var = True
        folder_selected = os.path.join(os.path.expanduser("~"), "Downloads")
        theme = 0
        net_option_var = False
        net_limit_down_var = 1024
        net_limit_up_var = 1024
        net_lat_var = 50
        change_log_var = True
        
        self.auto_save.set(auto_save)
        self.agregador_var.set(agregador_var)
        self.nome_var.set(nome_var)
        self.url_var.set(url_var)
        self.capitulo_var.set(capitulo_var)
        self.ate_var.set(ate_var)
        self.extension_var.set(extension_var)
        self.compact_extension_var.set(compact_extension_var)
        self.compact_var.set(compact_var)
        self.debug_var.set(debug_var)
        self.debug2_var.set(debug2_var)
        self.headless_var.set(headless_var)
        self.net_option_var.set(net_option_var)
        self.net_limit_down_var.set(net_limit_down_var)
        self.net_limit_up_var.set(net_limit_up_var)
        self.net_lat_var.set(net_lat_var)
        self.change_log_var.set(change_log_var)
        
        save_settings.setup(settings_dir, self.auto_save, self.agregador_var, self.nome_var, self.url_var, self.capitulo_var, self.ate_var, self.extension_var, self.compact_extension_var, self.compact_var, self.debug_var, self.debug2_var, self.headless_var, folder_selected, theme, self.net_option_var, self.net_limit_down_var, self.net_limit_up_var, self.net_lat_var, self.change_log_var)
        self.root.destroy()
        # reload_main.setup()
        sys.exit()


    def save_shortcut(self, event=None):
        if self.ipo9 is False:
            self.app_instance.move_text_wait('Configurações salvas')
        
    def start_shortcut(self, event=None):
        if self.ipo9 is False:
            self.start_download()
        
    def selenium_load_message(self, event=None):
        if self.ian is False:
            self.app_instance.move_text_wait('Verificando navegador')
        else:
            self.root.after(1000, self.selenium_load_message)
    
        
        
        
