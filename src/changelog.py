import tkinter as tk
from tkinter import scrolledtext

def setup(root, y):
    # Calcula as coordenadas para a janela secundária ao lado da principal
    secondary_window_x = 80
    secondary_window_y = y

    secondary_window = tk.Toplevel(root)
    secondary_window.title("Log de Atualizações")
    secondary_window.geometry(f"400x400+{secondary_window_x}+{secondary_window_y}")
    secondary_window.resizable(False, False)
    secondary_window.overrideredirect(False)
    

    secondary_window.transient(root)

    # Adicione um botão para fechar a janela secundária
    button_close_secondary = tk.Button(secondary_window, text="Fechar", font=("Arial", 12), command=secondary_window.destroy)
    button_close_secondary.pack(pady=20)
    
    # Adicione um widget Text para exibir o log de atualizações
    text_log = scrolledtext.ScrolledText(secondary_window, wrap=tk.WORD, width=70, height=20, font=("Arial", 12))
    text_log.pack(padx=10, pady=10)

    # Carrega o conteúdo do arquivo de texto
    file_path = "src\\change_log.txt"  # Substitua pelo caminho do seu arquivo
    with open(file_path, "r", encoding="utf-8") as file:
        log_content = file.read()

    text_log.insert(tk.END, log_content)
    
    # Desabilita a edição do widget Text
    text_log.configure(state=tk.DISABLED)
