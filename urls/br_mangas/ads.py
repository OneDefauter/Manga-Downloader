import os
import time
import shutil
import asyncio
from colorama import Fore, Style
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains


def setup(driver):
    elemento = driver.find_element(By.CSS_SELECTOR, 'div[id^="google_ads_iframe_"]')
    
    elemento.click()
    
    try:
        # Espera até que a nova guia seja carregada
        WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))  # Aguarda até que haja duas guias abertas
    
        janelas_abertas = driver.window_handles
        driver.switch_to.window(janelas_abertas[1])
        driver.close()
        time.sleep(1)
        
        janelas_abertas = driver.window_handles
        driver.switch_to.window(janelas_abertas[0])
        time.sleep(1)
    except:
        pass
