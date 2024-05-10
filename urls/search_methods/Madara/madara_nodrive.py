import re
import asyncio


async def setup(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    pagina = await driver.get(url)
    await pagina
    await asyncio.sleep(3)
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")
    
    x = 1
    while True:
        capitulos_encontrados = []
        capitulos = []
        
        await pagina.evaluate("window.dispatchEvent(new Event('mousemove'));")
        
        attempts = 0
        while attempts < max_attent:
            try:
                caps = await pagina.find('wp-manga-chapter', timeout = 2)
                if 'main version-chap no-volumn active' in caps.attributes[1]:
                    CLASS_ID = 'wp-manga-chapter'
                else:
                    caps = await pagina.find('main version-chap no-volumn active', timeout = 2)
                    if 'main version-chap no-volumn active' in caps.attributes[1]:
                        CLASS_ID = 'main version-chap no-volumn active'

                break
            except:
                attempts += 1
                await pagina.reload()
        
        try:
            btn = await pagina.find('c-chapter-readmore', timeout=3)
            await btn.children[0].click()
        except:
            pass
            
        capitulos = await pagina.find(CLASS_ID)
    
        for capitulo in capitulos.parent.children:
            if capitulo.tag == "li":
                link = capitulo.children[0].attributes[1]
                ch_number = capitulo.text
                if ch_number == '':
                    continue
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', ch_number.replace(',', '')))
                
                if inicio <= numero_capitulo <= fim:
                    capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
                    
            elif capitulo.tag == "ul":
                for cap in capitulo.children:
                    link = cap.children[1].attributes[1]
                    ch_number = cap.children[1].text
                    if ch_number == '':
                        continue
                    numero_capitulo = float(re.sub(r'[^0-9.,]', '', ch_number.replace(',', '')))
                    
                    if inicio <= numero_capitulo <= fim:
                        capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
                    
    
        if len(capitulos_encontrados) > 0:
            break
        else:
            if x < max_attent:
                x += 1
            else:
                break
    
    return capitulos_encontrados
