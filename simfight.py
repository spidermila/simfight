import math
from random import randint
from typing_extensions import runtime

class World:
    def __init__(self):
        self.x = 50
        self.y = 30
        self.groups = []
    
    def place_units(self):
        number_of_groups = len(self.groups)
        rows = int(number_of_groups / 2)
        gid = 0
        for row in range(rows):
            # populate left side of the map first
            group = self.groups[gid]
            left_col_x_min = 1
            left_col_x_max = int(self.x / 2)
            y_min = int((self.y / rows) * row + 1)
            y_max = int((self.y / rows) * (row + 1))
            x_next = left_col_x_min
            y_next = y_min
            for unit in group.members:
                if x_next > left_col_x_max:
                    y_next += 1
                    x_next = left_col_x_min
                    if y_next > y_max:
                        print(f"Too many units to fit on the map! {row=}, {group.name=}")
                unit.x = x_next
                x_next += 1
                unit.y = y_next
            
            # populate right side of the map next
            gid += 1
            right_col_x_min = int(self.x / 2) + 1
            right_col_x_max = self.x
            group = self.groups[gid]
            x_next = right_col_x_min
            y_next = y_min
            for unit in group.members:
                if x_next > right_col_x_max:
                    y_next += 1
                    x_next = right_col_x_min
                    if y_next > y_max:
                        print(f"Too many units to fit on the map! {row=}, {group.name=}")
                unit.x = x_next
                x_next += 1
                unit.y = y_next
                


class Group:
    def __init__(self, name):
        self.name = name
        self.members = []


class Unit():
    def __init__(self, mygroup, myworld):
        self.mygroup = mygroup
        self.myworld = myworld
        self.name = ""
        self.hp = 1
        self.x = 0
        self.y = 0


class Fighter(Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = "fighter"
        self.hp = 10
        self.move_speed = 2
        self.attack_speed = 1.0
        self.attack_max_range = 1
        self.attack_min_range = 1
        self.attack_min_damage = 2
        self.attack_max_damage = 10
        self.accuracy = 80
        self.target = None

    def pick_target(self):
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    self.target = group.members[randint(0, len(group.members) - 1)]
                    return True
        return False

    def do_something(self):
        if not self.target:
            if self.pick_target():
                pass
            else:
                print(f"{self.name} - nothing to target. Combat is over.")
                return False
        # if not close enough, move to target
        # only move this turn, number of fields moved depends on the unit's speed
        for i in range(self.move_speed):
            straight_dist = round(math.sqrt((self.x-self.target.x)**2 + (self.y-self.target.y)**2))
            if straight_dist > self.attack_max_range:
                x_dist = self.x - self.target.x
                y_dist = self.y - self.target.y
                if abs(x_dist) > abs(y_dist):
                    if x_dist > 0:
                        self.x -= 1
                    else:
                        self.x += 1
                else:
                    if y_dist > 0:
                        self.y -= 1
                    else:
                        self.y += 1
                print(f"{self.name} moved to {self.x},{self.y}")
            else:
                break


class Archer(Unit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.name = 'archer'
        self.hp = 10
        self.move_speed = 2
        self.attack_speed = 0.5
        self.attack_max_range = 20
        self.attack_min_range = 2
        self.attack_min_damage = 1
        self.attack_max_damage = 5
        self.accuracy = 80
        self.target = None

    def pick_target(self):
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    self.target = group.members[randint(0, len(group.members) - 1)]
                    return True
        return False

    def do_something(self):
        if not self.target:
            if self.pick_target():
                pass
            else:
                print(f"{self.name} - nothing to target. Combat is over.")
                return False
        # if not close enough, move to target
        # only move this turn, number of fields moved depends on the unit's speed
        for i in range(self.move_speed):
            straight_dist = round(math.sqrt((self.x-self.target.x)**2 + (self.y-self.target.y)**2))
            if straight_dist > self.attack_max_range:
                x_dist = self.x - self.target.x
                y_dist = self.y - self.target.y
                if abs(x_dist) > abs(y_dist):
                    if x_dist > 0:
                        self.x -= 1
                    else:
                        self.x += 1
                else:
                    if y_dist > 0:
                        self.y -= 1
                    else:
                        self.y += 1
                print(f"{self.name} moved to {self.x},{self.y}")
            else:
                break

def main():
    world = World()
    group_a = Group("Group A")
    group_b = Group("Group B")
    world.groups.append(group_a)
    world.groups.append(group_b)
    group_a.members.append(Fighter(mygroup = group_a, myworld = world))
    group_b.members.append(Archer(mygroup = group_b, myworld = world))
    world.place_units()

    world.turn = 1
    while True:
        for ma in group_a.members:
            result =  ma.do_something()
            if result == False:
                break
        for mb in group_b.members:
            result =  mb.do_something()
            if result == False:
                break

if __name__ == '__main__':
    raise SystemExit(main())
