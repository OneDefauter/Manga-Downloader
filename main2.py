import os
import subprocess
import requests

temp_folder = os.environ['TEMP']
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")
os.makedirs(app_folder, exist_ok=True)

os.chdir(app_folder)

url = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/main.py'
path = os.path.join(temp_folder, "Mangá Downloader (APP)", "main.py")

response = requests.get(url)
with open(path, 'wb') as f:
    f.write(response.content)
    
main_args = ['python', path]
    
subprocess.run(main_args)