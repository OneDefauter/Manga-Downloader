import os
import shutil
from datetime import datetime
from colorama import Fore, Style

import src.move as move
import src.organizar as organizar
from src.zipfile import setup as zip_setup

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

    pagina = await driver.get(url)

    await pagina.sleep(3)
    
    pag = await pagina.find('/html/body/div[1]/main/div/div[2]/div[2]/div[3]/img[1]')
    await pag.mouse_move()
    
    btn = await pagina.find('Abrir a imagem na galeria (G)')
    await btn.click()
    
    btn = await pagina.find('pv-gallery-head-command-others')
    await btn.click()
    
    btn = await pagina.find('Baixar todas as imagens')
    await btn.click()


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
                    zip_setup(download_folder)
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
