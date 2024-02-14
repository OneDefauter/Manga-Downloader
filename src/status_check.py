import time
import requests
from bs4 import BeautifulSoup

# Retornos
### 400 == Bad Request
### 401 == Unauthorized
### 403 == Forbidden
### 404 == Not Found

### 500 == Internal Server Error
### 502 == Bad Gateway
### 503 == Service Unavailable

def setup(driver, url, wait=3):
    
    time.sleep(wait)
    
    # Requisita
    response = requests.get(url)
    
    # Obtem o código de status da resposta
    status_code = response.status_code
    
    # driver.save_screenshot('save.png')
    
    # Erros 4xx
    if status_code == 400:
        print("Erro: URL inválida. Status code: 400")
        return 'e400'
    elif status_code == 401:
        print("Erro: Sem acesso. Status code: 401")
        return 'e401'
    elif status_code == 403:
        print("Erro: Sem acesso. Status code: 403")
        return 'e403'
    elif status_code == 404:
        print("Erro: URL inválida. Status code: 404")
        return 'e404'
    
    # Erros 5xx
    elif status_code == 500:
        print("Erro: Serviço indisponível. Status code: 500")
        return 'e500'
    elif status_code == 502:
        print("Erro: Serviço indisponível. Status code: 502")
        return 'e502'
    elif status_code == 503:
        print("Erro: Serviço indisponível. Status code: 503")
        return 'e503'
    elif status_code == 522:
        print("Erro: A conexão expirou. Status code: 522")
        return 'e522'
    
    # Verifica se a página está bloqueada pelo Cloudflare
    page_source = str(driver.page_source).lower()
    soup = BeautifulSoup(page_source, 'html.parser')
    
    if soup.title and "Cloudflare" in soup.title.string:
        print("Erro: Acesso bloqueado. Status code: 523")
        return 'e523'
    
    return 200
