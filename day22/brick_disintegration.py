import string
from collections import defaultdict

real_data = True

if real_data:
    file = open("input.txt", "r")
else:
    file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

bricks_coords = {}

# we'll use this to sort the bricks so we generally fall the lower bricks first
# rather than the unordered way in which the input.txt file arrives
brick_names_lowest_z = []

# parse the input data
brick_id = 0
for line in data:
    if real_data:
        brick_name = str(brick_id)
    else:
        brick_name = string.ascii_uppercase[brick_id]
    from_coords, to_coords = line.split("~")
    from_x, from_y, from_z = [int(coord) for coord in from_coords.split(",")]
    to_x, to_y, to_z = [int(coord) for coord in to_coords.split(",")]
    diff_x = abs(to_x - from_x)
    diff_y = abs(to_y - from_y)
    diff_z = abs(to_z - from_z)
    if max(diff_x, diff_y, diff_z) == 0: # single cell brick
        bricks_coords[(to_x, to_y, to_z)] = brick_name
    else:
        x,y,z = (min(from_x, to_x), min(from_y, to_y), min(from_z, to_z))
        while x <= max(from_x, to_x) and y <= max(from_y, to_y) and z <= max(from_z, to_z):
            bricks_coords[(x, y, z)] = brick_name
            if diff_x:
                x += 1
            if diff_y:
                y += 1
            if diff_z:
                z += 1
    brick_names_lowest_z.append((brick_name, min(from_z, to_z)))
    brick_id += 1

# roughly sort the bricks into a better falling order - it's not perfect, but
# it's close enough and far better than input.txt's ordering
brick_names_lowest_z.sort(key=lambda brick: brick[1])
brick_names = [b[0] for b in brick_names_lowest_z]

def can_brick_fall(brick_name, bricks_coords):
    current_brick_coords = [k for k in bricks_coords if bricks_coords[k] == brick_name]
    if len(current_brick_coords) > 1: # so it's not a single brick
        # look to handle vertical bricks - we only need to check the lowest
        # point of those bricks, so we switch to checking just that as we fall
        if current_brick_coords[0][0] == current_brick_coords[1][0] and \
           current_brick_coords[0][1] == current_brick_coords[1][1]:
            lowest_point = 10000000000
            for current_brick_coord in current_brick_coords:
                lowest_point = min(lowest_point, current_brick_coord[2])
            current_brick_coords = [(current_brick_coords[0][0], current_brick_coords[0][1], lowest_point)]
    brick_parts_fall_by = [] # store how many cells downwards an individual brick's part could fall
    for current_brick_coord in current_brick_coords:
        current_fall = 0
        current_z = current_brick_coord[2]-1
        while current_z > 0: # stop if we hit the ground
            if (current_brick_coord[0], current_brick_coord[1], current_z) in bricks_coords.keys():
                current_z = 0
            else:
                current_fall += 1
                current_z -= 1
        brick_parts_fall_by.append(current_fall)
    if min(brick_parts_fall_by) > 0:
        return True, min(brick_parts_fall_by)
    else:
        return False, None

def fall_brick(brick_name, bricks_coords, fall_by):
    current_brick_coords = [k for k in bricks_coords if bricks_coords[k] == brick_name]
    for current_brick_coord in current_brick_coords:
        bricks_coords[(current_brick_coord[0], current_brick_coord[1], current_brick_coord[2]-fall_by)] = bricks_coords.pop(current_brick_coord)

# fall the bricks
any_fallen = True
while any_fallen:
    any_fallen = False # reset
    for brick_name in brick_names:
        can_fall, fall_by = can_brick_fall(brick_name, bricks_coords)
        if can_fall:
            any_fallen = True
            fall_brick(brick_name, bricks_coords, fall_by)

#print(bricks_coords)

# check each brick to see if any are directly above, that they are supporting
# and which are below, that are supporting it
supported_by = defaultdict(list) # bricks, and what they are supported by
for brick_name in brick_names:
    current_brick_coords = [k for k in bricks_coords if bricks_coords[k] == brick_name]
    for current_brick_coord in current_brick_coords:
        if bricks_coords.get((current_brick_coord[0], current_brick_coord[1], current_brick_coord[2]+1)):
            supporting_brick_name = bricks_coords[(current_brick_coord[0], current_brick_coord[1], current_brick_coord[2]+1)]
            if supporting_brick_name != brick_name:
                #print(brick_name, "supporting...", supporting_brick_name)
                supported_by[supporting_brick_name].append(brick_name)

#print("supported_by", supported_by)

cant_be_disintegrated = []
for brick_name in supported_by.keys():
    if len(set(supported_by[brick_name])) == 1:
        cant_be_disintegrated.append(supported_by[brick_name][0])

#print("cant_be_disintegrated", set(cant_be_disintegrated))

print("part 1:", len(set(brick_names).difference(set(cant_be_disintegrated))))

# part 2 begins

sum_of_falling_bricks = 0

for chain_reaction_brick in set(cant_be_disintegrated):
    bricks_disintegrated_or_falling = {chain_reaction_brick}
    remaining_supports = supported_by.copy()
    falls = -1
    while falls != 0: # keep going until no more new bricks would fall in the chain reaction
        falls = 0
        bricks_to_fall = []
        for brick_name in remaining_supports.keys():
            if set(remaining_supports[brick_name]).issubset(bricks_disintegrated_or_falling):
                falls += 1
                bricks_disintegrated_or_falling.add(brick_name)
                bricks_to_fall.append(brick_name)
        for brick_name in bricks_to_fall:
            del remaining_supports[brick_name]
    sum_of_falling_bricks += (len(bricks_disintegrated_or_falling)-1) # minus 1 as we include the starting brick name

print("part 2:", sum_of_falling_bricks)
