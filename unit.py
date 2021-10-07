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

    def get_distance_to_target(self):
        return math.ceil(math.sqrt((self.x-self.target.x)**2 + (self.y-self.target.y)**2))
