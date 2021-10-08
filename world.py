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
        self.map_corpse_character = ':'
        self.map_nothing_character = '.'

        if sys.platform.find('linux') != -1:
            self.cls_command = 'clear'
        elif sys.platform.find('win') != -1:
            self.cls_command = 'cls'
        elif sys.platform.find('darwin') != -1:
            self.cls_command = 'clear'
        else:
            print('Unknown OS. cls will not work!')
            self.cls_command = False # type: ignore

    def cls(self) -> None:
        if self.cls_command: os.system(self.cls_command)

    def longest_list(self, *args) -> list:
        max = 0
        for l in args:
            if max < len(l):
                max = len(l)
                winner = l
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
                                if member.x == col and member.y == row:
                                    if member.alive:
                                        r = r + group.map_letter
                                    else:
                                        r = r + self.map_corpse_character
                                    found = True
                        if found == False:
                            #TODO fix wrong formatting - x is extending the row
                            r = r + self.map_nothing_character
            self.map.append(r)

    def print_map(self) -> None:
        for o in self.map:
            print(o)

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
                print(f'{member.name :<{max_name}} - {member.hp} HP, {member.attack_min_range}-{member.attack_max_range} range, {member.attack_min_damage}-{member.attack_max_damage} damage')
            print('-' * 50)

    def print_end_summary(self) -> None:
        summary = []
        loser = ''
        len_grp = 0
        len_alive = 0
        len_total = 0
        for group in self.groups:
            total = 0
            alive = 0
            for member in group.members:
                if member.alive:
                    alive += 1
                total += 1
            summary.append(
                {
                    'group':group.name,
                    'total':total,
                    'alive':alive,
                },
            )
            if alive == 0:
                loser = group.name
            if len_grp < len(group.name):
                len_grp = len(group.name)
            if len_alive < len(str(alive)):
                len_alive = len(str(alive))
            if len_total < len(str(total)):
                len_total = len(str(total))

        if len_grp < len('Group Name'):
            len_grp = len('Group Name')
        if len_alive < len('Alive Units'):
            len_alive = len('Alive Units')
        if len_total < len('Total Units'):
            len_total = len('Total Units')

        print(f'{loser} lost')
        print()
        print(f"{'Group Name':<{len_grp}} | {'Total Units':<{len_total}} | {'Alive Units':<{len_alive}}")
        for i in summary:
            print(f"{i['group']:<{len_grp}} | {i['total']:<{len_total}} | {i['alive']:<{len_alive}}")

    def generate_intermediate_summary(self) -> None:
        self.generate_map()
        #self.print_map()
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
            self.summary.append(f'--------------- {group.name} -- {c} alive ---------------')
            for member in group.members:
                if member.alive:
                    if member.target and member.target.alive:
                        tgt = member.target.name
                    else:
                        tgt = 'none'
                    loc = f'{member.x}/{member.y}'
                    self.summary.append(f'{member.name :<{max_name}} ({loc :<{max_loc}}) - {member.hp} HP - target: {tgt}')
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
                #self.map.append(f"{str(''):<{self.x+2}}")
        for i, m in enumerate(winner):
            print(f'{tmp_map[i]:<{max_map_len}} {self.summary[i]:<{max_sum_len}} {self.turn_log[i]:<{max_msg_len}}')


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
                        print(f'Too many units to fit on the map! {row=}, {group.name=}')
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
                        print(f'Too many units to fit on the map! {row=}, {group.name=}')
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
