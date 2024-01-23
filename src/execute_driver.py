import time
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options


def install_ext_1(driver):
    url_extension = 'https://update.greasyfork.org/scripts/419894/Image%20Downloader.user.js'
    driver.get(url_extension)
    
    # Pega o tempo inicial
    tempo_inicial = datetime.now()

    # Define o limite de tempo em segundos (30 segundos no seu caso)
    limite_tempo_segundos = 30

    while True:
        janelas_abertas = driver.window_handles

        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            break
        else:
            tempo_atual = datetime.now()
            tempo_decorrido = tempo_atual - tempo_inicial

            if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                print("Tempo limite atingido. Saindo do loop.")
                return
    
    time.sleep(0.8)
    
    # Realiza a ação de pressionar a tecla de espaço
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    time.sleep(0.2)
    
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.8)



def install_ext_2(driver):
    url_extension = 'https://update.greasyfork.org/scripts/482691/Teste.user.js'
    driver.get(url_extension)
    
    # Pega o tempo inicial
    tempo_inicial = datetime.now()

    # Define o limite de tempo em segundos (30 segundos no seu caso)
    limite_tempo_segundos = 30

    while True:
        janelas_abertas = driver.window_handles

        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            break
        else:
            tempo_atual = datetime.now()
            tempo_decorrido = tempo_atual - tempo_inicial

            if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                print("Tempo limite atingido. Saindo do loop.")
                return
    
    time.sleep(0.8)
    
    # Realiza a ação de pressionar a tecla de espaço
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    time.sleep(0.2)
    
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.8)



def install_ext_3(driver):
    url_extension = 'https://update.greasyfork.org/scripts/472453/CloudFlare%20Challenge.user.js'
    driver.get(url_extension)
    
    # Pega o tempo inicial
    tempo_inicial = datetime.now()

    # Define o limite de tempo em segundos (30 segundos no seu caso)
    limite_tempo_segundos = 30

    while True:
        janelas_abertas = driver.window_handles

        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            break
        else:
            tempo_atual = datetime.now()
            tempo_decorrido = tempo_atual - tempo_inicial

            if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                print("Tempo limite atingido. Saindo do loop.")
                return
    
    time.sleep(0.8)
    
    # Realiza a ação de pressionar a tecla de espaço
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    time.sleep(0.2)
    
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.8)



def setup(driver, ext=5):
    driver.get('https://www.google.com.br/')
    
    # Pega o tempo inicial
    tempo_inicial = datetime.now()

    # Define o limite de tempo em segundos (30 segundos no seu caso)
    limite_tempo_segundos = 30

    while True:
        janelas_abertas = driver.window_handles

        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            driver.close()
            janelas_abertas = driver.window_handles
            driver.switch_to.window(janelas_abertas[0])
            break
        else:
            tempo_atual = datetime.now()
            tempo_decorrido = tempo_atual - tempo_inicial

            if tempo_decorrido.total_seconds() > limite_tempo_segundos:
                print("Tempo limite atingido. Saindo do loop.")
                return
    
    if ext == 1:
        install_ext_1(driver)
    elif ext == 2:
        install_ext_2(driver)
    elif ext == 3:
        install_ext_3(driver)
        
    elif ext == 4:
        install_ext_1(driver)
        install_ext_2(driver)
    
    elif ext == 5:
        install_ext_1(driver)
        install_ext_2(driver)
        install_ext_3(driver)
        
    
