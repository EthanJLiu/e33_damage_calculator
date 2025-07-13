import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import Character

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Character Selection")
        self.geometry("600x600")

        self.char_select = CharacterSelection(self)

        self.mainloop()

class NavigationBar(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.grid()
        
        self.create_buttons()
    
characters = [{"name": "Lune", "image": "images/lune.png"}, {"name" : "Verso", "image": "images/verso.png"}, 
              {"name": "Sciel" , "image": "images/sciel.png"}, {"name" : "Maelle", "image": "images/maelle.png"}, 
              {"name" : "Monoco", "image": "images/monoco.png"}, {"name" : "Gustave", "image" : "images/gustave.png"}]

name_to_class_map = {"Lune" : Character.Lune(), "Verso" : Character.Verso(), "Sciel" : Character.Sciel(), 
                     "Maelle" : Character.Maelle(),"Monoco" : Character.Monoco(), "Gustave" : Character.Gustave()}




class CharacterSelection(tk.Frame):
    def move_to_character_screen(self, character_name, frame_to_remove):
        self.character = name_to_class_map[character_name]
        customization_frame = Customization_Screen(self.parent, character_name)
        customization_frame.grid()
        frame_to_remove.grid_forget()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        tk.Label(self, text = "Select Character:").grid(row = 1)
        
        for index, char in enumerate(characters):
            img = Image.open(char["image"]).resize((50,50))
            img = ImageTk.PhotoImage(img)
            print(char["name"])
            btn = tk.Button(self, image = img, text = char["name"], command = lambda name = char["name"], frame_to_remove = self: self.move_to_character_screen(name, frame_to_remove))
            btn.image = img 
            btn.grid(row = 2, column= index, ipadx = 10, padx = 10)
        
        self.grid(row = 2, pady = (0,20))
        

    
class Customization_Screen(tk.Frame):
    def return_to_home(self):
        self.grid_forget()
        
    def __init__(self, parent, character_name):
        self.parent = parent
        super().__init__(parent)
        label = tk.Label(self, text = character_name).grid(row = 1)
        
        back_btn = tk.Button(self, text = "Back", command = self.return_to_home)
        back_btn.grid(row = 0, column = 0)



    



App()
