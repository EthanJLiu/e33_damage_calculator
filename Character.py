class Player_Character():
    def __init__(self, weapons = None):
        self.level = 99
        self.vitality = 0
        self.might = 0
        self.agility = 0
        self.defense = 0
        self.luck = 0
        self.attribute_levels = {"vitality": 0, "might": 0, "agility": 0, "defense": 0, "luck": 0}
        self.weapons = weapons
    
    def get_lvl(self):
        return self.level
    

