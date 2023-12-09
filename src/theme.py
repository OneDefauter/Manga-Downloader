import tkinter as tk
from tkinter import ttk
import src.time_zone as hora_agora
import sv_ttk


# Temas
# Tema 1 (Sun Valley (Dark))
# Tema 2 (Sun Valley (Light))

# Tema 3 (Azure (Dark))
# Tema 4 (Azure (Light))

# Tema 5 (Forest (Dark))
# Tema 6 (Forest (Light))



def sucess():
    print(hora_agora.setup(), "INFO:", "✔ Tema carregado com sucesso")



def error(e):
    print(hora_agora.setup(), "INFO:", "✘ Houve um erro ao carregar o tema.\n", e)



def setup(root, theme):
    
    # Tema 1 (Sun Valley (Dark))
    if theme == 1:
        try:
            sv_ttk.set_theme("dark")
            sucess()
        except Exception as e:
            error(e)
    
    # Tema 2 (Sun Valley (Light))
    elif theme == 2:
        try:
            sv_ttk.set_theme("light")
            sucess()
        except Exception as e:
            error(e)
    
    # Tema 3 (Azure (Dark))
    elif theme == 3:
        try:
            root.tk.call("source", "themes\\azure\\azure.tcl")
            root.tk.call("set_theme", "dark")
            sucess()
        except Exception as e:
            error(e)
    
    # Tema 4 (Azure (Light))
    elif theme == 4:
        try:
            root.tk.call("source", "themes\\azure\\azure.tcl")
            root.tk.call("set_theme", "light")
            sucess()
        except Exception as e:
            error(e)
    
    # Tema 5 (Forest (Dark))
    elif theme == 5:
        try:
            style = ttk.Style(root)
            root.tk.call("source", "themes\\forest\\forest-dark.tcl")
            style.theme_use("forest-dark")
            sucess()
        except Exception as e:
            error(e)
    
    # Tema 6 (Forest (Light))
    elif theme == 6:
        try:
            style = ttk.Style(root)
            root.tk.call("source", "themes\\forest\\forest-light.tcl")
            style.theme_use("forest-light")
            sucess()
        except Exception as e:
            error(e)
            
        
