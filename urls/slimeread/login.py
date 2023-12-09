import time
from selenium.webdriver.common.keys import Keys

def login(driver):
    username = "yenic25188@frandin.com"
    password = "M8e.Dcd4.Wd$vdj"
    
    try:
        driver.get('https://slimeread.com/login')
        
        time.sleep(1)
        
        # Encontra os campos de entrada de nome de usuário e senha usando seus nomes
        campo_username = driver.find_element("name", "name")
        campo_password = driver.find_element("name", "password")
        
        # Insere o nome de usuário e senha
        campo_username.send_keys(username)
        campo_password.send_keys(password)
        
        # Submete o formulário de login
        campo_password.send_keys(Keys.RETURN)
        
        time.sleep(1)
    except:
        ...
