import os
import pickle
import src.time_zone as hora_agora


def setup(settings_dir):
    try:
        with open(f"{settings_dir}/settings.pickle", "rb") as file:
            settings = pickle.load(file)
        
        auto_save = settings["auto_save"]
        agregador_var = settings["agregador"]
        nome_var = settings["nome"]
        url_var = settings["url"]
        capitulo_var = settings["capitulo"]
        ate_var = settings["ate"]
        extension_var = settings["extensao"]
        compact_extension_var = settings["compact_extension"]
        nao_var = settings["nao_var"]
        sim_var = settings["sim_var"]
        debug_var = settings["debug"]
        debug2_var = settings["debug2"]
        headless_var = settings["headless"]
        folder_selected = settings["folder_selected"]
        theme = settings["theme"]
        print(hora_agora.setup(), "INFO:", "✔ Configurações carregadas")
        
    except:
        print(hora_agora.setup(), "INFO:", "✘ Erro ao carregar as configurações. Usando configuração padrão.")
        auto_save = False
        agregador_var = ""
        nome_var = ""
        url_var = ""
        capitulo_var = ""
        ate_var = ""
        extension_var = ".jpg"
        compact_extension_var = ".zip"
        nao_var = True
        sim_var = False
        debug_var = True
        debug2_var = False
        headless_var = True
        folder_selected = os.path.join(os.path.expanduser("~"), "Downloads")
        theme = 0
        
    return auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, nao_var, sim_var, debug_var, debug2_var, headless_var, folder_selected, theme
