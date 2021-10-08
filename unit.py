import math
from itertools import product
from typing import Optional

class Unit():
    def __init__(self, mygroup, myworld) -> None:
        self.mygroup = mygroup
        self.myworld = myworld
        self.alive = True
        self.name = ''
        self.hp = 1
        self.x = 0
        self.y = 0
        self.surrounding_fields = list(product([-1, 0, 1],[-1, 0, 1]))
        self.target: Optional[Unit]
        self.attack_credit: float = 0.0

    def get_distance_to_target(self) -> int:
        if isinstance(self.target, Unit):
            return math.ceil(math.sqrt((self.x-self.target.x)**2 + (self.y-self.target.y)**2))
        else:
            return -1

    def get_distance_to_xy(self, x, y) -> int:
        if isinstance(self.target, Unit):
            return math.ceil(math.sqrt((self.x-x)**2 + (self.y-y)**2))
        else:
            return -1

    def get_distance_to_target_from_xy(self, x, y) -> int:
        if isinstance(self.target, Unit):
            return math.ceil(math.sqrt((x-self.target.x)**2 + (y-self.target.y)**2))
        else:
            return -1
