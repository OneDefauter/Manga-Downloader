import undetected_chromedriver as uc

import src.execute_driver as ins_ext

def setup(extension_folder, download_folder):
    chrome_options = uc.ChromeOptions()
    chrome_options.add_argument("--disable-popup-blocking")
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument('--disable-extensions')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-infobars')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-browser-side-navigation')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--log-level=3')
    chrome_options.add_argument(f'--load-extension={extension_folder}')
    chrome_options.add_experimental_option("prefs", {"download.default_directory": download_folder})
    
    driver = uc.Chrome(options=chrome_options)
    
    driver.get("https://google.com")
    ins_ext.setup(driver, 2)
    ins_ext.setup(driver, 3)
    
    return driver