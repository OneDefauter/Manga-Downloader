import os
import json
import nodriver as uc

temp_folder = os.environ['TEMP']
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")
profile_folder = os.path.join(temp_folder, "Mangá Downloader Profile")
download_folder = os.path.join(temp_folder, "Manga Downloader Temp Download")
extension_folder = os.path.join(app_folder, "src", "Violentmonkey 2.18.0.0")
pref_path = os.path.join(profile_folder, "Default", "Preferences")

def adicionar_partes_ausentes(json_data):
    # Verifica se a parte "download" está presente
    if "download" not in json_data:
        # Adiciona a parte "download" ao JSON
        json_data["download"] = {
            "default_directory": download_folder,
            "directory_upgrade": True,
            "prompt_for_download": False
        }
    
    # Verifica se a parte "safebrowsing" está presente
    if "safebrowsing" not in json_data:
        # Adiciona a parte "safebrowsing" ao JSON
        json_data["safebrowsing"] = {
            "disable_download_protection": True,
            "enabled": True
        }
    else:
        if not json_data["safebrowsing"]['enabled']:
            json_data["safebrowsing"]["enabled"] = True
            json_data["safebrowsing"]["disable_download_protection"] = True
    
    return json_data

async def setup():
    if os.path.exists(pref_path):
        with open(pref_path, encoding="latin1", mode='r') as file:
            json_data = json.load(file)
    
        if "download" not in json_data or not json_data["safebrowsing"]['enabled']:
            json_data = adicionar_partes_ausentes(json_data)
            
            with open(pref_path, encoding="latin1", mode='w') as file:
                json.dump(json_data, file, indent=2)
                
        browser_args = [
            '--start-maximized',
            f'--load-extension={extension_folder}'
        ]
        
        driver = await uc.start(user_data_dir=profile_folder, browser_args=browser_args)
        return driver
    
    else:
        browser_args = [
            f'--load-extension={extension_folder}'
        ]
    
        driver = await uc.start(user_data_dir=profile_folder, headless=True, browser_args=browser_args)
        driver.stop()
        
        with open(pref_path, encoding="latin1", mode='r') as file:
            json_data = json.load(file)
            
        json_data = adicionar_partes_ausentes(json_data)
        
        with open(pref_path, encoding="latin1", mode='w') as file:
            json.dump(json_data, file, indent=2)
        
        browser_args = [
            '--start-maximized',
            f'--load-extension={extension_folder}'
        ]
        
        driver = await uc.start(user_data_dir=profile_folder, browser_args=browser_args)
        return driver
