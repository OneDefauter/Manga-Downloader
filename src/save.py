import os
import pickle
import src.time_zone as hora_agora

def setup(settings_dir, auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, nao_var, sim_var, debug_var, debug2_var, headless_var, folder_select, theme):
    settings = {
        "auto_save": auto_save.get(),
        "agregador": agregador_var.get(),
        "nome": nome_var.get(),
        "url": url_var.get(),
        "capitulo": capitulo_var.get(),
        "ate": ate_var.get(),
        "extensao": extension_var.get(),
        "compact_extension": compact_extension_var.get(),
        "nao_var": nao_var.get(),
        "sim_var": sim_var.get(),
        "debug": debug_var.get(),
        "debug2": debug2_var.get(),
        "headless": headless_var.get(),
        "folder_selected": folder_select,
        "theme": theme
        # Adicione outros dados que você deseja salvar automaticamente aqui
    }

    with open(f"{settings_dir}/settings.pickle", "wb") as file:
        pickle.dump(settings, file)
    
    print(hora_agora.setup(), "INFO:", "✔ Configurações salvas")