import os
from selenium import webdriver
import src.Scripts.setup as ins_ext


temp_folder = os.environ['TEMP'] if os.name == 'nt' else os.environ['tmp']
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")
profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
download_folder = os.path.join(temp_folder, "Manga Downloader Temp Download")
extension_path = os.path.join(app_folder, "src", "Violentmonkey 2.18.0.0.crx")

def setup(headless_var):
    chrome_options = webdriver.ChromeOptions()
    
    chrome_options.add_experimental_option("detach", True)
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    # options.add_argument("--headless=new")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-web-security')
    chrome_options.add_argument('--allow-running-insecure-content')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(f"user-data-dir={profile_folder}")
    
    prefs = {
        "safebrowsing.enabled": True,  # Ativa o Safe Browsing
        "safebrowsing.disable_download_protection": True,  # Desativa a proteção de download
        "download.prompt_for_download": False,  # Desativa a solicitação de download
        "download.directory_upgrade": True,  # Permite atualizações de diretório
        "download.default_directory": download_folder, # Define o diretório padrão para downloads
    }
    
    chrome_options.add_experimental_option("prefs", prefs)
    chrome_options.add_extension(extension_path)
    
    if headless_var:
        chrome_options.add_argument("--headless=new")
    else:
        chrome_options.add_argument('--start-maximized')
    
    driver = webdriver.Chrome(options=chrome_options)
    
    driver.get("https://google.com")
    
    ins_ext.setup_not_cloudflare(driver)
    
    return driver