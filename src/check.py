import os
import subprocess

def setup():
    # Verificar se os módulos estão instalados
    required_modules = [
        'requests', 
        'pywin32', 
        'selenium', 
        'aiohttp', 
        'asyncio', 
        'colorama',
        'sv-ttk',
        'pytz',
    ]

    for module in required_modules:
        try:
            if module == 'pywin32':
                __import__('win32api')
                
            elif module == 'sv-ttk':
                __import__('sv_ttk')
            
            else:
                __import__(module)
                
        except ImportError:
            print(f"Módulo {module} não encontrado. Instalando...")
            subprocess.run(['pip', 'install', module])
            
    os.system('cls')

