from random import randint

from typing import Optional
from typing import List
from unit import Unit

class Fighter(Unit):
    def __init__(self, *args, name = "fighter", **kwargs) -> None:
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
        self.target: Optional[Unit] = None

    def pick_random_target(self) -> bool:
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    attempted_targets = []
                    candidate_targets = group.members[:]
                    while len(candidate_targets) > 0:
                        attempt = candidate_targets[randint(0, len(candidate_targets) - 1)]
                        if attempt not in attempted_targets and attempt.alive == True:
                            self.target = attempt
                            if isinstance(self.target, Unit):
                                self.myworld.turn_log.append(f"{self.name} targeted {self.target.name}")
                                return True
                        else:
                            attempted_targets.append(attempt)
                            candidate_targets.pop(candidate_targets.index(attempt))
        return False

    def pick_closest_target(self) -> bool:
        maximum_attackers_on_one_target = 6
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    closest_target = None
                    dst_to_closest = 99999999999
                    for tgt in group.members:
                        if tgt.alive:
                            attackers = 0
                            if dst_to_closest > self.get_distance_to_target() - 1:
                                for member in self.mygroup.members:
                                        if member.target == tgt:
                                            attackers += 1
                                if attackers < maximum_attackers_on_one_target:
                                    dst_to_closest = self.get_distance_to_target() - 1
                                    closest_target = tgt
                                    self.target = closest_target
                                    return True
        return False

    def pick_lowestHP_target(self) -> bool:
        maximum_attackers_on_one_target = 6
        for group in self.myworld.groups:
            if group != self.mygroup:
                if len(group.members) > 0:
                    lowestHP_target = None
                    lowestHP = 99999999999
                    for tgt in group.members:
                        if tgt.alive:
                            attackers = 0
                            if isinstance(self.target, Unit):
                                if lowestHP > self.target.hp:
                                    for member in self.mygroup.members:
                                        if member.target == tgt:
                                            attackers += 1
                                    if attackers < maximum_attackers_on_one_target:
                                        lowestHP_target = tgt
                                        lowestHP = self.target.hp
                                        self.target = lowestHP_target
                                        return True
        return False

    def attack(self) -> None:
        if isinstance(self.target, Unit):
            if self.accuracy >= randint(1, 100):
                # hit
                dmg = randint(self.attack_min_damage, self.attack_max_damage)
                if self.target.hp - dmg <= 0:
                    self.myworld.turn_log.append(f"{self.name} attacking {self.target.name} ({self.target.hp} HP) - Hit for {dmg} - Target killed")
                    self.target.hp -= dmg
                    self.target.alive = False
                    self.target = None
                else:
                    self.myworld.turn_log.append(f"{self.name} attacking {self.target.name} ({self.target.hp} HP) - Hit for {dmg}")
                    self.target.hp -= dmg
            else:
                self.myworld.turn_log.append(f"{self.name} attacking {self.target.name} ({self.target.hp} HP) - Missed")

    def move_to_target(self) -> None:
        tries = 3
        tried = 0
        if isinstance(self.target, Unit):
            can_move = False
            while not can_move:
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
                    if tried < tries:
                        #print('trying 1')
                        tried += 1
                        #self.myworld.turn_log.append(f"{self.name} nowhere to move")
                        self.pick_lowestHP_target()
                    elif tried < tries * 2:
                        #print('trying 2')
                        self.pick_random_target()
                        tried += 1
                    else:
                        #print('trying x')
                        best_moves = [[0,0]]
                        can_move = True
                else:
                    can_move = True
            
            best_move = best_moves[randint(0, len(best_moves) - 1)]
            self.x += best_move[0]
            self.y += best_move[1]
            straight_dist = self.get_distance_to_target()
            self.myworld.turn_log.append(f"{self.name} moved {best_move} to ({self.x},{self.y}) - target {self.target.name} ({self.target.x},{self.target.y}) - new distance {straight_dist}")

    def do_something(self) -> bool:
        if not self.target or self.target.alive == False:
            if self.pick_closest_target():
                pass
            else:
                self.myworld.turn_log.append(f"{self.name} - nothing to target.")
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
            while self.attack_credit >= 1.0:
                self.attack_credit -= 1.0
                self.attack()
        return True
