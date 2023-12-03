import string
from collections import defaultdict

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
#file = open("input_test2.txt", "r") # specific case initially failing for part 1
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

# how to determine what each of the characters really is
def set_initial_adj(c):
    if c in string.digits:
        return "false"
    elif c == ".":
        return "dot"
    else:
        return "symbol"

def update_adjacency(r, c, star_coords):
    if coords_and_data[(r, c)]["adj"] == "false":
        coords_and_data[(r, c)]["adj"] = "true"
        coords_and_data[(r, c)]["star_coords"] = star_coords
        return 1
    else:
        return 0

coords_and_data = {} # keys are coords, values are characters plus proximity
max_rows = len(data)
max_cols = len(data[0])

# build our grid of coordinates, values and their initial adjacency values
for row in range(0, max_rows):
    for col in range(0, max_cols):
        coords_and_data[(row, col)] = {"val": data[row][col], "adj": set_initial_adj(data[row][col])}

# print(coords_and_data)
# print(coords_and_data[(2,58)])

# an initial round of determining any numbers with proximity to a symbol
for row in range(0, max_rows):
    for col in range(0, max_cols):
        changes = 0
        if coords_and_data[(row, col)]["adj"] == "symbol":
            star_coords = False
            if coords_and_data[(row, col)]["val"] == "*":
                star_coords = (row, col)
            changes += update_adjacency(row, col+1, star_coords)   # right
            changes += update_adjacency(row+1, col+1, star_coords) # bottom-right
            changes += update_adjacency(row+1, col, star_coords)   # bottom
            changes += update_adjacency(row+1, col-1, star_coords) # bottom-left
            changes += update_adjacency(row, col-1, star_coords)   # left
            changes += update_adjacency(row-1, col-1, star_coords) # top-left
            changes += update_adjacency(row-1, col, star_coords)   # top
            changes += update_adjacency(row-1, col+1, star_coords) # top-right
        if changes == 2 and coords_and_data[(row, col)]["val"] == "*":
            coords_and_data[(row, col)]["adj"] = "symbol_star"

# print(coords_and_data)
# print(coords_and_data[(2,58)])

# while we are still finding other numbers adjacent to numbers which are
# adjacent to ... a symbol, keep going looking for more of them
changes = 100000000
while changes > 0:
    changes = 0 # reset this back to zero - we've found zero when we start a new cycle
    for row in range(0, max_rows):
        for col in range(0, max_cols):
            # now we're looking for numeric adjaceny, to numbers already "adjacent"
            if coords_and_data[(row, col)]["adj"] == "true":
                star_coords = False
                if coords_and_data[(row, col)].get("star_coords"):
                    star_coords = coords_and_data[(row, col)]["star_coords"]
                if col < max_cols-1:
                    changes += update_adjacency(row, col+1, star_coords)   # right
                if col > 0:
                    changes += update_adjacency(row, col-1, star_coords)   # left

# print(coords_and_data)
# print(coords_and_data[(2,58)])

# build a list of tuples of numbers considered adjacent to any symbol, and - if
# that symbol was a star - what those coordinates were (otherwise store (-1, -1))
numbers_adjacent = []
for row in range(0, max_rows):
    crafted_number = ""
    star_coords = (-1, -1)
    for col in range(0, max_cols):
        # if it's an "adjacent" number, add that to our number string
        if coords_and_data[(row, col)]["adj"] == "true":
            crafted_number += coords_and_data[(row, col)]["val"]
            if coords_and_data[(row, col)].get("star_coords"):
                star_coords = coords_and_data[(row, col)]["star_coords"]
        # if it's not and we have a number crafted, add that to our list and reset
        elif crafted_number != "":
            numbers_adjacent.append((int(crafted_number), star_coords))
            crafted_number = ""
            star_coords = (-1, -1)
        # otherwise it's a just a dot or something, so we do nothing
    # make sure we include numbers which end at the line end - see input_test2.txt
    if crafted_number != "":
        numbers_adjacent.append((int(crafted_number), star_coords))

#print(numbers_adjacent)
print("part 1:", sum([x[0] for x in numbers_adjacent]))

# part 2 begins

potential_gear_ratios = defaultdict(lambda: [])
for i in range(0, len(numbers_adjacent)):
    crafted_number = numbers_adjacent[i][0]
    star_coords = numbers_adjacent[i][1]
    if star_coords != (-1, -1):
        potential_gear_ratios[star_coords].append(crafted_number)
#print(potential_gear_ratios)
total_gear_ratios = 0
for potential_gear_ratio in potential_gear_ratios.keys():
    if len(potential_gear_ratios[potential_gear_ratio]) == 2:
        total_gear_ratios += (potential_gear_ratios[potential_gear_ratio][0] * potential_gear_ratios[potential_gear_ratio][1])

print("part 2:", total_gear_ratios)
