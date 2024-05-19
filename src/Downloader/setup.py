import os
import time
import requests
from tkinter import messagebox
from colorama import Fore, Style

import src.clean as clean
import src.print as print_log
import src.Scripts.setup as ins_ext
import src.folder_delete as del_folder

import engine.default as engine_default
import engine.nodrive as nodrive

from src.Downloader.ag import *

from setup.ttk import download_folder, dic_agregadores


class DownloaderSetup():
    def __init__(
        self, 
        app_instance, 
        agregador_var, 
        nome_var, 
        url_var, 
        capitulo_var, 
        ate_var, 
        compact_var, 
        compact_extension_var, 
        extension_var, 
        auto_save, 
        debug_var, 
        headless_var, 
        max_attent_var, 
        max_verify_var,
        user_var,
        pass_var,
        process_completed,
        baixando_label,
        folder_selected,
        tempo_decorrido_,
        notif_01,
        notif_02,
        ext_01,
        ext_02,
        ext_03,
        ext_04
    ):
        self.app_instance = app_instance
        self.agregador_var = agregador_var
        self.nome_var = nome_var
        self.url_var = url_var
        self.capitulo_var = capitulo_var
        self.ate_var = ate_var
        self.compact_var = compact_var
        self.compact_extension_var = compact_extension_var
        self.extension_var = extension_var
        self.auto_save = auto_save
        self.debug_var = debug_var
        self.headless_var = headless_var
        self.max_attent_var = max_attent_var
        self.max_verify_var = max_verify_var
        self.user_var = user_var
        self.pass_var = pass_var
        self.username = None
        self.password = None
        self.result = None
        self.verificado = False
        self.process_completed = process_completed
        self.baixando_label = baixando_label
        self.folder_selected = folder_selected
        self.tempo_decorrido_ = tempo_decorrido_
        
        self.notif_01 = notif_01
        self.notif_02 = notif_02
        
        self.ext_01 = ext_01
        self.ext_02 = ext_02
        self.ext_03 = ext_03
        self.ext_04 = ext_04
        
    async def setup(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        
        print("Agregador escolhido:", self.agregador_var.get())
        print("Obra escolhida:", str(self.nome_var.get()).replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace("\n", "").rstrip())
        print("URL da obra:", self.url_var.get())
        print("Capítulo escolhido:", self.capitulo_var.get())
        print("Até qual capítulo baixar:", self.ate_var.get())
        print("Compactar:", "sim" if self.compact_var.get() else "não")
        print("Extensão da compactação:", self.compact_extension_var.get())
        print("Extensão de saída:", self.extension_var.get())
        print("Auto salvar:", self.auto_save.get())
        print("Debug:", self.debug_var.get())
        print("Navegador em segundo plano:", self.headless_var.get())
        print("Máximo de tentativas:", self.max_attent_var.get())
        print("Máximo de verificação:", self.max_verify_var.get())
        print("\n")
        
        self.VerificarOpções()
        
        if self.result == 777:
            return self.process_completed, self.result, self.notif_01, self.notif_02, self.ext_01, self.ext_02, self.ext_03, self.ext_04
        
        if self.verificado:
            await self.preparar()
        
        return self.process_completed, self.result, self.notif_01, self.notif_02, self.ext_01, self.ext_02, self.ext_03, self.ext_04
    
    def VerificarOpções(self):
        if self.agregador_var.get() == "SlimeRead":
            if self.user_var.get() == "" or self.pass_var.get() == "":
                print("Erro: Usuário ou senha em branco.")
                self.app_instance.move_text_wait('Erro: Usuário ou senha em branco')
                messagebox.showerror("Erro", "Usuário ou senha em branco")
                self.result = 777
            else:
                self.username = self.user_var.get()
                self.password = self.pass_var.get()
        
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
        
        elif self.capitulo_var.get() == "" and self.ate_var.get() == "":
            print("Erro: Capítulo inválido.")
            self.app_instance.move_text_wait('Erro: Capítulo inválido')
            messagebox.showerror("Erro", "Capítulo inválido")
            self.result = 777
        
        if self.result == 777:
            self.process_completed.set()
        
        else:
            if self.capitulo_var.get() == "" and self.ate_var.get() != "":
                self.capítulo = 0.0
                self.ate = float(self.ate_var.get())
            elif self.ate_var.get() == "" and self.capitulo_var.get() != "":
                self.capítulo = float(self.capitulo_var.get())
                self.ate = float(self.capitulo_var.get())
            else:
                self.capítulo = float(self.capitulo_var.get())
                self.ate = float(self.ate_var.get())
            
            self.verificado = True
            
            if self.ate < self.capítulo:
                self.ate = self.capítulo
    
    def check_cloudflare(self, url):
        try:
            response = requests.head(url)
            if 'server' in response.headers and 'cloudflare' in response.headers['server'].lower():
                return True
            else:
                return False
        except Exception as e:
            return False
    
    async def preparar(self):
        self.agregador_escolhido = self.agregador_var.get()
        self.nome = self.nome_var.get().replace("\n", "")
        self.url = self.url_var.get()
        # capítulo = float(self.capitulo_var.get())
        self.compactar = self.compact_var.get()
        self.extension = self.extension_var.get()
        self.compact_extension = self.compact_extension_var.get()
        
        self.nome_foler = self.nome.replace("<", "").replace(">", "").replace(":", "").replace("\"", "").replace("/", "").replace("\\", "").replace("|", "").replace("?", "").replace("*", "").replace("\n", "").rstrip()
        
        if self.debug_var.get():
            self.baixando_label.config(text="Iniciando...")
            print_log.setup(
                f'Agregador escolhido: {self.agregador_escolhido}', 
                [
                    f'Obra escolhida: {self.nome}',
                    f'Capítulo escolhido: {str(self.capítulo).replace(".0", "")}',
                    f'Até qual capítulo baixar: {str(self.ate).replace(".0", "")}',
                    f'Compactar: {"sim" if self.compactar else "não"}',
                    f'Tipo de compactação: {self.compact_extension}',
                    f'Extensão de saída: {self.extension}'
                ]
            )
            print("\n")
        self.app_instance.move_text_wait('Iniciando')
        
        for dic_name, dic_url in dic_agregadores.items():
            if not self.agregador_escolhido in dic_agregadores:
                self.app_instance.move_text_wait('Agregador inválido')
                if self.debug_var.get():
                    self.baixando_label.config(text="Agregador inválido")
                print("Agregador inválido")
                break
            
            elif not dic_name in self.agregador_escolhido:
                continue
            
            # Num 01 (BR Mangás)
            elif "BR Mangás" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_01)
                break
    
            # Num 02 (Crystal Scan)
            elif "Crystal Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_02)
                break
                
            # Num 03 (Argos Comics)
            elif "Argos Comics" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_03)
                break
    
            # Num 04 (Argos Hentai)
            # elif "Argos Hentai" in self.agregador_escolhido:
            #     await self.IniciarDrive(dic_url, agr_04)
            #     break
    
            # Num 05 (Mangás Chan)
            elif "Mangás Chan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_05)
                break
    
            # Num 06 (Ler Mangá)
            elif "Ler Mangá" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_06)
                break
    
            # Num 07 (Tsuki)
            elif "Tsuki" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_07)
                break
    
            # Num 08 (YomuMangás)
            elif "YomuMangás" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_08)
                break
    
            # Num 09 (SlimeRead)
            elif "SlimeRead" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_09)
                break
    
            # Num 10 (Flower Manga)
            elif "Flower Manga" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_10)
                break
    
            # Num 11 (Ler Manga Online)
            elif "Ler Manga Online" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_11)
                break
    
            # Num 12 (Manga BR)
            elif "Manga BR" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_12)
                break
    
            # Num 13 (Projeto Scanlator)
            elif "Projeto Scanlator" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_13)
                break
    
            # Num 14 (Hentai Teca)
            elif "Hentai Teca" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_14)
                break
    
            # Num 15 (Argos Scan)
            elif "Argos Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_15)
                break
    
            # Num 16 (NicoManga)
            elif "NicoManga" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_16)
                break
    
            # Num 17 (Momo no Hana)
            elif "Momo no Hana" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_17)
                break
    
            # Num 18 (Manhastro)
            elif "Manhastro" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_18)
                break
    
            # Num 19 (Valkyrie Scan)
            elif "Valkyrie Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_19)
                break
    
            # Num 20 (Limbo Scan)
            elif "Limbo Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_20)
                break
    
            # Num 21 (Nobre Scan)
            elif "Nobre Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_21)
                break
    
            # Num 22 (Iris Scanlator)
            elif "Iris Scanlator" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_22)
                break
    
            # Num 23 (NovelMic)
            elif "NovelMic" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_23)
                break
    
            # Num 24 (Norte Rose)
            elif "Norte Rose" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_24)
                break
    
            # Num 25 (L Scan)
            elif "L Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_25)
                break
    
            # Num 26 (MiniTwo Scan)
            elif "MiniTwo Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_26)
                break
    
            # Num 27 (Demon Sect)
            elif "Demon Sect" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_27)
                break
    
            # Num 28 (Moon Witch In Love)
            elif "Moon Witch In Love" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_28)
                break
    
            # Num 29 (Hikari Scan)
            elif "Hikari Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_29)
                break
    
            # Num 30 (Luratoon Scan)
            elif "Luratoon Scan" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_30)
                break
    
            # Num 31 (Mode Scanlator)
            elif "Mode Scanlator" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_31)
                break
    
            # Num 32 (Cerise Toon)
            elif "Cerise Toon" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_32)
                break
    
            # Num 33 (Sinensis Toon)
            elif "Sinensis Toon" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_33)
                break
    
            # Num 34 (3xyaoi)
            elif "3xyaoi" in self.agregador_escolhido:
                await self.IniciarDrive(dic_url, agr_34)
                break
        
        folder_path = os.path.join(self.folder_selected, self.nome_foler)
        del_folder.delete_empty_folders(folder_path.replace('/', '\\'))
        
        self.process_completed.set()
    
    async def IniciarDrive(self, dic_url, agregador):
        if not dic_url in self.url:
            self.result = 1
            print("Erro: URL inválida")
            return
        
        # self.cloudflare = self.check_cloudflare(dic_url)
        self.cloudflare = True
        
        if self.cloudflare:
            if self.headless_var.get():
                if self.notif_01 is False:
                    self.notif_01 = True
                    messagebox.showwarning("Aviso", "Agregador não suporta download em segundo plano.")
            print(f"{Fore.GREEN}AVISO: Esse agregador não suporta download em segundo plano.{Style.RESET_ALL}")
            self.driver = await nodrive.setup()
            
            await self.driver.get("https://www.google.com")
            
            # if not self.ext_01:
            #     self.ext_01 = True
            #     await ins_ext.setup(self.driver, e_01=True, cloudflare=self.cloudflare)
                
            if not self.ext_02:
                self.ext_02 = True
                await ins_ext.setup(self.driver, e_02=True, cloudflare=self.cloudflare)
            
            if not self.ext_03:
                self.ext_03 = True
                await ins_ext.setup(self.driver, e_03=True, cloudflare=self.cloudflare)
            
            if not self.ext_04:
                self.ext_04 = True
                await ins_ext.setup(self.driver, e_04=True, cloudflare=self.cloudflare)
        
        else:
            self.driver = engine_default.setup(self.headless_var.get())
            
            # if not self.ext_01:
            #     self.ext_01 = True
            #     await ins_ext.setup(self.driver, e_01=True)
                
            # if not self.ext_02:
            #     self.ext_02 = True
            #     await ins_ext.setup(self.driver, e_02=True)
                
            # if not self.ext_03:
            #     self.ext_03 = True
            #     await ins_ext.setup(self.driver, e_03=True)
        
        
        if self.debug_var.get():
            self.baixando_label.config(text="Aguarde...")
        print("\nAguarde...")
        
        clean.setup(download_folder)        
        
        await self.tempo_decorrido_.iniciar_tempo()
        self.result = await agregador.setup(
            self.driver,
            self.url,
            self.capítulo,
            self.ate,
            self.debug_var,
            self.baixando_label,
            self.folder_selected,
            self.nome_foler,
            self.nome,
            self.compactar,
            self.compact_extension,
            self.extension,
            download_folder,
            self.app_instance,
            int(self.max_attent_var.get()),
            int(self.max_verify_var.get()),
            self.username,
            self.password,
            self.cloudflare
            )

        await self.tempo_decorrido_.parar_tempo()
        
        if self.cloudflare:
            pag = await self.driver.get(self.url)
            await pag.close()
            self.driver.stop()
        else:
            self.driver.quit()
