file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

max_weight = len(data)

def print_platform(current_positions, cycles):
    print(f"After {cycles} cycles:")
    for line in current_positions:
        print(line)
    print("")

def rotate_anticlock(current_positions):
    platform_cols = []
    for i in range(len(current_positions[0])-1, -1, -1):
        new_col = ""
        for line in current_positions:
            new_col += line[i]
        platform_cols.append(new_col)
    return platform_cols

def rotate_clock(current_positions):
    platform_cols = []
    for i in range(0, len(current_positions)):
        new_col = ""
        for line in current_positions:
            new_col = line[i] + new_col
        platform_cols.append(new_col)
    return platform_cols

def roll_rocks(current_positions):
    rolled_data = []
    for row in current_positions:
        rolled_row = "#".join(["".join(sorted(list(x), reverse=True)) for x in row.split("#")])
        rolled_data.append(rolled_row)
    return rolled_data

#print_platform(data, 0)

data = rotate_anticlock(data)
data = roll_rocks(data)

total_weight = 0
for col in data:
    rolled_col = "#".join(["".join(sorted(list(x), reverse=True)) for x in col.split("#")])
    for i in range(0, len(rolled_col)):
        if rolled_col[i] == "O":
            total_weight += (max_weight - i)
print("part 1:", total_weight)

# we've done a partial cycle so far, so finish off cycle 1
data = rotate_clock(data) # rotate for west
data = roll_rocks(data) # roll to west
data = rotate_clock(data) # rotate for south
data = roll_rocks(data) # roll to south
data = rotate_clock(data) # rotate for east
data = roll_rocks(data) # roll to east
data = rotate_clock(data) # rotate for north

# rotation for printing to match exercise notes
# data = rotate_clock(data)
# print_platform(data, 1)
# data = rotate_anticlock(data)

# cycle 2 begins (this is where normal cycles begin)

def run_cycle(current_positions):
    for i in range(0, 4):
        current_positions = rotate_clock(roll_rocks(current_positions))
    return current_positions

hashes = {}
found_identical_positions = False
final_cycle_number = 1000000000

cycle = 2
while cycle <= final_cycle_number:
    data = run_cycle(data)
    
    # optional printing steps i.e. for cycle 3
    # data = rotate_clock(data)
    # print_platform(data, cycle)
    # data = rotate_anticlock(data)
    
    # optional assert i.e. for cycle 3 on the test data
    # if cycle == 3:
    #     assert data == ['.#...#OOOO', '.O..#..O..', '....O#.O#.', '..#.OO..#.', '#.#.O.#.##', '.#....O.OO', '...#.....O', '...O.#...O', '.....O....', '........##']
    
    cycle_hash = hash(str(data))
    if not found_identical_positions and hashes.get(cycle_hash):
        #print("repetition found", hashes, cycle, cycle_hash)
        period = cycle - hashes[cycle_hash]
        extra_cycles = int((final_cycle_number - cycle) / period)
        #print("extra_cycles", extra_cycles)
        higher_cycle_number_matching_current = cycle + (extra_cycles * period)
        #print("higher_cycle_number_matching_current", higher_cycle_number_matching_current)
        cycle = higher_cycle_number_matching_current
        found_identical_positions = True
    else:
        hashes[cycle_hash] = cycle
    cycle += 1

total_weight = 0
for col in data:
    for i in range(0, len(col)):
        if col[i] == "O":
            total_weight += (max_weight - i)
print("part 2:", total_weight)

"""
Calculation for test data with period length (7) giving the repeated position
1
2 
3 10 ... 94  ... 999999997
4 11 ... 95  ... 999999998
5 12 ... 96  ... 999999999
6 13 ... 97  ... 1000000000
7 14 ... 98  ... 
8 15 ... 99  ... 
9 16 ... 100 ... 
"""