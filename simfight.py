import math
from random import randint
from typing_extensions import runtime

class World:
    def __init__(self):
        self.x = 50
        self.y = 30
        self.groups = []
    
    def print_start_summary(self):
        print("=" * 50)
        print(" " * 20 + "Summary")
        print("=" * 50)
        for group in self.groups:
            print(f"Group: {group.name}:")
            for member in group.members:
                print(f"{member.name} - {member.hp} HP, {member.attack_min_range}-{member.attack_max_range} range, {member.attack_min_damage}-{member.attack_max_damage} damage")
            print("-" * 50)

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
        self.alive = True
        self.name = ""
        self.hp = 1
        self.x = 0
        self.y = 0
        self.attack_credit = 0

    def get_distance_to_target(self):
        return round(math.sqrt((self.x-self.target.x)**2 + (self.y-self.target.y)**2)) - 1

class Fighter(Unit):
    def __init__(self, *args, name = "fighter", **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.hp = 20
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
                    attempted_targets = []
                    candidate_targets = group.members[:]
                    while len(candidate_targets) > 0:
                        attempt = candidate_targets[randint(0, len(candidate_targets) - 1)]
                        if attempt not in attempted_targets and attempt.alive == True:
                            self.target = attempt
                            print(f"{self.name} targeted {self.target.name}")
                            return True
                        else:
                            attempted_targets.append(attempt)
                            candidate_targets.pop(candidate_targets.index(attempt))
        return False

    def attack(self):
        if self.accuracy >= randint(1, 100):
            # hit
            dmg = randint(self.attack_min_damage, self.attack_max_damage)
            if self.target.hp - dmg <= 0:
                print(f"{self.name} attacking {self.target.name} ({self.target.hp} HP) - Hit for {dmg} - Target killed")
                self.target.hp -= dmg
                self.target.alive = False
                self.target = None
            else:
                print(f"{self.name} attacking {self.target.name} ({self.target.hp} HP) - Hit for {dmg}")
                self.target.hp -= dmg
        else:
            print(f"{self.name} attacking {self.target.name} ({self.target.hp} HP) - Missed")

    def do_something(self):
        if not self.target or self.target.alive == False:
            if self.pick_target():
                pass
            else:
                print(f"{self.name} - nothing to target. Combat is over.")
                return False
        straight_dist = self.get_distance_to_target()
        if straight_dist <= self.attack_max_range and straight_dist >= self.attack_min_range:
            self.attack_credit += self.attack_speed
            while self.attack_credit >= 1:
                self.attack_credit -= 1
                self.attack()
        elif straight_dist < self.attack_min_range:
            # move away from target
            pass
        else:
        # if not close enough, move to target
        # only move this turn, number of fields moved depends on the unit's speed
            for i in range(self.move_speed):
                straight_dist = self.get_distance_to_target()
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
                    print(f"{self.name} moved to {self.x},{self.y} - target {self.target.name} at {self.target.x},{self.target.y} - distance {straight_dist}")
                else:
                    break
        return True


class Archer(Unit):
    def __init__(self, *args, name = "archer", **kwargs):
        super().__init__(*args, **kwargs)
        self.name = name
        self.hp = 10
        self.move_speed = 2
        self.attack_speed = 0.5
        self.attack_max_range = 20
        self.attack_min_range = 2
        self.attack_min_damage = 1
        self.attack_max_damage = 5
        self.accuracy = 70
        self.target = None

    def pick_target(self):
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    attempted_targets = []
                    candidate_targets = group.members[:]
                    while len(candidate_targets) > 0:
                        attempt = candidate_targets[randint(0, len(candidate_targets) - 1)]
                        if attempt not in attempted_targets and attempt.alive == True:
                            self.target = attempt
                            print(f"{self.name} targeted {self.target.name}")
                            return True
                        else:
                            attempted_targets.append(attempt)
                            candidate_targets.pop(candidate_targets.index(attempt))
        return False

    def attack(self):
        if self.accuracy >= randint(1, 100):
            # hit
            dmg = randint(self.attack_min_damage, self.attack_max_damage)
            if self.target.hp - dmg <= 0:
                print(f"{self.name} shooting {self.target.name} ({self.target.hp} HP) - Hit for {dmg} - Target killed")
                self.target.hp -= dmg
                self.target.alive = False
                self.target = None
            else:
                print(f"{self.name} shooting {self.target.name} ({self.target.hp} HP) - Hit for {dmg}")
                self.target.hp -= dmg
        else:
            print(f"{self.name} shooting {self.target.name} ({self.target.hp} HP) - Missed")


    def do_something(self):
        if not self.target or self.target.alive == False:
            if self.pick_target():
                pass
            else:
                print(f"{self.name} - nothing to target.")
                return False
        straight_dist = self.get_distance_to_target()
        if straight_dist <= self.attack_max_range and straight_dist >= self.attack_min_range:
            self.attack_credit += self.attack_speed
            while self.attack_credit >= 1:
                self.attack_credit -= 1
                self.attack()
        elif straight_dist < self.attack_min_range:
            # move away from target
            pass
        else:
            # if not close enough, move to target
            # only move this turn, number of fields moved depends on the unit's speed
            for i in range(self.move_speed):
                straight_dist = self.get_distance_to_target()
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
                    print(f"{self.name} moved to {self.x},{self.y} - target {self.target.name} at {self.target.x},{self.target.y} - distance {straight_dist}")
                else:
                    break
        return True

def main():
    world = World()
    group_a = Group("Group A")
    group_b = Group("Group B")
    world.groups.append(group_a)
    world.groups.append(group_b)
    for i in range(2):
        group_a.members.append(Fighter(name="fighter" + str(i), mygroup = group_a, myworld = world))
    for i in range(2):
        group_b.members.append(Archer(name="archer" + str(i), mygroup = group_b, myworld = world))
    world.place_units()

    world.print_start_summary()

    world.turn = 1
    fight = True
    while fight and world.turn < 25:
        fight = False
        print(f"===================== Turn {world.turn} =====================")
        for ma in group_a.members:
            result =  ma.do_something()
            if result == True:
                fight = True
        for mb in group_b.members:
            result =  mb.do_something()
            if result == True:
                fight = True
            world.turn += 1
    print("Fight ended.")

if __name__ == '__main__':
    raise SystemExit(main())
