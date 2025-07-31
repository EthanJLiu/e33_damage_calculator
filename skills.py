
import weapon as wpn

class Skill():
    def __init__(self, base_scaling, conditional_scaling, hit_count, name):
        self.base_scaling = float(base_scaling)
        self.conditional_scaling = float(conditional_scaling)
        self.hit_count = float(hit_count)
        self.name = name
    def get_single_hit_base_multi(self):
        return self.base_scaling

    def get_single_hit_final_multi(self):
        return self.conditional_scaling * self.base_scaling

    def get_total_base_multi(self):
        return self.hit_count * self.base_scaling

    def get_total_final_multi(self):
        return self.hit_count * self.conditional_scaling * self.base_scaling
    
    def get_name(self):
        return self.name
    
    def __str__(self):
        return f"base: {self.base_scaling}, conditional: {self.conditional_scaling}, hit: {self.hit_count}, name: {self.name}"

