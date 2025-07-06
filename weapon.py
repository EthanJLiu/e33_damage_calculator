import math

class Weapon():
    
    DEFAULT_ILVL = 15

    RANGE1_TO_3 = (.504, 1)
    RANGE3_TO_4 = (.327, 3)
    RANGE4_TO_9 = (.369, 4)
    RANGE9_TO_10 = (.211, 9)
    RANGE10_TO_19 = (.167, 10)
    RANGE19_TO_20 = (.144, 19)
    RANGE20_TO_32 = (.086, 20)
    RANGE32_TO_33 = (.3252, 32)

    def __init__(self, stats, grades, ilvl1_power):
        self.ilvl1_power = ilvl1_power #the starting power for an item level 1 weapon
        self.level = self.DEFAULT_ILVL #the default item level when a weapon is selected
        self.stat1 = [stats[0], grades[0]]
        self.stat2 = [stats[1], grades[1]]
        self.base_dmg = self.calc_might_scaling(99)
        #self.base_dmg = self.get_atk_from_ilvl(15)

    #Returns the percent increase corresponding to the different level ranges, which have varied scaling and grades
    def get_current_range(self, level):
        match level:
            case l if l >= 1 and l <3:
                return self.RANGE1_TO_3
            case l if l == 3:
                return self.RANGE3_TO_4
            case l if l >=4 and l < 9:
                return self.RANGE4_TO_9
            case l if l == 9:
                return self.RANGE9_TO_10
            case l if l >=10 and l < 19:
                return self.RANGE10_TO_19
            case l if l == 19:
                return self.RANGE19_TO_20
            case l if l >= 20 and l < 32:
                return self.RANGE20_TO_32
            case l if l == 32:
                return self.RANGE32_TO_33
            
    def get_atk_from_ilvl(self, level):
        power = self.ilvl1_power
        scale_from = power
        for i in range(1, level):
            r = self.get_current_range(i)
            multi = r[0]
            base = r[1]
            if i == base:
                scale_from = power
            power = power + (scale_from * multi)
            
        return int(power)
    
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

        percent_inc = 1+0.005*num_might

        atk_power = 1347
        dmg_from_ilvl = self.get_atk_from_ilvl(33)
        base_dmg = (dmg_from_ilvl*percent_inc) + (atk_power+flat_inc)
        return math.ceil(base_dmg)
    


kralim = Weapon(stats = ("vitality", "agility"), grades = ("S", "A"), ilvl1_power= 48)
print ("Kralim:" + str(kralim.base_dmg))

scaverim = Weapon(stats = ("vitality", "agility"), grades = ("S", "A"), ilvl1_power= 59)
print ("Scaverim:" + str(scaverim.base_dmg))

lunerim = Weapon(stats = ("vitality", "agility"), grades = ("S", "A"), ilvl1_power= 34)
print ("Lunerim:" + str(lunerim.base_dmg))

medalum = Weapon(stats = ("vitality", "agility"), grades = ("S", "A"), ilvl1_power= 41)
print ("medalum:" + str(medalum.base_dmg))

simoso = Weapon(stats = ("vitality", "agility"), grades = ("S", "A"), ilvl1_power= 45)
print ("simoso:" + str(simoso.base_dmg))

