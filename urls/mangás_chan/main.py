import os
import re
import sys
import time
import shutil
import asyncio
import aiohttp
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from colorama import Fore, Style

import urls.mangás_chan.search as obter_capitulos
import urls.mangás_chan.run as run

async def setup(driver, url, capítulo, ate, debug_var, baixando_label, folder_selected, nome_foler, nome, compactar, compact_extension, extension):
    base_url = 'https://mangaschan.net/manga/'

    # Função para obter capítulos dentro de um intervalo
    capitulos_solicitados = obter_capitulos.obter_capitulos(driver, url, capítulo, ate, debug_var, baixando_label)
    
    if capitulos_solicitados == 0:
        driver.quit()

    if len(capitulos_solicitados) == 0:
        print("Nenhum capítulo encontrado")
        driver.quit()
        sys.exit()

    async with aiohttp.ClientSession() as session:
        os.system("cls")
        
        # Inverter a ordem dos capítulos
        capitulos_solicitados.reverse()
        
        for capitulo in capitulos_solicitados:
            numero_capitulo = str(capitulo['numero_capitulo']).replace('.0', '')
            url = capitulo['link']
            
            await run.run(driver, url, numero_capitulo, session, folder_selected, nome_foler, nome, debug_var, baixando_label, compactar, compact_extension, extension)
                
        driver.quit()
        
    return 0

