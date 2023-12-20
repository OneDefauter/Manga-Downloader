from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup(headless_var, agregador_escolhido, carregar_imagens, download_folder, extension_path, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var):
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_argument("--disable-notifications")
    
    if headless_var:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-web-security")
        
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false') # Desativa a renderização de iamgens
    
    chrome_options.add_argument('--log-level=3')  # Nível 3 indica "sem logs"
    
    chrome_options.add_argument("--disable-gpu")
    
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    
    chrome_options.add_argument('--no-sandbox')
    
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36")
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    if agregador_escolhido not in carregar_imagens:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    
    
    
    # chrome_options.add_argument(f"user-data-dir={profile_folder}")
    chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})
    
    if agregador_escolhido in ['Tsuki', 'Flower Manga']:
        chrome_options.add_extension(extension_path)
    
    # chrome_options.add_argument("--start-maximized")
    
    if net_option_var:
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        
        # Emular uma conexão lenta usando o Chrome DevTools Protocol
        devtools_options = chrome_options.to_capabilities()
        devtools_options["goog:chromeOptions"]["perfLoggingPrefs"] = {
            "enableNetwork": True,
            "enablePage": False,
            "enableTimeline": False
        }

        # Configurar a condição de rede lenta (por exemplo, GPRS)
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd("Network.emulateNetworkConditions", {
            "offline": False,
            "downloadThroughput": int(net_limit_down_var) * 1024,  # Velocidade de download em bytes por segundo
            "uploadThroughput": int(net_limit_up_var) * 1024,  # Velocidade de upload em bytes por segundo
            "latency": int(net_lat_var)  # Atraso em milissegundos
        })

    
    driver = webdriver.Chrome(options=chrome_options)
    
    return driver