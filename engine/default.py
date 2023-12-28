from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def setup(headless_var, agregador_escolhido, profile_folder, download_folder, extension_path, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var):
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(f"user-data-dir={profile_folder}")
    chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})
    chrome_options.add_extension(extension_path)
    
    if headless_var and agregador_escolhido != 'Mangás Chan':
        chrome_options.add_argument("--headless=new")
    
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