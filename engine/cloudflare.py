import os
from selenium import webdriver

import src.execute_driver as ins_ext

temp_folder = os.environ['TEMP']
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")
profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
download_folder = os.path.join(temp_folder, "Mangá Downloader Temp Download")
extension_path = os.path.join(app_folder, "src", "Violentmonkey 2.18.0.0.crx")

def setup():
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    options.add_experimental_option("excludeSwitches", ["enable-automation"])
    options.add_experimental_option('useAutomationExtension', False)
    options.add_argument("--disable-blink-features=AutomationControlled")
    # options.add_argument('--disable-extensions')
    options.add_argument('--start-maximized')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-gpu')
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument('--log-level=3')
    options.add_argument(f"user-data-dir={profile_folder}")
    options.add_extension(extension_path)
    options.add_experimental_option("prefs", {"download.default_directory": download_folder})
    driver = webdriver.Chrome(options=options)
    
    driver.get("https://google.com")
    ins_ext.setup(driver)
    
    return driver
