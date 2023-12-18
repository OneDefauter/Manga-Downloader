# Importações da pasta 'src'
import src.folder_main as first
import src.load as load_settings


# Importações 
import setup.ttk as themed


settings_dir = first.setup()


def load():
    # Carrega as configurações
    auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var = load_settings.setup(settings_dir)
    return auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var

def setup():
    auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var = load()
    
    theme = 'litera' if theme == 0 else theme
    
    themed.setup(auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var)
