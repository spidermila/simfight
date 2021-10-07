from typing import List

class Group:
    def __init__(self, name, map_letter = "X") -> None:
        self.name = name
        self.members: List = []
        self.map_letter = map_letter
