import re


async def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    pagina = await driver.get(url)
    await pagina.sleep(3)
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")
    
    x = 1
    while True:
        capitulos_encontrados = []
        capitulos = []
        
        attempts = 0
        while attempts < max_attent:
            try:
                await pagina.find('/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul', timeout = 2)
                break
            except:
                attempts += 1
                await pagina.reload()
        
        capitulos = await pagina.find('/html/body/div[2]/div/div[1]/div/div[2]/div/div/div/div/div/div[1]/div[2]/div[2]/div/ul')
    
        for capitulo in capitulos.children:
            try:
                chapter_link = capitulo.children[0]._attrs.href
            except:
                chapter_link = capitulo.children[1]._attrs.href
            
            chapter_number = capitulo.text
            
            numero_capitulo = float(re.sub(r'[^0-9.,]', '', chapter_number.replace(',', '')))
            
            if inicio <= numero_capitulo <= fim:
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': chapter_link})
                    
        if len(capitulos_encontrados) > 0:
            break
        else:
            if x < max_attent:
                x += 1
            else:
                break
    
    return capitulos_encontrados
