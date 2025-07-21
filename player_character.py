# import weapon


class Player_Character():
    def __init__(self, name = None, skills = None):
        self.level = 99
        self.attribute_levels = {"vitality": 99, "might": 99, "agility": 99, "defense": 99, "luck": 99}
        self.skills = skills
        self.name = name 
    
    def update_attribute(self, attribute, direction):
        if self.attribute_levels[attribute] == 0 and direction == "DOWN":
            return
        elif self.attribute_levels[attribute] == 99 and direction == "UP":
            return
        else:
            self.attribute_levels[attribute] += 1 if direction == "UP" else -1

    def get_lvl(self):
        return self.level
    
    def get_might(self):
        return self.attribute_levels["might"]
    
    def get_name(self):
        return self.name
    


class Lune(Player_Character):
    def __init__(self):
        super().__init__(name = "Lune")
    
class Verso(Player_Character):
    def __init__(self):
        super().__init__(name = "Verso")

class Maelle(Player_Character):
    def __init__(self):
        super().__init__(name = "Maelle")

class Sciel(Player_Character):
    def __init__(self):
        super().__init__(name = "Sciel")

class Gustave(Player_Character):
    def __init__(self):
        super().__init__(name = "Gustave")

class Monoco(Player_Character):
    def __init__(self):
        super().__init__(name = "Monoco")
    

    
    

