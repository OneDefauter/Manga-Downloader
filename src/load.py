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
        compact_var = settings["compact_var"]
        debug_var = settings["debug"]
        debug2_var = settings["debug2"]
        headless_var = settings["headless"]
        folder_selected = settings["folder_selected"]
        theme = settings["theme"]
        net_option_var = settings["net_option_var"]
        net_limit_down_var = settings["net_limit_down_var"]
        net_limit_up_var = settings["net_limit_up_var"]
        net_lat_var = settings["net_lat_var"]
        change_log_var = settings["change_log_var"]
        max_attent_var = settings["max_attententions"]
        max_verify_var = settings["max_verify_var"]
        user_var = settings["user_var"]
        pass_var = settings["pass_var"]
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
        compact_var = False
        debug_var = True
        debug2_var = False
        headless_var = True
        folder_selected = os.path.join(os.path.expanduser("~"), "Downloads")
        theme = 0
        net_option_var = False
        net_limit_down_var = 1024
        net_limit_up_var = 1024
        net_lat_var = 50
        change_log_var = True
        max_attent_var = 3
        max_verify_var = 50
        user_var = ""
        pass_var = ""
        
    return auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var, max_attent_var, max_verify_var, user_var, pass_var
