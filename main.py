import os
import sys
import platform
import subprocess
from io import BytesIO
import importlib.metadata
from zipfile import ZipFile
from threading import Timer

namespace = "OneDefauter"
repo = f"https://api.github.com/repos/{namespace}/Manga-Downloader/releases"

def raise_error(ex):
    print(ex)

def install_modules():
    # Verificar se os módulos estão instalados
    required_modules = [
        'requests', 
        'pywin32', 
        'selenium', 
        'aiohttp', 
        'asyncio', 
        'colorama',
        'pytz',
        'ttkbootstrap',
        'undetected_chromedriver',
        'bs4',
        'Pillow',
        'imageio',
        'imageio[pyav]',
        'Wand',
        'packaging',
        'nodriver',
    ]

    for module in required_modules:
        try:
            if module == 'pywin32':
                sistema_operacional = platform.system()
                if sistema_operacional == 'Windows':
                    __import__('win32api')
            
            elif module == 'Pillow':
                __import__('PIL')
                
            elif module == 'imageio[pyav]':
                __import__("imageio")
                
            elif module == 'Wand':
                from wand.image import Image
            
            else:
                __import__(module)
                
        except ImportError:
            print(f"Módulo {module} não encontrado. Instalando...")
            subprocess.run(['pip', 'install', module])
        
        except:
            ...
            
    os.system('cls' if os.name == 'nt' else 'clear')

def get_latest_version(package_name):
    url = f"https://pypi.org/pypi/{package_name}/json"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        latest_version = data["info"]["version"]
        return latest_version
    else:
        print(f"Erro ao obter informações da versão para {package_name}.")
        return None

def get_installed_version(package_name):
    try:
        return importlib.metadata.version(package_name)
    except importlib.metadata.PackageNotFoundError:
        return None

def check_update_modules():
    latest_version = get_latest_version("undetected_chromedriver")
    installed_version = get_installed_version("undetected_chromedriver")
    if latest_version != installed_version:
        subprocess.run(['pip', 'install', '--upgrade', "undetected_chromedriver"])

def download_and_execute():
    temp_folder = os.environ['TEMP'] if os.name == 'nt' else os.environ['tmp']
    app_folder = os.path.join(temp_folder, "Mangá Downloader (APP)")
    path_file = os.path.join(app_folder, "setup", "main.py")
    
    os.makedirs(app_folder, exist_ok=True)
    os.chdir(app_folder)
    sys.path.append(app_folder)
    
    if os.path.exists(path_file):
        if os.path.exists(os.path.join(app_folder, "__init__.py")):
            with open(os.path.join(app_folder, "__init__.py"), 'r') as file:
                for line in file:
                    if line.startswith('__version__'):
                        __version__ = line.split('=')[1].strip().strip('"\'')
        else:
            __version__ = "0.0" # Force update
    else:
        __version__ = "1.0" # Initial version
    
    remote_release = requests.get(repo)
    local_version = version.parse(__version__)
    
    if remote_release.ok:
        remote_release_json = remote_release.json()
        remote_beta_version = None
        for release in remote_release_json:
            if release['prerelease'] == True:
                if remote_beta_version is None:
                    remote_beta_version = version.parse(release["tag_name"])
                    zip_resp_beta = requests.get(release["zipball_url"])
                    if zip_resp_beta.ok:
                        myzip_beta = ZipFile(BytesIO(zip_resp_beta.content))
                        zip_root_beta = [z for z in myzip_beta.infolist() if z.is_dir()][0].filename
                        zip_files_beta = [z for z in myzip_beta.infolist() if not z.is_dir()]
            else:
                remote_version = version.parse(release["tag_name"])
                zip_resp = requests.get(release["zipball_url"])
                if zip_resp.ok:
                    myzip = ZipFile(BytesIO(zip_resp.content))
                    zip_root = [z for z in myzip.infolist() if z.is_dir()][0].filename
                    zip_files = [z for z in myzip.infolist() if not z.is_dir()]
                break
        
        if not os.path.exists(path_file):
            for fileinfo in zip_files:
                filename = os.path.join(app_folder, fileinfo.filename.replace(zip_root, ""))
                dirname = os.path.dirname(filename)
                os.makedirs(dirname, exist_ok=True)
                file_data = myzip.read(fileinfo)

                with open(filename, "wb") as fopen:
                    fopen.write(file_data)
        else:
            if remote_version > local_version:
                print(f"Nova atualização.\nVersão atual: {local_version}\nNova versão: {remote_version}")
                timeout = 10
                t = Timer(timeout, raise_error, [ValueError("\nAtualização cancelada")])
                t.start()
                answer = input("Você deseja atualizar agora? (s/n)\n")
                t.cancel()

                if answer.lower() in ["true", "1", "t", "y", "yes", "sim", "s", "ok"]:
                    update = True
                else:
                    update = False
                    
                if update:
                    for fileinfo in zip_files:
                        filename = os.path.join(app_folder, fileinfo.filename.replace(zip_root, ""))
                        dirname = os.path.dirname(filename)
                        os.makedirs(dirname, exist_ok=True)
                        file_data = myzip.read(fileinfo)

                        with open(filename, "wb") as fopen:
                            fopen.write(file_data)
            
            elif remote_beta_version:
                if remote_version <= local_version and remote_beta_version > local_version:
                    print(f"Nova atualização BETA.\nVersão atual: {local_version}\nNova versão: {remote_beta_version}")
                    timeout = 10
                    t = Timer(timeout, raise_error, [ValueError("\nAtualização cancelada")])
                    t.start()
                    print("Você deseja atualizar para versão BETA agora? (s/n)")
                    answer = input("Lembre-se que a versão BETA pode conter erros.\n")
                    t.cancel()

                    if answer.lower() in ["true", "1", "t", "y", "yes", "sim", "s", "ok"]:
                        update = True
                    else:
                        update = False
                        
                    if update:
                        for fileinfo in zip_files_beta:
                            filename = os.path.join(app_folder, fileinfo.filename.replace(zip_root_beta, ""))
                            dirname = os.path.dirname(filename)
                            os.makedirs(dirname, exist_ok=True)
                            file_data = myzip_beta.read(fileinfo)

                            with open(filename, "wb") as fopen:
                                fopen.write(file_data)
                
                
    
    if os.path.exists(path_file):
        from src.ImageMagick.setup import setup as ImageMagickSetup
        
        ImageMagickSetup()
        
        # Importação da pasta 'Setup'
        import setup.main as setup_main

        # Inicia a GUI
        setup_main.setup()

if __name__ == "__main__":
    install_modules()
    import requests
    check_update_modules()
    from packaging import version
    download_and_execute()