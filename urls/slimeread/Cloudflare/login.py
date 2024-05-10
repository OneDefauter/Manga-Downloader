import time

async def login(driver, username, password):
    try:
        pagina = await driver.get('https://slimeread.com/login')
        
        await pagina
        
        campo_username = await pagina.select("input[id=name]")
        await campo_username.send_keys(username)
        
        campo_password = await pagina.select("input[id=password]")
        await campo_password.send_keys(password)
        
        btn = await pagina.select('button[type=submit]')
        await btn.click()
        
        time.sleep(1.750)
        
        try:
            erro_login = await pagina.find_element_by_text('Dados incorretos')
            if erro_login:
                print("Falha no login: Dados incorretos")
                return False
            
        except:
            # Se o elemento não for encontrado, o login não falhou por "Dados incorretos"
            print("Login bem-sucedido.")
            return True
        
    except Exception as e:
        print(f"Ocorreu um erro durante a tentativa de login: {e}")
        return False
