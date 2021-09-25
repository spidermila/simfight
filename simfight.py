import sys


class World:
    def __init__(self):
        self.x = 50
        self.y = 30


class Group:
    def __init__(self):
        self.members = []


class Unit:
    def __init__(self):
        self.name = ""
        self.hp = 1


class Fighter(Unit):
    def __init__(self):
        self.name = "fighter"
        self.hp = 10
        self.move_speed = 2
        self.attack_speed = 4
        self.attack_max_range = 1
        self.attack_min_range = 1
        self.attack_min_damage = 2
        self.attack_max_damage = 10
        self.accuracy = 80


def Archer(Unit):
    def __init__(self):
        self.name = 'archer'
        self.hp = 10
        self.move_speed = 2
        self.attack_speed = 2
        self.attack_max_range = 20
        self.attack_min_range = 2
        self.attack_min_damage = 1
        self.attack_max_damage = 5
        self.accuracy = 80

def main():
    group_a = Group()
    group_b = Group()
    group_a.members.append(Fighter())
    group_b.members.append(Archer())

    while True:
        #fight
        for ma in group_a.members:
            pass

if __name__ == '__main__':
    sys.exit(main())
