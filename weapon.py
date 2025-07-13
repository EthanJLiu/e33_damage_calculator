import math
import Character
    
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

    def __init__(self, attributes, ilvl1_power, owner = Character.Player_Character()):
        self.owner = owner 
        self.ilvl1_power = ilvl1_power
        self.level = self.DEFAULT_ILVL 
        
        #Initialize current scaling range and attribute affinities
        self.attributes = attributes
        self.lvl_range = self.get_current_range(self.DEFAULT_ILVL)
        self.attribute_affinities = {attributes[0]:self.lvl_range[2], attributes[1]:self.lvl_range[3]}
        
        #initialize each level's corresponding base damage values 
        self.atk_levels = []
        self.get_atk_from_ilvl() #initializes all the attack values from ilvl

        self.final_dmg = self.calc_final_dmg()

    def calc_final_dmg(self):
        base_dmg = self.atk_levels[self.level-1]
        atk_from_char_level = self.get_atk_from_char_lvl()
        flat_might_inc = self.calc_might_scaling(self.owner.get_might())[0]
        percent_might_inc = self.calc_might_scaling(self.owner.get_might())[1]

        return atk_from_char_level + (base_dmg * percent_might_inc) + flat_might_inc + self.calc_attribute_scaling()[0] + self.calc_attribute_scaling()[1]
    
    def update_final_dmg(self):
        self.final_dmg = self.calc_final_dmg()

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
        self.base_dmg = self.atk_levels[self.level]

        if new_range != old_range:
            self.attribute_affinities = {self.attributes[0]:new_range[2], self.attributes[1]:new_range[3]}
        
        self.update_final_dmg()

    def calc_attribute_scaling(self):
        base = self.atk_levels[self.level-1]
        

        lower_attribute = self.attributes[0]
        
        lower_grade = self.attribute_affinities[lower_attribute]

        higher_attribute = self.attributes[1]
        higher_grade = self.attribute_affinities[higher_attribute]

        power_from_lower = self.owner.attribute_levels[lower_attribute] * self.GRADE_MULIPLIERS[lower_grade] * base
        power_from_higher = self.owner.attribute_levels[higher_attribute] * self.GRADE_MULIPLIERS[higher_grade] * base

        return power_from_higher, power_from_lower

# scaverim = Weapon(attributes = ("agility", "vitality"), ilvl1_power= 59)
# print ("Scaverim:" + str(scaverim.atk_levels[scaverim.level-1]))


# print(str(scaverim.level))
# print(str(scaverim.attribute_affinities))
# print(scaverim.get_atk_from_ilvl())
# print ("Scaverim:" + str(scaverim.final_dmg))


# elerim = Weapon(attributes = ("defense", "vitality"), ilvl1_power = 50)
# print(elerim.attribute_affinities)
# print(elerim.get_atk_from_char_lvl())
# print ("Elerim:" + str(elerim.final_dmg))
# print(elerim.atk_levels)

class Scaverim(Weapon):
    ILVL1_POWER = 59
    HIGH_AFFINITY = "vitality"
    LOW_AFFINITY = "agility"

    def __init__(self):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER)
        self.element = "dark"
        self.num_dark_stains = 0

    def get_dmg_from_wpn_skill(self):
        bonus = 0
        if self.num_dark_stains == 4:
            bonus = 6
        else:
            bonus = 1 + 0.5 * self.num_dark_stains
        return bonus

class Kralim(Weapon):
    ILVL1_POWER = 48
    HIGH_AFFINITY = "agility"
    LOW_AFFINITY = "vitality"
    def __init__(self):
        super().__init__(attributes=(self.LOW_AFFINITY, self.HIGH_AFFINITY), ilvl1_power=self.ILVL1_POWER)
    


        

scaverim = Scaverim()
print(scaverim.final_dmg)
    
