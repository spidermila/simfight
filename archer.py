import math

from random import randint

from unit import Unit

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
            for i in range(self.move_speed):
                straight_dist = self.get_distance_to_target()
                x_dist = self.x - self.target.x
                y_dist = self.y - self.target.y
                if abs(x_dist) > abs(y_dist):
                    if x_dist > 0:
                        goto_x = self.x + 1
                        if self.myworld.square_is_valid(goto_x, self.y):
                            self.x = goto_x
                        else:
                            pass
                    else:
                        goto_x = self.x - 1
                        if self.myworld.square_is_valid(goto_x, self.y):
                            self.x = goto_x
                        else:
                            pass
                else:
                    if y_dist > 0:
                        goto_y = self.y + 1
                        if self.myworld.square_is_valid(self.x, goto_y):
                            self.y = goto_y
                        else:
                            pass
                        self.y = goto_y
                    else:
                        goto_y = self.y - 1
                        if self.myworld.square_is_valid(self.x, goto_y):
                            self.y = goto_y
                        else:
                            pass
                        self.y = goto_y
                if self.x > self.myworld.x or self.x < 1:
                    self.alive = False
                    print(f"{self.name} out of bounds")
                else:
                    print(f"{self.name} moved to {self.x},{self.y} - target {self.target.name} at {self.target.x},{self.target.y} - distance {straight_dist}")
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
                            goto_x = self.x - 1
                            if self.myworld.square_is_valid(goto_x, self.y):
                                self.x = goto_x
                            else:
                                pass
                        else:
                            goto_x = self.x + 1
                            if self.myworld.square_is_valid(goto_x, self.y):
                                self.x = goto_x
                            else:
                                pass
                    else:
                        if y_dist > 0:
                            goto_y = self.y - 1
                            if self.myworld.square_is_valid(self.x, goto_y):
                                self.y = goto_y
                            else:
                                pass
                        else:
                            goto_y = self.y + 1
                            if self.myworld.square_is_valid(self.x, goto_y):
                                self.y = goto_y
                            else:
                                pass
                    print(f"{self.name} moved to {self.x},{self.y} - target {self.target.name} at {self.target.x},{self.target.y} - distance {straight_dist}")
                else:
                    break
        return True
