import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

def login(driver, username, password):
    # username = "fadihof968@mcuma.com"
    # password = "0vL8.=qOm<6q"
    
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
        
        time.sleep(1.750)
        
        try:
            erro_login = driver.find_element(By.XPATH, "//h1[contains(text(), 'Dados incorretos')]")
            if erro_login:
                print("Falha no login: Dados incorretos")
                return False
            
        except NoSuchElementException:
            # Se o elemento não for encontrado, o login não falhou por "Dados incorretos"
            print("Login bem-sucedido ou falhou por outro motivo.")
            return True
        
    except Exception as e:
        print(f"Ocorreu um erro durante a tentativa de login: {e}")
        return False
