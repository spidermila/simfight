import math
import os
import sys
from typing import List


class World:
    def __init__(self) -> None:
        self.x = 50
        self.y = 30
        self.groups: List = []
        self.map: List = []
        self.summary: List = []
        self.turn_log: List = []
        self.short_summary: List = []
        self.map_corpse_character = '.'
        self.map_nothing_character = ' '

        if sys.platform.find('linux') != -1:
            self.cls_command = 'clear'
        elif sys.platform.find('win') != -1:
            self.cls_command = 'cls'
        elif sys.platform.find('darwin') != -1:
            self.cls_command = 'clear'
        else:
            print('Unknown OS. cls will not work!')
            self.cls_command = False  # type: ignore

    def cls(self) -> None:
        if self.cls_command:
            os.system(self.cls_command)

    def longest_list(self, *args) -> list:
        max = 0
        for ar in args:
            if max < len(ar):
                max = len(ar)
                winner = ar
        return winner

    def generate_map(self) -> None:
        self.map = []
        for row in range(self.y + 2):
            r = f'{str(row):>{2}}'
            if row == 0 or row == self.y + 1:
                r = r + '=' * (self.x + 2)
            else:
                for col in range(self.x + 2):
                    found = False
                    if col == 0 or col == self.x + 1:
                        r = r + '|'
                        found = True
                    else:
                        for group in self.groups:
                            for member in group.members:
                                if (
                                    member.x == col and
                                    member.y == row and
                                    not found
                                ):
                                    if member.alive:
                                        r = r + group.map_character
                                    else:
                                        r = r + self.map_corpse_character
                                    found = True
                    if found is False:
                        r = r + self.map_nothing_character
            self.map.append(r)

    def generate_short_summary(self):
        self.short_summary = []
        max_name = 0
        max_alive = 0
        max_kills = 0
        max_dead = 0
        for group in self.groups:
            if len(group.name) > max_name:
                max_name = len(group.name)
            if len(str(group.get_alive_count())) > max_alive:
                max_alive = len(str(group.get_alive_count()))
            if len(str(group.kills)) > max_kills:
                max_kills = len(str(group.kills))
            if len(str(group.get_dead_count())) > max_dead:
                max_dead = len(str(group.get_dead_count()))

        for group in self.groups:
            self.short_summary.append(
                f'{group.name:<{max_name}} ' +
                f'| {group.get_dead_count():<{max_dead}} dead ' +
                f'| {group.get_alive_count():<{max_alive}} alive ' +
                f'| {group.kills:<{max_kills}} kills',
            )

    def print_map(self) -> None:
        for o in self.map:
            print(o)
        for s in self.short_summary:
            print(s)

    def print_start_summary(self) -> None:
        max_name = 0
        for group in self.groups:
            for member in group.members:
                if len(member.name) > max_name:
                    max_name = len(member.name)
        print('=' * 50)
        print(' ' * 10 + 'Initial Pre-combat Summary')
        print('=' * 50)
        for group in self.groups:
            print(f'Group: {group.name}:')
            for member in group.members:
                print(
                    f'{member.name :<{max_name}} - {member.hp} HP' +
                    f', {member.attack_min_range}-' +
                    f'{member.attack_max_range} range' +
                    f', {member.attack_min_damage}-' +
                    f'{member.attack_max_damage} damage',
                )
            print('-' * 50)

    def generate_intermediate_summary(self) -> None:
        self.generate_map()
        self.generate_short_summary()
        # self.print_map()
        max_name = 0
        self.summary = []
        for group in self.groups:
            c = 0
            max_loc = 0
            for member in group.members:
                if len(member.name) > max_name:
                    max_name = len(member.name)
                if len(f'{member.x}/{member.y}') > max_loc:
                    max_loc = len(f'{member.x}/{member.y}')
                if member.alive:
                    c += 1
            self.summary.append(
                f'--------------- {group.name} -- {c} alive ---------------',
            )
            for member in group.members:
                if member.alive:
                    if member.target and member.target.alive:
                        tgt = member.target.name
                    else:
                        tgt = 'none'
                    loc = f'{member.x}/{member.y}'
                    self.summary.append(
                        f'{member.name :<{max_name}} ({loc :<{max_loc}}) ' +
                        f'- {member.hp} HP - target: {tgt}',
                    )
                    c += 1
        self.summary.append('-' * 50)

    def print_intermediate_summary(self) -> None:
        for s in self.summary:
            print(s)

    def print_intermediate_summary_w_map(self) -> None:
        if len(self.map) > len(self.summary):
            for i, m in enumerate(self.map):
                if i < len(self.summary):
                    print(f'{self.map[i]} {self.summary[i]}')
                else:
                    print(f'{m}')
        else:
            for i, s in enumerate(self.summary):
                if i < len(self.map):
                    print(f'{self.map[i]} {s}')
                else:
                    print(' ' * (self.x + 2) + s)

    def print_everything(self) -> None:
        max_msg_len = 0
        for msg in self.turn_log:
            if max_msg_len < len(msg):
                max_msg_len = len(msg)
        max_sum_len = 0
        for sum in self.summary:
            if max_sum_len < len(sum):
                max_sum_len = len(sum)
        max_map_len = 0
        for m in self.map:
            if max_map_len < len(m):
                max_map_len = len(m)

        winner = self.longest_list(self.map, self.summary, self.turn_log)
        tmp_map = []
        for i in range(len(winner)):
            if i >= len(self.turn_log):
                self.turn_log.append(f"{str(''):<{max_msg_len}}")
            if i >= len(self.summary):
                self.summary.append(f"{str(''):<{max_sum_len}}")
            if i < len(winner) - len(self.map):
                tmp_map.append(f"{str(''):<{self.x+2}}")
            else:
                tmp_map.append(self.map[i - (len(winner) - len(self.map))])
                # self.map.append(f"{str(''):<{self.x+2}}")
        for i, m in enumerate(winner):
            print(
                f'{tmp_map[i]:<{max_map_len}} ' +
                f'{self.summary[i]:<{max_sum_len}} ' +
                f'{self.turn_log[i]:<{max_msg_len}}',
            )

    def place_units(self) -> None:
        number_of_groups = len(self.groups)
        rows = math.ceil(number_of_groups / 2)
        gid = -1
        for row in range(rows):
            # populate left side of the map first
            gid += 1
            group = self.groups[gid]
            left_col_x_min = 1
            left_col_x_max = int(self.x / 2)
            y_min = int((self.y / rows) * row + 1)
            y_max = int((self.y / rows) * (row + 1))
            x_next = left_col_x_min
            y_next = y_min
            for unit in group.members:
                if y_next > y_max:
                    x_next += 1
                    y_next = y_min
                    if x_next > left_col_x_max:
                        print(
                            'Too many units to fit on the map! ' +
                            f'{row=}, {group.name=}',
                        )
                unit.x = x_next
                unit.y = y_next
                y_next += 1

            # populate right side of the map next
            gid += 1
            right_col_x_min = int(self.x / 2) + 1
            right_col_x_max = self.x
            group = self.groups[gid]
            x_next = right_col_x_min
            y_next = y_min
            for unit in group.members:
                if y_next > y_max:
                    x_next += 1
                    y_next = y_min
                    if x_next > right_col_x_max:
                        print(
                            'Too many units to fit on the map! ' +
                            f'{row=}, {group.name=}',
                        )
                unit.x = x_next
                unit.y = y_next
                y_next += 1

    def square_is_valid(self, goto_x: int, goto_y: int) -> bool:
        for group in self.groups:
            for member in group.members:
                if goto_x == member.x and goto_y == member.y:
                    if member.alive:
                        return False
        if goto_x <= 0 or goto_x > self.x or goto_y <= 0 or goto_y > self.y:
            return False
        return True
