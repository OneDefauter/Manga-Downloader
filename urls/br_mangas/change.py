import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from colorama import Fore, Style

def setup(driver):
    # Localiza o elemento do menu suspenso pelo ID
    select_modo_leitura = driver.find_element(By.ID, 'modo_leitura')

    # Cria um objeto Select para interagir com o menu suspenso
    modo_leitura_dropdown = Select(select_modo_leitura)

    # Obtém o valor atual do modo de leitura
    modo_atual = modo_leitura_dropdown.first_selected_option.get_attribute('value')

    print(f'{Fore.GREEN}INFO:{Style.RESET_ALL} Modo atual de leitura: {modo_atual}')

    # Verifica se o modo atual é o desejado (por exemplo, 'Páginas abertas')
    if modo_atual != '2':
        # Seleciona a opção desejada ('Páginas abertas')
        modo_leitura_dropdown.select_by_value('2')  # Troque '2' pelo valor da opção desejada

        # Espera até que o novo conteúdo seja carregado após a seleção
        driver.implicitly_wait(10)
        
        print(f"{Fore.GREEN}INFO:{Style.RESET_ALL} Modo de leitura alterado para: Páginas abertas\n")

        time.sleep(3)
        
