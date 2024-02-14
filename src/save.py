import pickle
import src.time_zone as hora_agora

def setup(settings_dir, auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_select, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var):
    settings = {
        "auto_save": auto_save.get(),
        "agregador": agregador_var.get(),
        "nome": nome_var.get(),
        "url": url_var.get(),
        "capitulo": capitulo_var.get(),
        "ate": ate_var.get(),
        "extensao": extension_var.get(),
        "compact_extension": compact_extension_var.get(),
        "compact_var": compact_var.get(),
        "debug": debug_var.get(),
        "debug2": debug2_var.get(),
        "headless": headless_var.get(),
        "folder_selected": folder_select,
        "theme": theme,
        "net_option_var": net_option_var.get(),
        "net_limit_down_var": net_limit_down_var.get(),
        "net_limit_up_var": net_limit_up_var.get(),
        "net_lat_var": net_lat_var.get(),
        "change_log_var": change_log_var.get()
        # Adicione outros dados que você deseja salvar automaticamente aqui
    }

    with open(f"{settings_dir}/settings.pickle", "wb") as file:
        pickle.dump(settings, file)
    
    print(hora_agora.setup(), "INFO:", "✔ Configurações salvas")