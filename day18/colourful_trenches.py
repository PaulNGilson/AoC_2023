file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

data = data + [data[0]] # redo the first at the end so we close the loop

def new_ourcoords_position_and_end_coords(ourcoords, direction, next_direction, start_coords, length):
    if ourcoords == "bot-left" and direction == "U":
        if next_direction == "R":
            return "top-left", (start_coords[0], start_coords[1]+length+1)
        elif next_direction == "L":
            return ourcoords, (start_coords[0], start_coords[1]+length)
    elif ourcoords == "bot-left" and direction == "L":
        if next_direction == "U":
            return ourcoords, (start_coords[0]-length, start_coords[1])
        elif next_direction == "D":
            return "bot-right", (start_coords[0]-(length-1), start_coords[1])
    
    elif ourcoords == "bot-right" and direction == "L":
        if next_direction == "U":
            return "bot-left", (start_coords[0]-(length+1), start_coords[1])
        elif next_direction == "D":
            return ourcoords, (start_coords[0]-length, start_coords[1])
    elif ourcoords == "bot-right" and direction == "D":
        if next_direction == "L":
            return ourcoords, (start_coords[0], start_coords[1]-length)
        elif next_direction == "R":
            return "top-right", (start_coords[0], start_coords[1]-(length-1))
    
    elif ourcoords == "top-right" and direction == "D":
        if next_direction == "L":
            return "bot-right", (start_coords[0], start_coords[1]-(length+1))
        elif next_direction == "R":
            return ourcoords, (start_coords[0], start_coords[1]-length)
    elif ourcoords == "top-right" and direction == "R":
        if next_direction == "D":
            return ourcoords, (start_coords[0]+length, start_coords[1])
        elif next_direction == "U":
            return "top-left", (start_coords[0]+length-1, start_coords[1])
    
    elif ourcoords == "top-left" and direction == "R":
        if next_direction == "D":
            return "top-right", (start_coords[0]+length+1, start_coords[1])
        elif next_direction == "U":
            return ourcoords, (start_coords[0]+length, start_coords[1])
    elif ourcoords == "top-left" and direction == "U":
        if next_direction == "R":
            return ourcoords, (start_coords[0], start_coords[1]+length)
        elif next_direction == "L":
            return "bot-left", (start_coords[0], start_coords[1]+length-1)

def print_area_for_part_n(all_coords, n):
    all_coords = all_coords + [all_coords[0]]
    total = 0
    for i in range(0, len(all_coords)-1):
        total += all_coords[i][0]*all_coords[i+1][1] - all_coords[i][1]*all_coords[i+1][0]
    total /= 2
    print(f"part {n}:", int(abs(total)))

ourcoords = "top-left"
current_coords = (0, 0)
all_coords = []

ourcoords_part2 = "bot-left" # hard-coded; this would be "top-left" for the test data
current_coords_part2 = (0, 0)
all_coords_part2 = []

direction_lookup = {"0": "R", "1": "D", "2": "L", "3": "U"}

for i in range(0, len(data)-1):
    direction, length_str, colour_str = data[i].split()
    next_direction, _, next_colour_str = data[i+1].split()
    ourcoords, current_coords = new_ourcoords_position_and_end_coords(ourcoords, direction, next_direction, current_coords, int(length_str))
    all_coords.append(current_coords)
    
    # part 2 begins

    length_part2 = int(colour_str[2:-2], 16)
    direction_part2 = direction_lookup[colour_str[-2]]
    next_direction_part2 = direction_lookup[next_colour_str[-2]]
    ourcoords_part2, current_coords_part2 = new_ourcoords_position_and_end_coords(ourcoords_part2, direction_part2, next_direction_part2, current_coords_part2, length_part2)
    all_coords_part2.append(current_coords_part2)

print_area_for_part_n(all_coords, "1")
print_area_for_part_n(all_coords_part2, "2")
