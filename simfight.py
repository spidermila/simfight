from random import randint
from typing_extensions import runtime

from fighter import Fighter
from group import Group
from archer import Archer
from world import World

    

def main():
    world = World()
    group_a = Group("Group A", map_letter="A")
    group_b = Group("Group B", map_letter="B")
    world.groups.append(group_a)
    world.groups.append(group_b)
    for i in range(5):
        group_a.members.append(Fighter(name="fighter" + str(i + 1), mygroup = group_a, myworld = world))
    for i in range(10):
        group_b.members.append(Archer(name="archer" + str(i + 1), mygroup = group_b, myworld = world))
    world.place_units()

    world.cls()
    world.print_start_summary()
    print("Press Enter to continue or q to quit")
    a = input()
    if a == "q":
        return
    world.cls()

    world.turn = 1
    fight = True
    while fight and world.turn < 100:
        fight = False
        print(f"===================== Turn {world.turn} =====================")
        world.generate_intermediate_summary()
        for ma in group_a.members:
            if ma.alive:
                result =  ma.do_something()
                if result == True:
                    fight = True
        for mb in group_b.members:
            if mb.alive:
                result =  mb.do_something()
                if result == True:
                    fight = True
        world.print_everything()
        world.turn_log = [] # delete the log after printing
        world.turn += 1
        print("Press Enter to continue or q to quit")
        a = input()
        if a == "q":
            return
        world.cls()
    world.print_end_summary()

if __name__ == '__main__':
    raise SystemExit(main())
