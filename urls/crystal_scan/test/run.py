import re
import time
from urllib.parse import urlparse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys

url = 'https://crystalscan.net/manga/youre-not-decrypting-it-at-all-are-you/cap-00/'

chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_argument('--log-level=3')
chrome_options.add_argument('--ignore-certificate-errors')

# Inicializa o WebDriver (use o caminho para o seu driver)
driver = webdriver.Chrome(options=chrome_options)

# Abre a página
driver.get(url)

time.sleep(1)

leitor = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CLASS_NAME, "reading-content"))
)

paginas = leitor.find_elements(By.CLASS_NAME, 'page-break')

# Função para rolar até a imagem e aguardar o carregamento
def scroll_to_image(image_element):
    driver.execute_script("arguments[0].scrollIntoView();", image_element)
    wait_time = 0
    while not image_element.get_attribute("complete") and wait_time < 10:
        time.sleep(1)
        wait_time += 1

# Itera sobre as imagens
for pagina in paginas:
    imagem = pagina.find_element(By.TAG_NAME, 'img')
    scroll_to_image(imagem)
    
    # Aqui você pode adicionar o código para baixar a imagem ou qualquer outra ação desejada
    print(imagem.get_attribute('src'))
