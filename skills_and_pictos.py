
import weapon as wpn
import math

class Skill():
    def __init__(self, base_scaling, conditional_scaling, hit_count, wp = wpn.Weapon()):
        self.wpn_atk_dmg = wp.final_dmg
        self.base_scaling = base_scaling
        self.conditional_acaling = conditional_scaling
        self.hit_count = hit_count
    
    def get_single_hit_base_dmg(self):
        

    def get_single_hit_final_dmg(self):
        pass

    def get_total_base_dmg(self):
        pass

    def get_total_final_dmg(self):
        pass