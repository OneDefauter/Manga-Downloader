import re
import asyncio


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
            capitulos = await pagina.find('/html/body/div[1]/main/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/ul')
            
            if capitulos.children[0].text != first_cap_tab:
                first_cap_tab = capitulos.children[0].text
            else:
                break
                
            for capitulo in capitulos.children:
                chapter_link = 'https://modescanlator.com/' + capitulo.attributes[3]
                chapter_number = capitulo.text
                if chapter_number == '':
                    continue
                
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
                
                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
            
            releasespaginate = await pagina.find('/html/body/div[1]/main/div/div[1]/div[2]/div[2]/div/div[1]/div[2]/nav/ul[4]/li/a')
            await releasespaginate.click()

        except:
            if trying < max_attent:
                trying += 1
                pagina = await driver.get(url)
                await pagina
                await asyncio.sleep(3)
                
            else:
                return 0 # Nenhum capítulo encontrado
        
            
    return capitulos_encontrados
