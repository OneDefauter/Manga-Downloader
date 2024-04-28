import time
import threading
from tkinter import *
import ttkbootstrap as tb

class TempoDecorrido():
    def __init__(self, root):
        
        self.root = root
        
        self.tempo_decorrido = tb.Label(self.root)
        self.tempo_decorrido.place(relx=0.380, rely=0.96, height=63, width=195)
        self.tempo_decorrido.configure(text="00:00")
        self.tempo_decorrido.configure(font=("Segoe UI", 14, "bold"))
        
        self.rely_text = 0.96
        
        self.start_time = None
        self.running = False
        self.task = None
        
    def move_time(self):
        while float(self.rely_text) > float(0.89):
            mov = self.rely_text - 0.0002
            self.rely_text = mov
            self.tempo_decorrido.place(relx=0.380, rely=mov)
            self.root.update()
    
    def move_time2(self):
        while float(self.rely_text) < float(0.95):
            mov = self.rely_text + 0.0002
            self.rely_text = mov
            self.tempo_decorrido.place(relx=0.380, rely=mov)
            self.root.update()

    def atualizar_tempo(self):
        while self.running:
            if self.start_time:
                tempo_decorrido = self.calcular_tempo_decorrido()
                self.tempo_decorrido.configure(text=tempo_decorrido)
            time.sleep(1)
            self.root.update()
        if not self.running:
            self.root.after(10000, self.move_time2)

    def calcular_tempo_decorrido(self):
        if self.start_time:
            tempo_passado = int(time.time() - self.start_time)
            minutos, segundos = divmod(tempo_passado, 60)
            return f"{minutos:02d}:{segundos:02d}"
        else:
            return "00:00"

    async def iniciar_tempo(self):
        self.move_time()
        self.start_time = time.time()
        self.running = True
        threading.Thread(target=self.atualizar_tempo, daemon=True).start()

    async def parar_tempo(self):
        self.running = False
