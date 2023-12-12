import os
from selenium.webdriver.common.by import By

def obter_capitulos(driver, url, inicio, fim, debug_var, baixando_label):
    # Abre a página
    driver.get(url)
    
    # Aguarde um pouco para garantir que a página seja totalmente carregada (você pode ajustar esse tempo conforme necessário)
    driver.implicitly_wait(5)
    
    # Verifica se a página contém o texto "Página não encontrada"
    if "Página não encontrada" in driver.page_source:
            print("Erro: URL inválida. Status code: 404")
            driver.quit()
            return 'e1'
    
    # Esperar a lista de capítulos carregar
    capitulos = driver.find_elements(By.XPATH, '//div[@class="lista_manga"]//li[@class="row lista_ep"]')

    capitulos_encontrados = []
    
    os.system("cls")
    print("Verificando capítulos...")
    if debug_var.get():
        baixando_label.config(text="Verificando capítulos...")

    for capitulo in capitulos:
        numero_capitulo = float(capitulo.get_attribute('data-cap'))
        if inicio <= numero_capitulo <= fim:
            link = capitulo.find_element(By.XPATH, './/a').get_attribute('href')
            capitulos_encontrados.append({'numero_capitulo': numero_capitulo, 'link': link})

    return capitulos_encontrados
