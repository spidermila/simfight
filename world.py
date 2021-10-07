class World:
    def __init__(self):
        self.x = 50
        self.y = 30
        self.groups = []
    
    def print_start_summary(self):
        max_name = 0
        for group in self.groups:
            for member in group.members:
                if len(member.name) > max_name:
                    max_name = len(member.name)
        print("=" * 50)
        print(" " * 20 + "Summary")
        print("=" * 50)
        for group in self.groups:
            print(f"Group: {group.name}:")
            for member in group.members:
                print(f"{member.name :<{max_name}} - {member.hp} HP, {member.attack_min_range}-{member.attack_max_range} range, {member.attack_min_damage}-{member.attack_max_damage} damage")
            print("-" * 50)

    def print_intermediate_summary(self):
        max_name = 0
        for group in self.groups:
            c = 0
            max_loc = 0
            for member in group.members:
                if len(member.name) > max_name:
                    max_name = len(member.name)
                if len(f"{member.x}/{member.y}") > max_loc:
                    max_loc = len(f"{member.x}/{member.y}")
                if member.alive:
                    c += 1
            print(f"--------------- {group.name} -- {c} alive ---------------")
            for member in group.members:
                if member.alive:
                    if member.target and member.target.alive:
                        tgt = member.target.name
                    else:
                        tgt = "none"
                    loc = f"{member.x}/{member.y}"
                    print(f"{member.name :<{max_name}} ({loc :<{max_loc}}) - {member.hp} HP - target: {tgt}")
                    c += 1
        print("-" * 50)

    def place_units(self):
        number_of_groups = len(self.groups)
        rows = int(number_of_groups / 2)
        gid = 0
        for row in range(rows):
            # populate left side of the map first
            group = self.groups[gid]
            left_col_x_min = 1
            left_col_x_max = int(self.x / 2)
            y_min = int((self.y / rows) * row + 1)
            y_max = int((self.y / rows) * (row + 1))
            x_next = left_col_x_min
            y_next = y_min
            for unit in group.members:
                if x_next > left_col_x_max:
                    y_next += 1
                    x_next = left_col_x_min
                    if y_next > y_max:
                        print(f"Too many units to fit on the map! {row=}, {group.name=}")
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
                if x_next > right_col_x_max:
                    y_next += 1
                    x_next = right_col_x_min
                    if y_next > y_max:
                        print(f"Too many units to fit on the map! {row=}, {group.name=}")
                unit.x = x_next
                unit.y = y_next
                y_next += 1

    def square_is_valid(self, goto_x, goto_y):
        for group in self.groups:
            for member in group.members:
                if goto_x == member.x and goto_y == member.y:
                    return False
        if goto_x < 0 or goto_x > self.x or goto_y < 0 or goto_y > self.y:
            return False
        return True
