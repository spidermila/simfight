from typing import List


class Group:
    def __init__(self, name, map_character='X') -> None:
        self.name = name
        self.members: List = []
        self.map_character = map_character
        self.kills = 0

    def get_alive_count(self) -> int:
        alive = 0
        for member in self.members:
            if member.alive:
                alive += 1
        return alive

    def get_total_count(self) -> int:
        return len(self.members)

    def get_dead_count(self) -> int:
        dead = 0
        for member in self.members:
            if member.alive is False:
                dead += 1
        return dead
