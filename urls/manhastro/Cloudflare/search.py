import re

async def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    pagina = await driver.get(url)
    await pagina
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
                await pagina.find('manga-chapters-holder')
                break
            except:
                attempts += 1
                await pagina.reload()
        
        capitulos = await pagina.find('main version-chap no-volumn')
        
        for capitulo in capitulos.children:
            numero_capitulo = capitulo.text
            if numero_capitulo.isdigit():
                numero_capitulo = float(numero_capitulo)
            elif numero_capitulo == "prologo":
                numero_capitulo = 0.0
            else:
                numero_capitulo = float(re.sub(r'[^0-9.,]', '', numero_capitulo.replace(',', '')))
            if inicio <= numero_capitulo <= fim:
                link = capitulo.children[1].attributes[1]
                capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})
        
        if len(capitulos_encontrados) > 0:
            break
        else:
            if x < max_attent:
                x += 1
            else:
                break

    return capitulos_encontrados
