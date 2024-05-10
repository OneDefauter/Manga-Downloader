import urls.search_methods.Madara.madara as capitulos

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent):
    capitulos_encontrados = capitulos.setup(driver, url, inicio, fim, debug_var, baixando_label, app_instance, max_attent)
    
    return capitulos_encontrados
