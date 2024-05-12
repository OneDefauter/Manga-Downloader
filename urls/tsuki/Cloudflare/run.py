import os
import re
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
    
    controle = await pagina.find('chapter-controls-bottom', timeout=10)
    if controle.children[0].children[1].text == 'Páginas abertas':
        await controle.children[0].children[1].click()
    
    async def wait_image():
        while True:
            fim = False
            paginas__ = await pagina.find('/html/body/div[1]/div[1]/div[2]')
            for paginas___ in paginas__.children:
                if paginas___.tag == 'img':
                    if paginas___.attributes[1] == 'pagereader':
                        await paginas___.scroll_into_view()
                        fim = True
                    else:
                        await wait_image()
            if fim:
                break

    async def load_images():
        count_repet = 0
        count_save = 0
        paginas_encontradas = 0
        while count_repet < max_verify:
            paginas_encontrada = 0
            try:
                if debug_var.get():
                    baixando_label.config(text=f"Carregando capítulo {numero_capitulo}\nVerificação {count_repet + 1} / {max_verify}\nEncontrados {paginas_encontradas} imagens")

                paginas = await pagina.find('/html/body/div[1]/div[1]/div[2]')

                for pag in paginas.children:
                    if pag.tag == 'img':
                        if not pag.attributes[1] == 'pagereader':
                            await wait_image()
                        await pag.scroll_into_view()
                        paginas_encontrada += 1
                
                count_repet += 1
                
                if paginas_encontradas == paginas_encontrada:
                    if count_save + 20 == count_repet:
                        break
                    else:
                        time.sleep(0.2)
                else:
                    paginas_encontradas = paginas_encontrada
                    count_save += 1
                    time.sleep(0.2)

            except Exception as e:
                print(f"Erro durante o carregamento de imagens: {e}")
                # Se ocorrer um erro, você pode querer tentar novamente ou lidar com a situação de outra maneira
    
    await load_images()

    while True:
        paginas = await pagina.find('/html/body/div[1]/div[1]/div[2]')
    
        # Itera sobre as imagens
        for imagem in paginas.children:
            if imagem.local_name == 'a':
                continue
    
            await imagem.scroll_into_view()
        
        links_das_imagens = []
        for pag in paginas.children:
            if pag.tag == 'img':
                if not pag.attributes[1] == 'pagereader':
                    await wait_image()
                await pag.scroll_into_view()
                links_das_imagens.append(pag.attributes[3])
        
        links_count = str(len(links_das_imagens))
        
        break
        
    async def download_images(count, files):
        for imagem in links_das_imagens:
            if debug_var.get():
                baixando_label.config(text=f"Verificando capítulo {numero_capitulo}\nBaixando página: {count} / {links_count}")
                
            pag_ = await driver.get(imagem, new_tab = True)
            
            attents = 1
            while attents < max_attent:
                try:
                    input_element = await pag_.select('input[type="number"]')
                    break
                except:
                    try:
                        await pag_.close()
                        pag_ = await driver.get(imagem, new_tab = True)
                        time.sleep(0.2)
                        
                        input_element = await pag_.select('input[type="number"]')
                    except:
                        attents += 1
            if attents == max_attent:
                print(f"{Fore.RED}Falha ao baixar o capítulo {numero_capitulo}")
                return 526
            
            await input_element.clear_input()
            await input_element.send_keys(f"{count}")
            
            download_button = await pag_.find('/html/body/button')
            await download_button.mouse_click()
            
            extension_match = re.search(r'\.(jpg|jpeg|png|gif|bmp|webp)(\?|$)', imagem, re.IGNORECASE)
            
            if extension_match:
                file_extension = extension_match.group(1)
            
            print(f"{Fore.GREEN}Baixando {imagem} como {count:02d}.{file_extension}...{Style.RESET_ALL}")
            
            time.sleep(0.8)
            
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
                        await download_button.mouse_click()
                        attention = 0
                        warning_img += 1
                        continue
            
            count += 1
            await pag_.close()
            
        return count
    
    await download_images(1, 0)
    
    if debug_var.get():
        baixando_label.config(text=f"Arrumando páginas...")

    move.setup(download_folder, folder_path)
    
    organizar.organizar(folder_path, compactar, compact_extension, extension)
    
    if debug_var.get():
        baixando_label.config(text=f"Aguarde...")
    
    app_instance.move_text_wait(f'Capítulo {numero_capitulo} baixado com sucesso')
    
    print(f"═══════════════════════════════════► {nome} -- {numero_capitulo} ◄═══════════════════════════════════════\n")
