from itertools import product

import math

class Unit():
    def __init__(self, mygroup, myworld):
        self.mygroup = mygroup
        self.myworld = myworld
        self.alive = True
        self.name = ""
        self.hp = 1
        self.x = 0
        self.y = 0
        self.attack_credit = 0
        self.surrounding_fields = list(product([-1, 0, 1],[-1, 0, 1]))

    def get_distance_to_target(self) -> int:
        return math.ceil(math.sqrt((self.x-self.target.x)**2 + (self.y-self.target.y)**2))
    
    def get_distance_to_xy(self, x, y) -> int:
        return math.ceil(math.sqrt((self.x-x)**2 + (self.y-y)**2))

    def get_distance_to_target_from_xy(self, x, y) -> int:
        return math.ceil(math.sqrt((x-self.target.x)**2 + (y-self.target.y)**2))