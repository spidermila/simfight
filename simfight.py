import argparse

from archer import Archer
from fighter import Fighter
from group import Group
from world import World


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', action='store_true', help='show map')
    parser.add_argument('-s', action='store_true', help='show turn summary')
    parser.add_argument('-l', action='store_true', help='show turn log')
    args = parser.parse_args()
    show_map = args.m
    show_summary = args.s
    show_log = args.l

    world = World()
    group_a = Group('Group A elite fighters', map_character='A')
    group_b = Group('Group B archers', map_character='B')
    group_c = Group('Group C fighters', map_character='C')
    group_d = Group('Group D archers', map_character='D')
    world.groups.append(group_a)
    world.groups.append(group_b)
    world.groups.append(group_c)
    world.groups.append(group_d)
    # adding a comment just to test this
    # nothing special
    for i in range(70):
        group_a.members.append(
            Fighter(
                name='elite fighterA' + str(i + 1),
                accuracy=95,
                hp=40,
                attack_min_damage=5,
                attack_max_damage=20,
                mygroup=group_a,
                myworld=world,
            ),
        )
    for i in range(90):
        group_b.members.append(
            Archer(
                name='archerB' + str(i + 1),
                mygroup=group_b,
                myworld=world,
            ),
        )
    for i in range(100):
        group_c.members.append(
            Fighter(
                name='fighterC' + str(i + 1),
                mygroup=group_c,
                myworld=world,
            ),
        )
    for i in range(150):
        group_d.members.append(
            Archer(
                name='archerD' + str(i + 1),
                mygroup=group_d,
                myworld=world,
            ),
        )
    world.place_units()

    world.cls()
    world.print_start_summary()
    print('Press Enter to continue or q to quit')
    a = input()
    if a == 'q':
        return
    world.cls()

    world.turn = 1
    fight = True
    while fight and world.turn < 100:
        fight = False
        print(f'===================== Turn {world.turn} =====================')
#        world.generate_intermediate_summary()
        for group in world.groups:
            for m in group.members:
                if m.alive:
                    result = m.do_something()
                    if result is True:
                        fight = True

        world.generate_intermediate_summary()
        if show_log and show_map and show_summary:
            world.print_everything()
        elif show_map and show_summary:
            world.print_intermediate_summary_w_map()
        elif show_map and show_log:
            pass
        elif show_map:
            world.print_map()
        else:
            world.print_everything()
        world.turn_log = []  # delete the log after printing
        world.turn += 1
        print('Press Enter to continue or q to quit')
        a = input()
        if a == 'q':
            return
        world.cls()
    world.print_map()


if __name__ == '__main__':
    raise SystemExit(main())
