class Player_Character():
    def __init__(self, weapons = None):
        self.level = 99
        self.attribute_levels = {"vitality": 99, "might": 99, "agility": 99, "defense": 0, "luck": 0}
        self.weapons = weapons
    
    def get_lvl(self):
        return self.level
    
    def get_might(self):
        return self.attribute_levels["might"]
    
    

