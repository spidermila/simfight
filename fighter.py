from random import randint

from unit import Unit

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

    def move_to_target(self):
        best_moves = []
        best_move = [0, 0]
        straight_dist = self.get_distance_to_target() - 1
        best_move_dst = straight_dist
        for loc in self.surrounding_fields:
            dst = self.get_distance_to_target_from_xy(self.x + loc[0], self.y + loc[1]) - 1
            if best_move_dst == dst and self.myworld.square_is_valid(self.x + loc[0], self.y + loc[1]):
                best_moves.append(loc[:])
            elif best_move_dst > dst and self.myworld.square_is_valid(self.x + loc[0], self.y + loc[1]):
                best_move_dst = dst
                best_moves = [loc[:]]
            #print(f"{self.name}({self.x},{self.y}) - {straight_dist=} - ({self.target.x},{self.target.y}) - move {loc} - {dst=}, {best_moves=}")
        if len(best_moves) == 0:
            print(f"{self.name} nowhere to move")
        else:
            best_move = best_moves[randint(0, len(best_moves) - 1)]
            self.x += best_move[0]
            self.y += best_move[1]
            straight_dist = self.get_distance_to_target()
            print(f"{self.name} moved {best_move} to ({self.x},{self.y}) - target {self.target.name} ({self.target.x},{self.target.y}) - new distance {straight_dist}")

    def do_something(self):
        if not self.target or self.target.alive == False:
            if self.pick_target():
                pass
            else:
                print(f"{self.name} - nothing to target.")
                return False

        straight_dist = self.get_distance_to_target()
        if straight_dist > self.attack_max_range:
        # if not close enough, move to target
        # only move this turn, number of fields moved depends on the unit's speed
            for i in range(self.move_speed):
                straight_dist = self.get_distance_to_target()
                if straight_dist > self.attack_max_range:
                    self.move_to_target()
                else:
                    break
        elif straight_dist < self.attack_min_range:
            # move away from target
            pass

        straight_dist = self.get_distance_to_target()
        if straight_dist <= self.attack_max_range and straight_dist >= self.attack_min_range:
            self.attack_credit += self.attack_speed
            while self.attack_credit >= 1:
                self.attack_credit -= 1
                self.attack()
        return True
