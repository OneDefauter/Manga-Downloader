import re
import asyncio
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import src.status_check as status_check

async def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    pagina = await driver.get(url)
    await pagina
    await asyncio.sleep(3)
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    trying = 1
    first_cap_tab = None
    capitulos_encontrados = []
    while True:
        try:
            capitulos = await pagina.find('/html/body/div[1]/div[1]/div[3]/div[2]/div')
            
            if capitulos.children[0].children[2].text != first_cap_tab:
                first_cap_tab = capitulos.children[0].children[2].text
            else:
                break
                
            for capitulo in capitulos.children:
                if capitulo.attributes[1] == 'cardchapters pointer':
                    chapter_link = "https://tsuki-mangas.com" + capitulo.children[2].attributes[1]
                    chapter_number = capitulo.children[2].text
                    if chapter_number == '':
                        continue
                    
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                    
                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
            
            releasespaginate = await pagina.find('/html/body/div[1]/div[1]/div[3]/div[2]/div/ul')
            
            for pag in releasespaginate.children:
                if pag.text == '>':
                    await pag.children[0].click()
                    break
        
        except:
            if trying < max_attent:
                trying += 1
                pagina = await driver.get(url)
                await pagina
                await asyncio.sleep(3)
                
            else:
                return 3 # Nenhum capítulo encontrado
        
            
    return capitulos_encontrados
