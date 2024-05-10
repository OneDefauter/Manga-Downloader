import re

async def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    pagina = await driver.get(url)
    
    print("Verificando capítulos...")
    app_instance.move_text_wait(f'Verificando capítulos')
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")
    
    x = 1
    while True:
        capitulos_encontrados = []
        
        attempts = 0
        while attempts < max_attent:
            try:
                await pagina.find('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4', timeout=10)
                break
            except:
                attempts += 1
                await pagina.reload()
        
        try:
            btn = await pagina.find('flex w-48 py-4 flex-col gap-2 items-center justify-center cursor-pointer ease-in-out transform hover:scale-110  hover:shadow-lg rounded-lg p-2  shadow-md  transition-all duration-300 bg-dark', timeout=2)
            await btn.click()
        except:
            ...
        
        capitulos = await pagina.find('grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4', timeout=10)
        
        for capitulo in capitulos.children:
            chapter_link = "https://slimeread.com" + capitulo.children[0].attributes[1]
            chapter_number = str(capitulo.children[0].children[0].children[0].children[1])
            
            if chapter_number == '':
                continue
            
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
