import math
import player_character as pc

class Weapon():
    
    MIN_ILVL = 1
    MAX_ILVL = 33
    DEFAULT_ILVL = 15

    WHITE = (.508, 1, "D", "C")
    LVL3_TO_4 = (.327, 3, "D", "C")
    BLUE = (.369, 4, "C", "B")
    LVL9_TO_10 = (.211, 9, "C", "B")
    PURPLE = (.167, 10, "C", "B")
    LVL19_TO_20 = (.144, 19, "C", "B")
    YELLOW = (.086, 20, "B", "A")
    MAX = (.3252, 32, "A", "S")

    GRADE_MULIPLIERS = {"S" : 0.01004, "A" : 0.00632, "B": 0.00365, "C" : 0.001838, "D" : 0.0008345}

    def __init__(self, attributes, ilvl1_power, name, owner = pc.Player_Character()):
        self.owner = owner
        self.ilvl1_power = ilvl1_power
        self.level = self.DEFAULT_ILVL 
        self.name = name
        
        #Initialize current scaling range and attribute affinities
        self.attributes = attributes
        self.lvl_range = self.get_current_range(self.DEFAULT_ILVL)
        self.attribute_affinities = {attributes[0]:self.lvl_range[2], attributes[1]:self.lvl_range[3]}
        
        #initialize each level's corresponding base damage values 
        self.atk_levels = []
        self.get_atk_from_ilvl() #initializes all the attack values from ilvl

        self.final_dmg = math.ceil(self.calc_final_dmg())

    def calc_final_dmg(self):
        base_dmg = self.atk_levels[self.level-1]
        atk_from_char_level = self.get_atk_from_char_lvl()
        flat_might_inc = self.calc_might_scaling(self.owner.get_might())[0]
        percent_might_inc = self.calc_might_scaling(self.owner.get_might())[1]

        return atk_from_char_level + (base_dmg * percent_might_inc) + flat_might_inc + self.calc_attribute_scaling()[0] + self.calc_attribute_scaling()[1]
    
    def update_final_dmg(self):
        self.final_dmg = math.ceil(self.calc_final_dmg())

    #Returns the percent increase corresponding to the different level ranges, which have varied scaling and grades
    def get_current_range(self, level):
        match level:
            case l if l >= 1 and l <3:
                return self.WHITE
            case l if l == 3:
                return self.LVL3_TO_4
            case l if l >=4 and l < 9:
                return self.BLUE
            case l if l == 9:
                return self.LVL9_TO_10
            case l if l >=10 and l < 19:
                return self.PURPLE
            case l if l == 19:
                return self.LVL19_TO_20
            case l if l >= 20 and l < 32:
                return self.YELLOW
            case l if l >= 32:
                return self.MAX
            
    def get_atk_from_ilvl(self):
        power = self.ilvl1_power
        self.atk_levels.append(power)
        scale_from = power

        for i in range(1, 33):
            r = self.get_current_range(i)
            multi = r[0]
            base = r[1]
            if i == base:
                scale_from = power
            power = power + (scale_from * multi)
            self.atk_levels.append(math.ceil(power))

    def get_atk_from_char_lvl(self):
        atk_from_char_lvl = math.trunc(15 + 13.6 * (self.owner.get_lvl()-1))
        return atk_from_char_lvl

    def calc_might_scaling(self, num_might):  
        with open("might.txt", 'r') as f:
            lvl_bonuses = {}
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                data = line.split()
                lvl_bonuses.update({int(data[0]):int(data[1])})

        flat_inc = 0
        for i in range(1, num_might):
            flat_inc += lvl_bonuses[i]

        percent_inc = 1+(0.005*num_might)

        return flat_inc, percent_inc

    def change_lvl(self, direction):
        old_range = self.get_current_range(self.level)
        if self.level == 33 and direction == "UP":
            return
        if self.level == 1 and direction == "DOWN":
            return
        
        self.level += 1 if direction == "UP" else -1
        new_range = self.get_current_range(self.level)
        self.base_dmg = self.atk_levels[self.level-1]

        if new_range != old_range:
            self.attribute_affinities = {self.attributes[0]:new_range[2], self.attributes[1]:new_range[3]}
        
        self.update_final_dmg()

    def calc_attribute_scaling(self):
        base = self.atk_levels[self.level-1]
        
        lower_attribute = self.attributes[0]
        if lower_attribute != None:
            lower_grade = self.attribute_affinities[lower_attribute]

        higher_attribute = self.attributes[1]
        higher_grade = self.attribute_affinities[higher_attribute]
        if lower_attribute != None:
            power_from_lower = self.owner.attribute_levels[lower_attribute] * self.GRADE_MULIPLIERS[lower_grade] * base
        else:
            power_from_lower = 0

        power_from_higher = self.owner.attribute_levels[higher_attribute] * self.GRADE_MULIPLIERS[higher_grade] * base

        return power_from_higher, power_from_lower
    
    def get_name(self):
        return self.name

#region Lune Weapons
class Angerim(Weapon):
    ILVL1_POWER = 46
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "defense"
    ID = "Angerim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)
    
class Benisim(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Benisim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Betalim(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Betalim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Braselim(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Braselim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Chapelim(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Chapelim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)
    
class Choralim(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Choralim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Colim(Weapon):
    ILVL1_POWER = 36
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Colim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Coralim(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "vitality"
    ID = "Coralim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Deminerim(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Deminerim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)
    
class Elerim(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Elerim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Kralim(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Kralim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Lighterim(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Lighterim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Lithelim(Weapon):
    ILVL1_POWER = 44
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "luck"
    ID = "Lithelim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Lunerim(Weapon):
    ILVL1_POWER = 34
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Lunerim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)
    
class Painerim(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Painerim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Potierim(Weapon):
    ILVL1_POWER = 41
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Potierim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Redalim(Weapon):
    ILVL1_POWER = 36
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Redalim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Saperim(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "luck"
    ID = "Saperim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)
    
class Scaverim(Weapon):
    ILVL1_POWER = 59
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Scaverim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)
        self.element = "dark"
        self.num_dark_stains = 0

    def get_dmg_from_wpn_skill(self):
        bonus = 0
        if self.num_dark_stains == 4:
            bonus = 6
        else:
            bonus = 1 + 0.5 * self.num_dark_stains
        return bonus
    
class Snowim(Weapon):
    ILVL1_POWER = 54
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Snowim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Trebuchim(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "luck"
    ID = "Trebuchim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character)

class Troubadim(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "vitality"
    ID = "Troubadim"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 
#endregion
    
#region Verso/Gustave Weapons
class Abysseram(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Abysseram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Blodam(Weapon):
    ILVL1_POWER = 49
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Blodam"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Chevalem(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Chevalem"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Confuso(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Confuso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Contorso(Weapon):
    ILVL1_POWER = 40
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Contorso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Corpeso(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Corpeso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Cruleram(Weapon):
    ILVL1_POWER = 49
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "luck"
    ID = "Cruleram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Cultam(Weapon):
    ILVL1_POWER = 44
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Cultam"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Danseso(Weapon):
    ILVL1_POWER = 42
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Danseso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Delaram(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Delaram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Demonam(Weapon):
    ILVL1_POWER = 40
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Demonam"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Dreameso(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Dreameso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Dualiso(Weapon):
    ILVL1_POWER = 25
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Dualiso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Gaulteram(Weapon):
    ILVL1_POWER = 46
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Gaulteram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Gesam(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Gesam"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Glaceso(Weapon):
    ILVL1_POWER = 41
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "defense"
    ID = "Glaceso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Lanceram(Weapon):
    ILVL1_POWER = 52
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Lanceram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Liteso(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Liteso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Noahram(Weapon):
    ILVL1_POWER = 32
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = None
    ID = "Noahram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Nosaram(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Nosaram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Sakaram(Weapon):
    ILVL1_POWER = 41
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Sakaram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Seeram(Weapon):
    ILVL1_POWER = 52
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Seeram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Simoso(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Simoso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Sireso(Weapon):
    ILVL1_POWER = 36
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Sireso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Tireso(Weapon):
    ILVL1_POWER = 52
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Tireso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Verleso(Weapon):
    ILVL1_POWER = 49
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = None
    ID = "Verleso"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

#endregion

#region Sciel Weapons
class Algueron(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "luck"
    ID = "Algueron"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Blizzon(Weapon):
    ILVL1_POWER = 59
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "defense"
    ID = "Blizzon"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Bourgelon(Weapon):
    ILVL1_POWER = 44
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Bourgelon"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Charnon(Weapon):
    ILVL1_POWER = 42
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "defense"
    ID = "Abysseram"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Chation(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Chation"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Corderon(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "luck"
    ID = "Corderon"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Direton(Weapon):
    ILVL1_POWER = 57
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Direton"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Garganon(Weapon):
    ILVL1_POWER = 44
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Garganon"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Gobluson(Weapon):
    ILVL1_POWER = 47
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Gobluson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Guleson(Weapon):
    ILVL1_POWER = 44
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Guleson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Hevason(Weapon):
    ILVL1_POWER = 49
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Hevason"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Litheson(Weapon):
    ILVL1_POWER = 40
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Litheson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Lusteson(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Lusteson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Martenon(Weapon):
    ILVL1_POWER = 54
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Martenon"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Minason(Weapon):
    ILVL1_POWER = 40
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Minason"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Moisson(Weapon):
    ILVL1_POWER = 47
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Moisson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Ramasson(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Ramasson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Rangeson(Weapon):
    ILVL1_POWER = 44
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Rangeson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Sadon(Weapon):
    ILVL1_POWER = 36
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Sadon"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Scieleson(Weapon):
    ILVL1_POWER = 49
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Scieleson"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Tisseron(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Tisseron"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 


#endregion

#region Monoco Weapons
class Ballaro(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Ballaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Boucharo(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Boucharo"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Brumaro(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Brumaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Chromaro(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Chromaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Fragaro(Weapon):
    ILVL1_POWER = 59
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "defense"
    ID = "Fragaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Grandaro(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Grandaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Joyaro(Weapon):
    ILVL1_POWER = 52
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Joyaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Monocaro(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "luck"
    ID = "Monocaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Nusaro(Weapon):
    ILVL1_POWER = 59
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Nusaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Sidaro(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "might"
    ID = "Sidaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Urnaro(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "luck"
    ID = "Urnaro"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

#endregion

#region Maelle Weapons
class Barrier_Breaker(Weapon):
    ILVL1_POWER = 51
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Barrier Breaker"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Battlum(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "luck"
    ID = "Battlum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Brulerum(Weapon):
    ILVL1_POWER = 39
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Brulerum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Chalium(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Chalium"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Chantenum(Weapon):
    ILVL1_POWER = 40
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Chantenum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Clierum(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Clierum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Coldum(Weapon):
    ILVL1_POWER = 36
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "defense"
    ID = "Coldum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Duenum(Weapon):
    ILVL1_POWER = 34
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Duenum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Facesum(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Facesum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Glaisum(Weapon):
    ILVL1_POWER = 52
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Glaisum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Jarum(Weapon):
    ILVL1_POWER = 36
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "luck"
    ID = "Jarum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Lithum(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "agility"
    ID = "Lithum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Maellum(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = None
    ID = "Maellum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Medalum(Weapon):
    ILVL1_POWER = 41
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Medalum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Melarum(Weapon):
    ILVL1_POWER = 50
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "luck"
    ID = "Melarum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Plenum(Weapon):
    ILVL1_POWER = 43
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "defense"
    ID = "Plenum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Seashelum(Weapon):
    ILVL1_POWER = 42
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "defense"
    ID = "Seashelum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Sekarum(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"
    ID = "Sekarum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Stalum(Weapon):
    ILVL1_POWER = 45
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "luck"
    ID = "Stalum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Tissenum(Weapon):
    ILVL1_POWER = 54
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Tissenum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Veremum(Weapon):
    ILVL1_POWER = 46
    HIGH_AFFINITY = "luck"
    LOW_AFFINITY = "vitality"
    ID = "Veremum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Volesterum(Weapon):
    ILVL1_POWER = 46
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    ID = "Volesterum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

class Yeverum(Weapon):
    ILVL1_POWER = 7
    HIGH_AFFINITY = "defense"
    LOW_AFFINITY = "agility"
    ID = "Yeverum"
    def __init__(self, character):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER, name = self.ID, owner= character) 

#endregion