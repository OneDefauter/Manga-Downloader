import os
import time
import shutil
import asyncio
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

    pagina = await driver.get(url)
    await pagina
    await asyncio.sleep(3)
    
    await pagina.evaluate("var select = document.getElementById('readingmode');"
                            "select.value = 'full';"
                            "var event = new Event('change');"
                            "select.dispatchEvent(event);")
    
    async def wait_image():
        attent = 1
        while attent < max_attent:
            fim = False
            paginas__ = await pagina.find('/html/body/div[1]/div[2]/div/div/div/article/div[3]/div[4]')
            paginas___ = paginas__.children[-1]
            if paginas___.tag == 'img':
                if paginas___.attributes[-1] == 'loaded':
                    await paginas___.scroll_into_view()
                    fim = True
                else:
                    await pagina.scroll_down(200)
                    # await pagina.evaluate("window.scrollTo(0, document.body.scrollHeight);")
            if fim:
                break
            
            else:
                attent += 1
    
    async def load_images():
        count_repet = 0
        count_save = 0
        paginas_encontradas = 0
        while count_repet < max_verify:
            paginas_encontrada = 0
            try:
                if debug_var.get():
                    baixando_label.config(text=f"Carregando capítulo {numero_capitulo}\nVerificação {count_repet + 1} / {max_verify}\nEncontrados {paginas_encontradas} imagens")

                paginas = await pagina.find('/html/body/div[1]/div[2]/div/div/div/article/div[3]/div[4]')
                
                for pag in paginas.children:
                    if pag.tag == 'img':
                        if pag.attributes[-1] == 'loaded':
                            await pag.scroll_into_view()
                            paginas_encontrada += 1
                        else:
                            await wait_image()
                
                count_repet += 1
                
                if paginas_encontradas == paginas_encontrada:
                    if count_save + 10 == count_repet:
                        break
                    else:
                        time.sleep(0.2)
                else:
                    paginas_encontradas = paginas_encontrada
                    count_save += 1
                    time.sleep(0.2)
            
            except Exception as e:
                print(f"Erro durante o carregamento de imagens: {e}")
            
    await load_images()
    
    while True:
        paginas = await pagina.find('/html/body/div[1]/div[2]/div/div/div/article/div[3]/div[4]')
    
        await paginas.children[0].scroll_into_view()
    
        await paginas.children[0].scroll_into_view()
        await paginas.children[0].mouse_move()
        
        btn = await pagina.find('Abrir a imagem na galeria (G)')
        await btn.click()
        
        btn = await pagina.find('pv-gallery-head-command-others')
        await btn.click()
        
        btn = await pagina.find('Baixar todas as imagens')
        await btn.click()
        
        break
        
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
    
    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
