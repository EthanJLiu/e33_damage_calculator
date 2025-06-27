import tkinter as tk
from tkinter import *

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Character Selection")
        self.geometry("600x600")
        
        #
        self.nav_bar = NavigationBar(self)
 
        #run
        self.mainloop()

class NavigationBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.place(x = 0, y = 0,relwidth= 0.3, relheight= 0.5)

        self.create_buttons()
    
    def create_buttons(self):
        back_btn = tk.Button(self, text = "back")
        back_btn.grid(row = 0, column = 0)
App()
