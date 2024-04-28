import time
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


# Image Downloader
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
    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    
    time.sleep(0.2)
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
    
    time.sleep(0.2)
    
    driver.close()
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.2)


# Teste
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

    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    
    time.sleep(0.2)
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()    
    
    time.sleep(0.2)
    
    driver.close()
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.2)


# CloudFlare Challenge
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
    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    
    time.sleep(0.2)
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()    
    
    time.sleep(0.2)
    
    driver.close()
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.2)


# Popup
def install_ext_4(driver):
    url_extension = 'https://update.greasyfork.org/scripts/467776/%F0%9F%92%AF%20%E6%87%92%E4%BA%BA%E4%B8%93%E7%94%A8%E7%B3%BB%E5%88%97%20%E2%80%94%E2%80%94%E2%80%94%20%E5%85%A8%E7%BD%91%20VIP%20%E8%A7%86%E9%A2%91%E7%A0%B4%E8%A7%A3%E5%8E%BB%E5%B9%BF%E5%91%8A.user.js'
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
    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    
    time.sleep(0.2)
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()    
    
    time.sleep(0.2)
    
    driver.close()
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.2)


# Popup
def install_ext_5(driver):
    url_extension = 'https://userscripts.adtidy.org/release/popup-blocker/2.5/popupblocker.user.js'
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
    
    try:
        wait = WebDriverWait(driver, 2)
        wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    except:
        driver.refresh()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    
    time.sleep(0.2)
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()    
    
    time.sleep(0.2)
    
    driver.close()
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.2)


# Picviewer
def install_ext_6(driver):
    url_extension = 'https://update.greasyfork.org/scripts/24204/Picviewer%20CE%2B.user.js'
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
    
    wait = WebDriverWait(driver, 30)
    wait.until(EC.element_to_be_clickable((By.ID, 'confirm')))
    
    time.sleep(0.2)
    
    ActionChains(driver).key_down(Keys.CONTROL).send_keys(Keys.ENTER).key_up(Keys.CONTROL).perform()
    
    time.sleep(0.2)
    
    driver.close()
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(0.2)




def setup(
    driver,
    pd = False,
    e_01 = False,
    e_02 = False,
    e_03 = False,
    e_04 = False,
    e_05 = False,
    e_06 = False,
    e_07 = False
):
    if pd:
        install_ext_1(driver)
        install_ext_2(driver)
        install_ext_3(driver)
        install_ext_6(driver)
    else:
        if e_01:
            install_ext_1(driver)
        if e_02:
            install_ext_2(driver)
        if e_03:
            install_ext_3(driver)
        if e_04:
            install_ext_4(driver)
        if e_05:
            install_ext_5(driver)
        if e_06:
            install_ext_6(driver)
        if e_07:
            install_ext_6(driver)
            install_ext_2(driver)
