import tkinter as tk
from tkinter import *
from PIL import ImageTk, Image
import customtkinter as ctk
import player_character as pc
import weapon as wpn
import re
import skills as sp
import math

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
            skill_dictionary[name] = sp.Skill(base_scaling, conditional_scaling, hit_count, name)
    return skill_dictionary

LUNE_WEAPONS = [wpn.Angerim, wpn.Benisim, wpn.Betalim, wpn.Braselim, 
                wpn.Chapelim, wpn.Choralim, wpn.Colim, wpn.Coralim,
                wpn.Deminerim, wpn.Elerim, wpn.Kralim, wpn.Lighterim,
                wpn.Lithelim, wpn.Lunerim, wpn.Painerim, wpn.Potierim,
                wpn.Redalim, wpn.Saperim, wpn.Scaverim, wpn.Snowim,
                wpn.Trebuchim, wpn.Troubadim]
LUNE_SKILLS = parse_skills_from_txt("skill_txt_files/lune_skills.txt")

VERSO_AND_GUSTAVE_WEAPONS = [wpn.Abysseram, wpn.Blodam, wpn.Chevalem, wpn.Confuso, 
                 wpn.Contorso, wpn.Corpeso, wpn.Cruleram, wpn.Cultam, 
                 wpn.Danseso, wpn.Delaram, wpn.Demonam, wpn.Dreameso, 
                 wpn.Dualiso, wpn.Gaulteram, wpn.Gesam, wpn.Glaceso, 
                 wpn.Lanceram, wpn.Liteso, wpn.Noahram, wpn.Nosaram, 
                 wpn.Sakaram, wpn.Seeram, wpn.Simoso, wpn.Sireso, 
                 wpn.Tireso, wpn.Verleso]
VERSO_SKILLS = parse_skills_from_txt("skill_txt_files/verso_skills.txt")
GUSTAVE_SKILLS = parse_skills_from_txt("skill_txt_files/gustave_skills.txt")

SCIEL_WEAPONS = [wpn.Algueron, wpn.Blizzon, wpn.Bourgelon, wpn.Charnon, 
                 wpn.Chation, wpn.Corderon, wpn.Direton, wpn.Garganon,
                 wpn.Gobluson, wpn.Guleson, wpn.Hevason, wpn.Litheson,
                 wpn.Lusteson, wpn.Martenon, wpn.Minason, wpn.Moisson,
                 wpn.Ramasson, wpn.Rangeson, wpn.Sadon, wpn.Scieleson,
                 wpn.Tisseron]
SCIEL_SKILLS = parse_skills_from_txt("skill_txt_files/sciel_skills.txt")

MONOCO_WEAPONS = [wpn.Ballaro, wpn.Boucharo, wpn.Brumaro, wpn.Chromaro, 
                  wpn.Fragaro, wpn.Grandaro, wpn.Joyaro, wpn.Monocaro,
                  wpn.Nusaro, wpn.Sidaro, wpn.Urnaro]
MONOCO_SKILLS = parse_skills_from_txt("skill_txt_files/monoco_skills.txt")

MAELLE_WEAPONS = [wpn.Barrier_Breaker, wpn.Battlum, wpn.Brulerum, wpn.Chalium, 
                 wpn.Chantenum, wpn.Clierum, wpn.Coldum, wpn.Duenum,
                 wpn.Facesum, wpn.Glaisum, wpn.Jarum, wpn.Lithum,
                 wpn.Maellum, wpn.Medalum, wpn.Melarum, wpn.Plenum,
                 wpn.Seashelum, wpn.Sekarum, wpn.Stalum, wpn.Tissenum,
                 wpn.Veremum, wpn.Volesterum, wpn.Yeverum]
MAELLE_SKILLS = parse_skills_from_txt("skill_txt_files/maelle_skills.txt")

NAME_TO_ITEMS = {"Verso" : VERSO_AND_GUSTAVE_WEAPONS, "Lune" : LUNE_WEAPONS, "Monoco" : MONOCO_WEAPONS, "Sciel": SCIEL_WEAPONS, "Maelle": MAELLE_WEAPONS, "Gustave" : VERSO_AND_GUSTAVE_WEAPONS}
NAME_TO_SKILLS = {"Verso" : VERSO_SKILLS, "Lune" : LUNE_SKILLS, "Monoco" : MONOCO_SKILLS, "Sciel": SCIEL_SKILLS, "Maelle": MAELLE_SKILLS, "Gustave" : GUSTAVE_SKILLS}

PICTOS_AND_BUFFS = {"At Death's Door" : ("MULTI", 1.5), "First Offense" : ("MULTI", 1.5), "Full Strength": ("MULTI", 1.25),
                    "Glass Canon" : ("MULTI", 1.25), "Roulette":("MULTI", 2.0), "Solo Fighter" : ("MULTI", 1.5), 
                    "Teamwork" : ("MULTI", 1.1), "Greater Defenseless":("MULTI", 1.40), "Greater Powerful" : ("MULTI", 1.4),
                    "Burn Affinity" : ("ADD", 0.25), "Confident Fighter" : ("ADD", 0.3), "Empowering Dodge(10 Stacks)" : ("ADD", 0,5), 
                    "Empowering Parry(10 Stacks)" : ("ADD", 0.5), "Exhausting Power": ("ADD", 0.5), "Gradient Fighter" : ("ADD", 0.25), 
                    "Immaculate" : ("ADD", 0.3), "Inverted Affinity" : ("ADD", 0.5), "Powered Attack" : ("ADD", 0.2), 
                    "Powerful Shield(9 stacks)" : ("ADD", 0.9), "Shield Affinity": ("ADD", 0.3), "Stun Boost" : ("ADD", 0.3), 
                    "Tainted(1 Stack)" : ("ADD", 0.15), "Warming Up(5 Stacks)" : ("ADD", 0.25)}
#NOTE Gradient fighter improperly applies to non gradient atks
#NOTE In game, it is not possible to have 5 stacks of Warming Up while having Inverted Affinity
#NOTE At Death's Door and Full Strength can be both selected even though it is not possible to have both buffs


active_item = None
active_skill = None
active_char = None
class CharacterSelection(tk.Frame):
    def move_to_character_screen(self, prev, character_name, frame_to_remove):
        customization_frame = Customization_Screen(self.parent, prev, character_name)
        customization_frame.pack(fill = "both")
        frame_to_remove.pack_forget()

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        tk.Label(self, text = "Select Character:").pack()

        #Create character buttons
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
        global active_char, active_item, active_skill
        active_skill = None
        active_char = None 
        active_item = None
        self.parent.update_idletasks()

    #Create the frame where stats and selections will go
    def __init__(self, parent, prev_frame, character_name):
        super().__init__(parent)
        self.parent = parent
        self.prev_frame = prev_frame

        global active_char
        active_char = NAME_TO_OBJECT[character_name]
        label = tk.Label(self, text = active_char.get_name()).pack()
        back_btn = tk.Button(self, text = "Back", command = self.return_to_char_select)
        back_btn.pack(side = "top", anchor = "nw")
        
        selection_screen = Select_Screen(self, self.parent, active_char)
        selection_screen.pack(side = "left")

class Select_Screen(tk.Frame):
    multiplicative_bonus = 1
    cumulative_bonus = 1

    def display_stats(self, frame, item = None, skill = None):
        #set active item and skill
        global active_item
        global active_skill
        if item == None and active_item == None:
            return
        elif item == None and active_item != None:
            pass
        else:
            active_item = item
        
        active_skill = skill
        if skill == None:
            character_skills =list(NAME_TO_SKILLS[self.character.get_name()].values())
            default_skill = character_skills[0]
            active_skill = default_skill

        #replace the window with updated stats
        if hasattr(self, 'stats') and self.stats.winfo_exists():
            self.stats.destroy()
        self.stats = Stat_Screen(frame, active_item, active_skill)
        self.stats.pack(in_=frame, anchor = "center", padx = (0, self.wpn_select.winfo_width()))

    def __init__(self, custom, parent, character):
        super().__init__(custom, width = 100)
        self.wpn_select = ctk.CTkScrollableFrame(self)
        self.skill_select = ctk.CTkScrollableFrame(self)
        self.buff_select = ctk.CTkScrollableFrame(self)

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
            btn = tk.Button(self.skill_select, text = ability, command = lambda skill = self.skill_set[ability], frame = custom: self.display_stats(frame, active_item, skill))
            btn.pack()
        self.skill_select.pack(side = "top")

        #picto and buff select
        def calc_buff_multipliers(is_checked, buff = (None, None)):
            bonus = buff
            if bonus == (None, None):
                return
            if is_checked.get():
                if bonus[0] == "MULTI":
                    Select_Screen.multiplicative_bonus *= bonus[1]
                else:
                    Select_Screen.cumulative_bonus += bonus[1]
            else:
                if bonus[0] == "MULTI":
                    Select_Screen.multiplicative_bonus /= bonus[1]
                else:
                    Select_Screen.cumulative_bonus -= bonus[1]
            self.display_stats(custom, active_item, active_skill)
        
        for bonus in PICTOS_AND_BUFFS:
            is_checked = BooleanVar()
            check_box = tk.Checkbutton(self.buff_select, text = bonus, variable = is_checked, command = lambda buff = PICTOS_AND_BUFFS[bonus], status = is_checked: calc_buff_multipliers(status, buff))
            check_box.pack()
        self.buff_select.pack()

        parent.title("Character Customization")
        

class Stat_Screen(tk.Frame):
    def change_lvl(self, direction):
        self.item.change_lvl(direction)
        self.ilvl = self.item.level

        self.new_base_atk = self.item.atk_levels[self.ilvl-1]
        self.new_final_atk = self.item.final_dmg 

        self.lvl_label.config(text = f"Level: {self.ilvl}")
        self.atk_label.config(text = f"Base Attack Power: {self.new_base_atk}")
        self.final_atk_label.config(text = f"Final Base Attack Power: {self.new_final_atk}")

        self.new_single_base_hit_skill = self.new_final_atk * active_skill.get_single_hit_base_multi() * Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.single_base_hit_skill_label.config(text = f"Single Hit Skill Dmg(no conditions met): {math.trunc(self.new_single_base_hit_skill)}" )

        self.new_single_final_hit_skill = self.new_final_atk  * active_skill.get_single_hit_final_multi() * Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.single_final_hit_skill_label.config(text = f"Single Hit Skill Dmg(conditions met): {math.trunc(self.new_single_final_hit_skill)}" )

        self.new_total_base_skill_dmg = self.new_final_atk  * active_skill.get_total_base_multi()* Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.total_base_skill_dmg_label.config(text = f"Total Dmg(no conditions met): {math.trunc(self.new_total_base_skill_dmg)}" )

        self.new_total_skill_dmg = self.new_final_atk  * active_skill.get_total_final_multi()* Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.total_skill_dmg_label.config(text = f"Total Dmg(conditions met): {math.trunc(self.new_total_skill_dmg)}" )
    
    def __init__(self, frame, item, skill):
        super().__init__()
        
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
        self.skill_name_label = tk.Label(self, text = skill.get_name(), font = ("Arial", 14, "underline"))

        self.single_base_hit_skill = self.final_atk_power * skill.get_single_hit_base_multi() * Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.single_base_hit_skill_label = tk.Label(self, text = f"Single Hit Skill Dmg(no conditions met): {math.trunc(self.single_base_hit_skill)}" )

        self.single_final_hit_skill = self.final_atk_power * skill.get_single_hit_final_multi()* Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.single_final_hit_skill_label = tk.Label(self, text = f"Single Hit Skill Dmg(conditions met): {math.trunc(self.single_final_hit_skill)}" )

        self.total_base_skill_dmg = self.final_atk_power * skill.get_total_base_multi()* Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.total_base_skill_dmg_label = tk.Label(self, text = f"Total Dmg(no conditions met): {math.trunc(self.total_base_skill_dmg)}" )

        self.total_skill_dmg = self.final_atk_power * skill.get_total_final_multi()* Select_Screen.multiplicative_bonus * Select_Screen.cumulative_bonus
        self.total_skill_dmg_label = tk.Label(self, text = f"Total Dmg(conditions met): {math.trunc(self.total_skill_dmg)}" )

        #packing
        self.down_btn.pack(side = tk.LEFT, anchor="nw", pady = 40)
        self.up_btn.pack(side =tk.RIGHT, anchor = "ne", pady = 40)
        self.divider = tk.Label(self, text = "")

        self.name_label.pack(pady = (0, 25))

        self.lvl_label.pack()
        self.atk_label.pack()
        self.final_atk_label.pack()
        self.divider.pack()

        self.skill_name_label.pack()
        self.single_base_hit_skill_label.pack()
        self.single_final_hit_skill_label.pack()
        self.total_base_skill_dmg_label.pack()
        self.total_skill_dmg_label.pack()

App()
