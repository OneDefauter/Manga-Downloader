import time
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
    
    janelas_abertas = driver.window_handles
    
    for _ in range(1, 1200):
        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            break
        else:
            janelas_abertas = driver.window_handles
            time.sleep(0.1)
    
    time.sleep(1)
    
    # Realiza a ação de pressionar a tecla de espaço
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    time.sleep(1)
    
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(1)
    
    
def install_ext_2(driver):
    url_extension = 'https://update.greasyfork.org/scripts/482691/Teste.user.js'
    driver.get(url_extension)
    
    janelas_abertas = driver.window_handles
    
    for _ in range(1, 1200):
        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            break
        else:
            janelas_abertas = driver.window_handles
            time.sleep(0.1)
    
    time.sleep(1)
    
    # Realiza a ação de pressionar a tecla de espaço
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    time.sleep(1)
    
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(1)
    
    
def install_ext_3(driver):
    url_extension = 'https://update.greasyfork.org/scripts/472453/CloudFlare%20Challenge.user.js'
    driver.get(url_extension)
    
    janelas_abertas = driver.window_handles
    
    for _ in range(1, 1200):
        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            break
        else:
            janelas_abertas = driver.window_handles
            time.sleep(0.1)
    
    time.sleep(1)
    
    # Realiza a ação de pressionar a tecla de espaço
    ActionChains(driver).send_keys(Keys.SPACE).perform()
    
    time.sleep(1)
    
    janelas_abertas = driver.window_handles
    driver.switch_to.window(janelas_abertas[0])
    time.sleep(1)
    
    

def setup(driver, ext=5):
    driver.get('https://www.google.com.br/')
            
    janelas_abertas = driver.window_handles
    
    for _ in range(1, 15):
        if len(janelas_abertas) != 1:
            driver.switch_to.window(janelas_abertas[-1])
            driver.close()
            janelas_abertas = driver.window_handles
            driver.switch_to.window(janelas_abertas[0])
            break
        else:
            janelas_abertas = driver.window_handles
            time.sleep(1)
    
    if ext == 1:
        install_ext_1(driver)
    if ext == 2:
        install_ext_2(driver)
    if ext == 3:
        install_ext_3(driver)
        
    if ext == 4:
        install_ext_1(driver)
        install_ext_2(driver)
    
    if ext == 5:
        install_ext_1(driver)
        install_ext_2(driver)
        install_ext_3(driver)
