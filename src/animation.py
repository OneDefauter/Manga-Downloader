from tkinter import *
import ttkbootstrap as tb

class AnimationNotification():
    def __init__(self, root, version_, ian):
        self.root = root
        self.version_ = version_
        self.ian = ian
    
    def animation_text(self):
        self.text_info = tb.Label(self.root)
        self.text_info.place(relx=-0.32, rely=0.93, height=30, width=350)
        self.text_info.configure(text=self.version_)
        self.text_info.configure(font=("Segoe UI", 14, "bold"))
        
        self.relx_text = -0.32
        
        # Inicia a animação após um curto período
        self.root.after(1000, self.move_text)

    def move_text(self):
        self.ian = True
        while float(self.relx_text) < float(0.0):
            mov = 0.002 + self.relx_text
            self.relx_text = mov
            self.text_info.place(relx=mov, rely=0.93)
            self.root.update()
            
        self.root.after(3000, self.move_text2)

    def move_text2(self):
        while float(self.relx_text) > float(-0.32):
            mov = -0.002 + self.relx_text
            self.relx_text = mov
            self.text_info.place(relx=mov, rely=0.93)
            self.root.update()
        self.ian = False

    def move_text_wait(self, texto):
        if self.ian is False:
            self.text_info.configure(text=texto)
            self.move_text()
        else:
            self.root.after(1000, lambda: self.move_text_wait(texto))
        
