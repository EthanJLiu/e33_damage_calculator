import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import customtkinter as ctk
import player_character as pc
import weapon as wpn

Lune = pc.Lune()
Verso = pc.Verso()
Monoco = pc.Monoco()
Sciel = pc.Sciel()
Maelle = pc.Maelle()
Gustave = pc.Gustave()


class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Character Selection")
        self.geometry("600x600")
        self.attributes("-fullscreen", True)
        
        self.char_select = CharacterSelection(self)
        
        self.mainloop()        
    
CHARACTERS = [{"name": "Lune", "image": "images/lune.png"}, {"name" : "Verso", "image": "images/verso.png"}, 
              {"name": "Sciel" , "image": "images/sciel.png"}, {"name" : "Maelle", "image": "images/maelle.png"}, 
              {"name" : "Monoco", "image": "images/monoco.png"}, {"name" : "Gustave", "image" : "images/gustave.png"}]

NAME_TO_OBJECT = {"Lune" : Lune, "Verso" : Verso, "Sciel" : Sciel, 
                     "Maelle" : Maelle,"Monoco" : Monoco, "Gustave" : Gustave}

LUNE_WEAPONS = [wpn.Angerim, wpn.Benisim, wpn.Betalim, wpn.Braselim, 
            wpn.Chapelim, wpn.Choralim, wpn.Colim, wpn.Coralim,
            wpn.Deminerim, wpn.Elerim, wpn.Kralim, wpn.Lighterim,
            wpn.Lithelim, wpn.Lunerim, wpn.Painerim, wpn.Potierim,
            wpn.Redalim, wpn.Saperim, wpn.Scaverim, wpn.Snowim,
            wpn.Trebuchim, wpn.Troubadim]

VERSO_WEAPONS = {}
SCIEL_WEAPONS = {}
MONOCO_WEAPONS = {}
MAELLE_WEAPONS = {}
GUSTAVE_WEAPONS = {}

NAME_TO_ITEMS = {"Verso" : VERSO_WEAPONS, "Lune" : LUNE_WEAPONS, "Monoco" : MONOCO_WEAPONS, "Sciel": SCIEL_WEAPONS, "Maelle": MAELLE_WEAPONS, "Gustave" : GUSTAVE_WEAPONS}
# LUNE_SKILLS = []


class CharacterSelection(tk.Frame):
    def move_to_character_screen(self, prev, character_name, frame_to_remove):
        customization_frame = Customization_Screen(self.parent, prev, character_name)
        customization_frame.pack(fill = "both")
        frame_to_remove.pack_forget()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        tk.Label(self, text = "Select Character:").pack()
        
        for index, char in enumerate(CHARACTERS):
            img = Image.open(char["image"]).resize((75,75))
            img = ImageTk.PhotoImage(img)
            btn = tk.Button(self, image = img, 
                            command = lambda name = char["name"],frame_to_remove = self: 
                            self.move_to_character_screen(self, name, frame_to_remove))
            btn.image = img 
            btn.pack()
        
        self.pack()

class Customization_Screen(tk.Frame):
    def return_to_char_select(self):
        for frame in self.parent.winfo_children():
            if isinstance(frame, tk.Frame):
                frame.pack_forget()
        self.prev_frame.pack()
        self.parent.title("Character Select")
        self.parent.update_idletasks()

    def __init__(self, parent, prev_frame, character_name):
        super().__init__(parent)
        self.parent = parent
        self.prev_frame = prev_frame
        self.character = NAME_TO_OBJECT[character_name]
        label = tk.Label(self, text = self.character.get_name()).pack()
        
        back_btn = tk.Button(self, text = "Back", command = self.return_to_char_select)
        back_btn.pack(side = "top", anchor = "nw")
        
        wpn_select = Weapon_Select(self, self.parent, self.character)
        wpn_select.pack(side = "left")

class Weapon_Select(ctk.CTkScrollableFrame):
    def display_stats(self, item, frame):
        if hasattr(self, 'stats') and self.stats.winfo_exists():
            self.stats.destroy()
        self.stats = Stat_Screen(item, frame)
        self.stats.pack()

    def __init__(self, custom, parent, character):
        super().__init__(custom, width = 100)
        self.parent = parent
        self.character = character
        wpn_set = NAME_TO_ITEMS[self.character.get_name()]
        for i in range(len(wpn_set)):
            wp = wpn_set[i](self.character)
            btn = tk.Button(self, text = wp.get_name(), 
                            command= lambda item = wp, frame = custom: 
                            self.display_stats(item, frame))
            btn.pack()
        parent.title("Character Customization")

class Stat_Screen(tk.Frame):
    def change_lvl(self, direction):
        self.item.change_lvl(direction)
        self.ilvl = self.item.level


        self.new_base_atk = self.item.atk_levels[self.ilvl-1]
        self.new_final_atk = self.item.final_dmg

        self.lvl_label.config(text = f"Level: {self.ilvl}")
        self.atk_label.config(text = f"Base Attack: {self.new_base_atk}")
        self.final_atk_label.config(text = f"Final Base Attack: {self.new_final_atk}")

    def __init__(self, item, frame):
        super().__init__(bg='red')
        self.item = item
        self.ilvl = item.level
        self.name_label = tk.Label(self, text = f"{self.item.get_name()}")
        #base attack without attributes
        self.atk_power = item.atk_levels[self.ilvl-1]
        self.lvl_label = tk.Label(self, text = f"Level: {self.ilvl}")
        self.atk_label = tk.Label(self, text = f"Base Attack: {self.atk_power}")
        
        #with attributes
        self.final_atk_power = item.final_dmg
        self.final_atk_label = tk.Label(self, text = f"Final Base Attack: {self.final_atk_power}")

        #level buttons
        self.down_btn = tk.Button(self, text = "<--", command= lambda: self.change_lvl("DOWN"))
        self.up_btn = tk.Button(self, text = "-->", command = lambda: self.change_lvl("UP"))
        

        #packing
        self.down_btn.pack(side = tk.LEFT)
        self.up_btn.pack(side =tk.RIGHT)
        self.name_label.pack(pady = (0, 25))

        self.lvl_label.pack()
        self.atk_label.pack()
        self.final_atk_label.pack()




App()
