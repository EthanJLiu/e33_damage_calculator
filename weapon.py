class Weapon():
    def __init__(self, stats, grades, level = 15):
        self.level = level
        self.stat1 = [stats[0], grades[0]]
        self.stat2 = [stats[1], grades[1]]
        self.base_dmg = self.calc_base_damage()
    
    def calc_base_damage(self):  
        with open("might.txt", 'r') as f:
            lvl_bonuses = {}
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                data = line.split()
                lvl_bonuses.update({int(data[0]):int(data[1])})

        num_might = 99

        flat_inc = 0
        for i in range(1, num_might):
            flat_inc += lvl_bonuses[i]

        percent_inc = 1+0.005*num_might

        atk_power = 911
        dmg_from_weapon_lvl = 34
        base_dmg = (dmg_from_weapon_lvl*percent_inc) + (atk_power+flat_inc)
        return base_dmg
    

scaverim = Weapon(stats = ("vitality", "agility"), grades = ("S", "A"))

print (scaverim.base_dmg)


