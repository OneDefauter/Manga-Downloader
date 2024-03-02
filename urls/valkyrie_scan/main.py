import os
import aiohttp

import urls.valkyrie_scan.search as obter_capitulos
import urls.valkyrie_scan.run as run

async def setup(driver, url, capítulo, ate, debug_var, baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension, download_folder, app_instance, max_attent, max_verify):
    base_url = 'https://valkyriescan.com/'

    # Função para obter capítulos dentro de um intervalo
    capitulos_solicitados = obter_capitulos.obter_capitulos(driver, url, capítulo, ate, debug_var, baixando_label, app_instance, max_attent)
    
    if capitulos_solicitados in ['e400', 'e401', 'e403', 'e404', 'e500', 'e502', 'e503', 'e522', 'e523']:
        return capitulos_solicitados
    
    if len(capitulos_solicitados) == 0:
        print("Nenhum capítulo encontrado")
        return 3

    async with aiohttp.ClientSession() as session:
        os.system("cls")
        
        # Inverter a ordem dos capítulos
        capitulos_solicitados.reverse()
        
        for capitulo in capitulos_solicitados:
            numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
            numero_ultimo_capitulo = str(capitulos_solicitados[-1]['numero_capitulo']).replace('.0', '')
            url = capitulo['link']
            
            if len(capitulos_solicitados) == 1:
                app_instance.move_text_wait(f'Carregando capítulo {numero_capitulo}')
            else:
                app_instance.move_text_wait(f'Carregando capítulo {numero_capitulo} / {numero_ultimo_capitulo}')
            
            await run.run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension, download_folder, app_instance, max_attent, max_verify)
            
    return 0