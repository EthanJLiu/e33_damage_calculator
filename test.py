import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import customtkinter as ctk
import player_character as pc
import weapon as wpn
import re
import skills_and_pictos as sp

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

def parse_skills_from_txt(text):
    skill_dictionary = {}
    with open(text, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data = re.split(r"(?<=\s)(?=\d+)", line)
            data = [item.strip() for item in data]
            name = data[0]
            base_scaling = data[3]
            hit_count = data[4]
            conditional_scaling = data[5]
            skill_dictionary[name] = sp.Skill(base_scaling, conditional_scaling, hit_count)
    return skill_dictionary

LUNE_WEAPONS = [wpn.Angerim, wpn.Benisim, wpn.Betalim, wpn.Braselim, 
            wpn.Chapelim, wpn.Choralim, wpn.Colim, wpn.Coralim,
            wpn.Deminerim, wpn.Elerim, wpn.Kralim, wpn.Lighterim,
            wpn.Lithelim, wpn.Lunerim, wpn.Painerim, wpn.Potierim,
            wpn.Redalim, wpn.Saperim, wpn.Scaverim, wpn.Snowim,
            wpn.Trebuchim, wpn.Troubadim]
LUNE_SKILLS = parse_skills_from_txt("skill_txt_files/lune_skills.txt")

VERSO_WEAPONS = {}
VERSO_SKILLS = parse_skills_from_txt("skill_txt_files/verso_skills.txt")

SCIEL_WEAPONS = {}
SCIEL_SKILLS = parse_skills_from_txt("skill_txt_files/sciel_skills.txt")

MONOCO_WEAPONS = {}
MONOCO_SKILLS = parse_skills_from_txt("skill_txt_files/monoco_skills.txt")

MAELLE_WEAPONS = {}
MAELLE_SKILLS =parse_skills_from_txt("skill_txt_files/maelle_skills.txt")

GUSTAVE_WEAPONS = {}
GUSTAVE_SKILLS = parse_skills_from_txt("skill_txt_files/gustave_skills.txt")

NAME_TO_ITEMS = {"Verso" : VERSO_WEAPONS, "Lune" : LUNE_WEAPONS, "Monoco" : MONOCO_WEAPONS, "Sciel": SCIEL_WEAPONS, "Maelle": MAELLE_WEAPONS, "Gustave" : GUSTAVE_WEAPONS}
NAME_TO_SKILLS = {"Verso" : VERSO_SKILLS, "Lune" : LUNE_SKILLS, "Monoco" : MONOCO_SKILLS, "Sciel": SCIEL_SKILLS, "Maelle": MAELLE_SKILLS, "Gustave" : GUSTAVE_SKILLS}

active_char = None
active_item = None
active_skill = None

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
        active_char = NAME_TO_OBJECT[character_name]
        label = tk.Label(self, text = active_char.get_name()).pack()
        
        back_btn = tk.Button(self, text = "Back", command = self.return_to_char_select)
        back_btn.pack(side = "top", anchor = "nw")
        
        wpn_select = Select(self, self.parent, active_char)
        wpn_select.pack(side = "left")

class Select(tk.Frame):
    def display_stats(self, frame, item = None, skill = None):

        if item == None:
            return
        
        #set active item and skill
        active_item = item
        active_skill = skill

        if hasattr(self, 'stats') and self.stats.winfo_exists():
            self.stats.destroy()
        self.stats = Stat_Screen(frame, active_item, active_skill)
        self.stats.pack(in_=frame, anchor = "center", padx = (0, self.wpn_select.winfo_width()))

    def __init__(self, custom, parent, character):
        super().__init__(custom, width = 100, bg= "red")
        self.wpn_select = ctk.CTkScrollableFrame(self)
        self.skill_select = ctk.CTkScrollableFrame(self)

        self.parent = parent
        self.character = character

        #weapon select
        self.wpn_set = NAME_TO_ITEMS[self.character.get_name()]
        for i in range(len(self.wpn_set)):
            wp = self.wpn_set[i](self.character)
            btn = tk.Button(self.wpn_select, text = wp.get_name(), 
                            command= lambda item = wp, frame = custom: 
                            self.display_stats(frame, item, active_skill))
            btn.pack()
        self.wpn_select.pack(side = "top")
        
        #skill select
        self.skill_set = NAME_TO_SKILLS[self.character.get_name()]
        for ability in self.skill_set:
            btn = tk.Button(self.skill_select, text = ability, command = lambda skill = ability, frame = custom: self.display_stats(frame, active_item, skill))
            btn.pack()
        parent.title("Character Customization")
        self.skill_select.pack(side = "top")

class Stat_Screen(tk.Frame):
    def change_lvl(self, direction):
        self.item.change_lvl(direction)
        self.ilvl = self.item.level

        self.new_base_atk = self.item.atk_levels[self.ilvl-1]
        self.new_final_atk = self.item.final_dmg

        self.lvl_label.config(text = f"Level: {self.ilvl}")
        self.atk_label.config(text = f"Base Attack Power: {self.new_base_atk}")
        self.final_atk_label.config(text = f"Final Base Attack Power: {self.new_final_atk}")

    def __init__(self, frame, item, skill):
        super().__init__(bg='red')
        

             
        self.item = item
        self.ilvl = item.level
        self.name_label = tk.Label(self, text = f"{self.item.get_name()}")
        
        #base atk power without attributes
        self.atk_power = item.atk_levels[self.ilvl-1]
        self.lvl_label = tk.Label(self, text = f"Level: {self.ilvl}")
        self.atk_label = tk.Label(self, text = f"Base Attack Power: {self.atk_power}")
        
        #atk powerwith attributes
        self.final_atk_power = item.final_dmg
        self.final_atk_label = tk.Label(self, text = f"Final Base Attack Power: {self.final_atk_power}")

        #level buttons
        self.down_btn = tk.Button(self, text = "<--", command= lambda: self.change_lvl("DOWN"))
        self.up_btn = tk.Button(self, text = "-->", command = lambda: self.change_lvl("UP"))
        
        #expected skill damage
        if skill != None:
            print("hellow")
            self.single_base_hit_skill = self.final_atk_power * skill.get_single_hit_base_multi()
            self.single_base_hit_skill_label = tk.Label(self, text = f"Single Hit Skill Dmg(no conditions met): {self.single_base_hit_skill}" )

            self.single_final_hit_skill = self.final_atk_power * skill.get_single_hit_final_multi()
            self.single_final_hit_skill_label = tk.Label(self, text = f"Single Hit Skill Dmg(conditions met): {self.single_final_hit_skill}" )

            self.total_base_skill_dmg = self.final_atk_power * skill.get_total_base_multi()
            self.total_base_skill_dmg_label = tk.Label(self, text = f"Total Dmg(no conditions met): {self.total_base_skill_dmgl}" )

            self.total_skill_dmg = self.final_atk_power * skill.get_total_final_multi()
            self.total_skill_dmg_label = tk.Label(self, text = f"Total Dmg(conditions met): {self.total_skill_dmg}" )

        #packing
        self.down_btn.pack(side = tk.LEFT)
        self.up_btn.pack(side =tk.RIGHT)
        self.name_label.pack(pady = (0, 25))

        
        self.lvl_label.pack()
        self.atk_label.pack()
        self.final_atk_label.pack()

        self.skill_name_label = tk.Label(self, text = skill)

        self.single_base_hit_skill_label.pack()
        self.single_final_hit_skill_label.pack()
        self.total_base_skill_dmg_label.pack()
        self.total_skill_dmg_label.pack()

App()
