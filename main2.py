import os
import platform
import requests
import subprocess
import tempfile

temp_folder = tempfile.gettempdir()
app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")
os.makedirs(app_folder, exist_ok=True)

os.chdir(app_folder)

url = 'https://raw.githubusercontent.com/OneDefauter/Manga-Downloader/main/main.py'
path = os.path.join(temp_folder, "Mangá Downloader (APP)", "main.py")
sistema_operacional = platform.system()

response = requests.get(url)
with open(path, 'wb') as f:
    f.write(response.content)

if sistema_operacional == 'Windows':
    main_args = ['python', path]
else:
    main_args = ['python3', path]

subprocess.run(main_args)