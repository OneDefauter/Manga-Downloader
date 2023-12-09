import os
import src.time_zone as hora_agora

def setup():
    # Diretório onde o arquivo settings.pickle será salvo
    app_dir = os.path.join(os.path.expanduser("~"), "app")
    if not os.path.exists(app_dir):
        os.mkdir(app_dir)
        print(hora_agora.setup(), "INFO:", "✔ Pasta do app criada")
    
    settings_dir = os.path.join(app_dir, "MangaDownloader")
    if not os.path.exists(settings_dir):
        os.mkdir(settings_dir)
        print(hora_agora.setup(), "INFO:", "✔ Pasta de configuração criada")
    
    return settings_dir
