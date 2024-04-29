import ttkbootstrap as tb

# Importações da pasta 'src'
import src.folder_main as first
import src.load as load_settings

# Importações 
import setup.ttk as main_setup


settings_dir = first.setup()

def load():
    # Carrega as configurações
    auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var, max_attent_var, max_verify_var, user_var, pass_var = load_settings.setup(settings_dir)
    return auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var, max_attent_var, max_verify_var, user_var, pass_var

def setup():
    auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var, max_attent_var, max_verify_var, user_var, pass_var = load()
    
    theme = 'litera' if theme == 0 else theme
    
    root = None
    
    root = tb.Window(
        title='Mangá Downloader', 
        themename=theme, 
        resizable=[False, False], 
        overrideredirect=False,
    )
    
    window_width = 1124
    window_height = 466
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    root.iconbitmap('images/icon.ico')
    
    app = main_setup.AppMain(root, auto_save, agregador_var, nome_var, url_var, capitulo_var, ate_var, extension_var, compact_extension_var, compact_var, debug_var, debug2_var, headless_var, folder_selected, theme, net_option_var, net_limit_down_var, net_limit_up_var, net_lat_var, change_log_var, max_attent_var, max_verify_var, user_var, pass_var, window_width, window_height, screen_width, screen_height, x, y)
    root.mainloop()
