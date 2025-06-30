import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Character Selection")
        self.geometry("600x600")
        
        
        self.nav_bar = NavigationBar(self)

        #set character select
        self.char_select = CharacterSelection(self)

        #run
        self.mainloop()

class NavigationBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        
        self.create_buttons()
    
    def create_buttons(self):
        back_btn = tk.Button(self, text = "back")
        back_btn.grid(row = 0, column = 0)

characters = [{"name": "Lune", "image": "images/lune.png"}, {"name" : "Verso", "image": "images/verso.png"}, 
              {"name": "Sciel" , "image": "images/sciel.png"}, {"name" : "Maelle", "image": "images/maelle.png"}, 
              {"name" : "Monoco", "image": "images/monoco.png"}, {"name" : "Gustave", "image" : "images/gustave.png"}]

class CharacterSelection(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(text = "Select Character:").grid(row = 1)

        for index, char in enumerate(characters):
            img = Image.open(char["image"]).resize((50,50))
            img = ImageTk.PhotoImage(img)

            btn = tk.Button(self, image = img, text = char["name"])
            btn.image = img #prevents image garbage collecting
            btn.grid(row = 1, column= index, padx = 10)
        
        self.grid(row = 2, pady = (0,20))
App()
