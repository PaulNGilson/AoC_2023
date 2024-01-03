file = open("input_unreachable.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

def get_coords():
    coords = {}
    for row in range(0, len(data)):
        for col in range(0, len(data[0])):
            cell_content = data[row][col]
            if cell_content == "S":
                coords[(row, col)] = {"cell": ".", "visited": None}
            elif cell_content == "#":
                coords[(row, col)] = {"cell": "#", "visited": "rock"}
            else:
                coords[(row, col)] = {"cell": data[row][col], "visited": None}
    return coords

def get_valid_positions(position, coords):
    valid_positions = []
    row, col = position
    # right
    if row < len(data[0])-1 and not coords[(row+1, col)]["visited"]:
        valid_positions.append((row+1, col))
    # left
    if row > 0 and not coords[(row-1, col)]["visited"]:
        valid_positions.append((row-1, col))
    # down
    if col < len(data)-1 and not coords[(row, col+1)]["visited"]:
        valid_positions.append((row, col+1))
    # up
    if col > 0 and not coords[(row, col-1)]["visited"]:
        valid_positions.append((row, col-1))
    #print("new valid positions", valid_positions)
    return valid_positions

def make_steps(steps_to_make, starting_coords):
    steps_so_far = 0

    furthest_reached = [starting_coords]

    coords = get_coords()

    # set step count of "zero" for starting cell to be Even:
    coords[furthest_reached[0]] = {"cell": ".", "visited": "even"}

    while steps_so_far < steps_to_make:
        new_furthest_reached = []
        steps_so_far += 1
        for position in furthest_reached:
            valid_positions = get_valid_positions(position, coords)
            new_furthest_reached += valid_positions
            for valid_position in valid_positions:
                if steps_so_far % 2 == 0: # even number of steps
                    coords[(valid_position)]["visited"] = "even"
                else:
                    coords[(valid_position)]["visited"] = "odd"
        furthest_reached = new_furthest_reached
    return coords

# variant is for counting Odd or Even places reached
def examine_and_print_grid(variant, coords, printing=False):
    odd_reached = 0
    even_reached = 0
    for row in range(0, len(data)):
        output_line = ""
        for col in range(0, len(data[0])):
            if coords[(row, col)]["visited"] == "odd":
                output_line += "O"
                odd_reached += 1
            elif coords[(row, col)]["visited"] == "even":
                output_line += "E"
                even_reached += 1
            else:
                output_line += coords[(row, col)]["cell"]
        if printing:
            if row == 65:
                print(output_line, 65)
            else:
                print(output_line)
    if variant == "odd":
        return odd_reached
    else:
        return even_reached

# grid name/type
# number of grids of that type
# steps to make
# starting coords
# count Odd or Even
grids = [
    {"name": "W", "number": 1, "steps_to_make": 130, "starting_coords": (65,130), "odd_even": "even"},
    {"name": "E", "number": 1, "steps_to_make": 130, "starting_coords": (65,0), "odd_even": "even"},
    {"name": "S", "number": 1, "steps_to_make": 130, "starting_coords": (0,65), "odd_even": "even"},
    {"name": "N", "number": 1, "steps_to_make": 130, "starting_coords": (130,65), "odd_even": "even"},
    
    {"name": "M", "number": 202299, "steps_to_make": 195, "starting_coords": (130,130), "odd_even": "odd"},
    {"name": "O", "number": 202299, "steps_to_make": 195, "starting_coords": (130,0), "odd_even": "odd"},
    {"name": "R", "number": 202299, "steps_to_make": 195, "starting_coords": (0,130), "odd_even": "odd"},
    {"name": "T", "number": 202299, "steps_to_make": 195, "starting_coords": (0,0), "odd_even": "odd"},
    
    {"name": "m", "number": 202300, "steps_to_make": 64, "starting_coords": (130,130), "odd_even": "even"},
    {"name": "o", "number": 202300, "steps_to_make": 64, "starting_coords": (130,0), "odd_even": "even"},
    {"name": "r", "number": 202300, "steps_to_make": 64, "starting_coords": (0,130), "odd_even": "even"},
    {"name": "t", "number": 202300, "steps_to_make": 64, "starting_coords": (0,0), "odd_even": "even"},
    
    {"name": "G", "number": 40924885401, "steps_to_make": 131, "starting_coords": (65,65), "odd_even": "odd"},
    {"name": "g", "number": 40925290000, "steps_to_make": 131, "starting_coords": (65,65), "odd_even": "even"}
]

part_2_total = 0

for grid in grids:
    reachable_count = examine_and_print_grid(grid["odd_even"], make_steps(grid["steps_to_make"], grid["starting_coords"]), False)
    grid_total = grid["number"]*reachable_count
    print("grid", grid["name"], "reachable count", reachable_count, "- total is (*", grid["number"], ") :", grid_total)
    part_2_total += grid_total

print("part 2:", part_2_total)

"""
Start cell was 65,65.

For the NSEW grids, we're doing 130 steps from the middle of the sides. Because
we have an even number of steps remaining, our true Odd reachable cells will in
this case be the ones marked as even. So, we have inputs and counts:

W: start (65,130), 130 steps, Odd count 5576 BUT Even count 5619
E: start (65,0), 130 steps, Odd count 5551 BUT Even count 5593
S: start (0,65), 130 steps, Odd count 5555 BUT Even count 5608
N: start (130,65), 130 steps, Odd count 5572 BUT Even count 5604

For the upper case grids, they start from the corners and with 195 steps that
will mean we do check the Odd reachable cells:

M (NW): start (130,130), 195 steps, Odd count 6524
O (NE): start (130,0), 195 steps, Odd count 6522
R (SW): start (0,130), 195 steps, Odd count 6537
T (SE): start (0,0), 195 steps, Odd count 6513

For the lower case grids, they start from the corners too, but as they are with
64 steps it's the same as WESN above - we look at Even reachable cells:

m (NW): start (130,130), 64 steps, Even count 954
o (NE): start (130,0), 64 steps, Even count 947
r (SW): start (0,130), 64 steps, Even count 951
t (SE): start (0,0), 64 steps, Even count 933

so the calculation is:

1*W = 5619
1*E = 5593
1*S = 5608
1*N = 5604
202299*M = 1319798676
202299*O = 1319394078
202299*R = 1322428563
202299*T = 1317573387
202300*m = 192994200
202300*o = 191578100
202300*r = 192387300
202300*t = 188745900
40924885401*G = 304562997154242
40925290000*g = 305138962240000

5619 + 5593 + 5608 + 5604 + 1319798676 + 1319394078 + 1322428563 + 1317573387 +
192994200 + 191578100 + 192387300 + 188745900 + 304562997154242 +
305138962240000
= 609708004316870
"""