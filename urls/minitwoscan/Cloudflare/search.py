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
    
    x = 1
    while True:
        capitulos_encontrados = []
        capitulos = []
        
        await pagina.evaluate("window.dispatchEvent(new Event('mousemove'));")
        
        attempts = 0
        while attempts < max_attent:
            try:
                await pagina.find('main version-chap active', timeout = 2)
                break
            except:
                attempts += 1
                await pagina.reload()
        
        try:
            btn = await pagina.find('c-chapter-readmore', timeout=3)
            await btn.children[0].click()
        except:
            pass
            
        capitulos = await pagina.find('main version-chap active')
    
        for capitulo in capitulos.children:
            link = capitulo.children[0].attributes[1]
            ch_number = capitulo.text
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
