from random import randint
from typing import List
from typing import Optional

from unit import Unit

class Archer(Unit):
    def __init__(self, *args, name = 'archer', **kwargs) -> None:
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
        self.target: Optional[Unit] = None

    def pick_random_target(self) -> bool:
        candidates = []
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    for member in group.members:
                        candidates.append(member)
        attempted_targets = []
        candidate_targets = candidates[:]
        while len(candidate_targets) > 0:
            attempt = candidate_targets[randint(0, len(candidate_targets) - 1)]
            if attempt not in attempted_targets and attempt.alive == True:
                self.target = attempt
                if isinstance(self.target, Unit):
                    self.myworld.turn_log.append(f'{self.name} targeted {self.target.name}')
                    return True
            else:
                attempted_targets.append(attempt)
                candidate_targets.pop(candidate_targets.index(attempt))
        return False

    def move_to_target(self) -> None:
        if isinstance(self.target, Unit):
            best_moves: List = []
            best_move: List = [0, 0]
            straight_dist = self.get_distance_to_target() - 1
            best_move_dst = straight_dist
            for loc in self.surrounding_fields:
                dst = self.get_distance_to_target_from_xy(self.x + loc[0], self.y + loc[1]) - 1
                if best_move_dst == dst and self.myworld.square_is_valid(self.x + loc[0], self.y + loc[1]):
                    best_moves.append(loc[:])
                elif best_move_dst > dst and self.myworld.square_is_valid(self.x + loc[0], self.y + loc[1]):
                    best_move_dst = dst
                    best_moves = [loc[:]]
                #self.myworld.turn_log.append(f"{self.name}({self.x},{self.y}) - {straight_dist=} - ({self.target.x},{self.target.y}) - move {loc} - {dst=}, {best_moves=}")
            if len(best_moves) == 0:
                # TODO pick a different target
                self.myworld.turn_log.append(f'{self.name} nowhere to move')
            else:
                best_move = best_moves[randint(0, len(best_moves) - 1)]
                self.x += best_move[0]
                self.y += best_move[1]
                straight_dist = self.get_distance_to_target()
                self.myworld.turn_log.append(f'{self.name} moved {best_move} to ({self.x},{self.y}) - target {self.target.name} ({self.target.x},{self.target.y}) - new distance {straight_dist}')

    def attack(self) -> None:
        if isinstance(self.target, Unit):
            if self.accuracy >= randint(1, 100):
                # hit
                dmg = randint(self.attack_min_damage, self.attack_max_damage)
                if self.target.hp - dmg <= 0:
                    self.myworld.turn_log.append(f'{self.name} shooting {self.target.name} ({self.target.hp} HP) - Hit for {dmg} - Target killed')
                    self.target.hp -= dmg
                    self.target.alive = False
                    self.target = None
                    self.mygroup.kills += 1
                else:
                    self.myworld.turn_log.append(f'{self.name} shooting {self.target.name} ({self.target.hp} HP) - Hit for {dmg}')
                    self.target.hp -= dmg
            else:
                self.myworld.turn_log.append(f'{self.name} shooting {self.target.name} ({self.target.hp} HP) - Missed')


    def do_something(self) -> bool:
        if not self.target or self.target.alive == False:
            if self.pick_random_target():
                pass
            else:
                self.myworld.turn_log.append(f'{self.name} - nothing to target.')
                return False
        straight_dist = self.get_distance_to_target()
        if straight_dist <= self.attack_max_range and straight_dist >= self.attack_min_range:
            self.attack_credit += self.attack_speed
            while self.attack_credit >= 1.0:
                self.attack_credit -= 1.0
                self.attack()
        elif straight_dist < self.attack_min_range:
            # move away from target
            for i in range(self.move_speed):
                straight_dist = self.get_distance_to_target()
                if isinstance(self.target, Unit):
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
                        self.myworld.turn_log.append(f'{self.name} out of bounds')
                    else:
                        self.myworld.turn_log.append(f'{self.name} moved to {self.x},{self.y} - target {self.target.name} at {self.target.x},{self.target.y} - distance {straight_dist}')
        else:
            # if not close enough, move to target
            # only move this turn, number of fields moved depends on the unit's speed
            for i in range(self.move_speed):
                straight_dist = self.get_distance_to_target()
                if straight_dist > self.attack_max_range:
                    self.move_to_target()
                else:
                    break
        return True
