import os
import time
from selenium import webdriver

temp_folder = os.environ['TEMP']
profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
download_folder = os.path.join(temp_folder, "Mangá Downloader Temp Download")
extension_url = 'https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/Tampermonkey.5.0.0.0.crx'
extension_zip_url = 'https://github.com/OneDefauter/Manga-Downloader/releases/download/Main/Tampermonkey.5.0.0.0.zip'
extension_name = "Tampermonkey.5.0.0.0.crx"
extension_path = os.path.join(temp_folder, extension_name)
extension_folder_path = os.path.join(temp_folder, 'Tampermonkey.5.0.0.0')

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
    driver = webdriver.Chrome(options=options)
    
    
    time.sleep(3)
    
    return driver
