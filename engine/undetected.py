import os
from undetected_chromedriver import Chrome, ChromeOptions
import undetected_chromedriver as uc

def setup(headless_var, agregador_escolhido, carregar_imagens, download_folder, extension_path, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var):
    chrome_options = ChromeOptions()
    
    chrome_options.add_argument("--disable-notifications")
    
    if headless_var:
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-web-security")
        
    # chrome_options.add_argument('--blink-settings=imagesEnabled=false') # Desativa a renderização de iamgens
    
    chrome_options.add_argument('--log-level=3')  # Nível 3 indica "sem logs"
    
    chrome_options.add_argument("--disable-gpu")
    
    chrome_options.add_argument('--no-sandbox')
    
    chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    
    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    
    if agregador_escolhido not in carregar_imagens:
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
    
    # chrome_options.add_argument(f"user-data-dir={profile_folder}")
    chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})
    
    if agregador_escolhido in ['Tsuki', 'Flower Manga', 'Hentai Teca']:
        temp_folder = os.environ['TEMP']
        extension_folder_path = os.path.join(temp_folder, 'Tampermonkey.5.0.0.0')
        chrome_options.add_argument(f'--load-extension={extension_folder_path}')
    
    # chrome_options.add_argument("--start-maximized")
    
    if net_option_var:
        chrome_options.add_argument("--proxy-server='direct://'")
        chrome_options.add_argument("--proxy-bypass-list=*")
        
        # Emular uma conexão lenta usando o Chrome DevTools Protocol
        uc.enable_cdp()
        uc.add_options("--proxy-server='direct://'")
        uc.add_options("--proxy-bypass-list=*")
        uc.set_capability("goog:chromeOptions", {
            "perfLoggingPrefs": {
                "enableNetwork": True,
                "enablePage": False,
                "enableTimeline": False
            }
        })

        # Configurar a condição de rede lenta (por exemplo, GPRS)
        driver = Chrome(options=chrome_options)
        uc.emulate_network_conditions(
            driver,
            offline=False,
            download_throughput=int(net_limit_down_var) * 1024,
            upload_throughput=int(net_limit_up_var) * 1024,
            latency=int(net_lat_var)
        )
    else:
        driver = Chrome(options=chrome_options)

    return driver
