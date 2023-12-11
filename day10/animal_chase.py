file = open("input.txt", "r")
#file = open("input_test.txt", "r")
#file = open("input_test_2.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

start = (-1, -1)
for row in range(0, len(data)):
    if "S" in data[row]:
        start = (row, data[row].index("S"))

start_directions = []
if start[0] != 0:
    if data[start[0]-1][start[1]] in "|7F":
        start_directions.append("N")
if start[0] < len(data)-1:
    if data[start[0]+1][start[1]] in "|LJ":
        start_directions.append("S")
if start[1] != 0:
    if data[start[0]][start[1]-1] in "-LF":
        start_directions.append("W")
if start[1] < len(data[0])-1:
    if data[start[0]][start[1]+1] in "-J7":
        start_directions.append("E")

routes = {"a": {"dir": start_directions[0], "coords": start},
          "b": {"dir": start_directions[1], "coords": start}}
all_loop_coords = [start]

def new_direction(prev_dir, pipe_shape):
    if pipe_shape == "|" or pipe_shape == "-":
        return prev_dir
    elif pipe_shape == "L":
        if prev_dir == "S":
            return "E"
        else:
            return "N"
    elif pipe_shape == "J":
        if prev_dir == "S":
            return "W"
        else:
            return "N"
    elif pipe_shape == "7":
        if prev_dir == "N":
            return "W"
        else:
            return "S"
    else: # "F"
        if prev_dir == "N":
            return "E"
        else:
            return "S"

def make_move(k):
    # update coords
    if routes[k]["dir"] == "S":
        routes[k]["coords"] = (routes[k]["coords"][0]+1, routes[k]["coords"][1])
    elif routes[k]["dir"] == "E":
        routes[k]["coords"] = (routes[k]["coords"][0], routes[k]["coords"][1]+1)
    elif routes[k]["dir"] == "N":
        routes[k]["coords"] = (routes[k]["coords"][0]-1, routes[k]["coords"][1])
    else: # "W"
        routes[k]["coords"] = (routes[k]["coords"][0], routes[k]["coords"][1]-1)
    # find new direction it is facing in
    pipe_shape = data[routes[k]["coords"][0]][routes[k]["coords"][1]]
    routes[k]["dir"] = new_direction(routes[k]["dir"], pipe_shape)

def make_moves_both():
    make_move("a")
    make_move("b")

steps = 0
while routes["a"]["coords"] != routes["b"]["coords"] or routes["a"]["coords"] == start:
    make_moves_both()
    # some data we'll want for part 2, acquired now to be efficient
    all_loop_coords.append(routes["a"]["coords"])
    all_loop_coords.append(routes["b"]["coords"])
    steps += 1

print("part 1:", steps)

# part 2 begins

all_loop_coords.pop() # we've duplicated the final place, so remove it

# using left and right to help visualize the path moved along...
# ...but will print as "X" and "Y" later on, as "L" already used as pipe tiles
sides = {"L": [], "R": []}

# simple visual display of the grid to aid debugging
def display_grid():
    for row in range(0, len(data)):
        out_row = ""
        for col in range(0, len(data[0])):
            if (row, col) in all_loop_coords:
                out_row += "#"
            elif (row, col) in sides["L"]:
                out_row += "X"
            elif (row, col) in sides["R"]:
                out_row += "Y"
            else:
                out_row += "."
        print(out_row)
    print("")

#display_grid()

# move around the loop again, one direction this time, considering whether tiles
# are "to the left" or "to the right" (direction doesn't matter, it's just the
# grouping)
routes = {"a": {"dir": start_directions[0], "coords": start}}
while routes["a"]["coords"] != start or sides["L"] == []:
    row = routes["a"]["coords"][0]
    col = routes["a"]["coords"][1]
    if data[row][col] == "|":
        if routes["a"]["dir"] == "N":
            sides["L"].append((row, col-1))
            sides["R"].append((row, col+1))
        else:
            sides["L"].append((row, col+1))
            sides["R"].append((row, col-1))
    elif data[row][col] == "-":
        if routes["a"]["dir"] == "W":
            sides["L"].append((row+1, col))
            sides["R"].append((row-1, col))
        else:
            sides["L"].append((row-1, col))
            sides["R"].append((row+1, col))
    elif data[row][col] == "L":
        if routes["a"]["dir"] == "E":
            sides["R"].append((row, col-1))
            sides["R"].append((row+1, col))
        else:
            sides["L"].append((row, col-1))
            sides["L"].append((row+1, col))
    elif data[row][col] == "J":
        if routes["a"]["dir"] == "N":
            sides["R"].append((row, col+1))
            sides["R"].append((row+1, col))
        else:
            sides["L"].append((row, col+1))
            sides["L"].append((row+1, col))
    elif data[row][col] == "7":
        if routes["a"]["dir"] == "W":
            sides["R"].append((row, col+1))
            sides["R"].append((row-1, col))
        else:
            sides["L"].append((row, col+1))
            sides["L"].append((row-1, col))
    elif data[row][col] == "F":
        if routes["a"]["dir"] == "S":
            sides["R"].append((row-1, col))
            sides["R"].append((row, col-1))
        else:
            sides["L"].append((row-1, col))
            sides["L"].append((row, col-1))
    make_move("a")

#display_grid()

# collate all "." tiles that aren't our pipe loop nor adjacent to it
not_yet_reached_dots = []
for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        if (row, col) not in all_loop_coords and \
           (row, col) not in sides["L"] and \
           (row, col) not in sides["R"]:
            not_yet_reached_dots.append((row, col))

# expand the "X" and "Y" tiles into adjacent "." tiles, until one stops
# expanding - this is most likely to be our contained area, and with the input
# data is the "Y"/"R" area
new_xs = 1
new_ys = 1
while new_xs != 0 and new_ys != 0:
    still_not_yet_reached_dots = []
    new_xs = 0
    new_ys = 0
    for dot_coord in not_yet_reached_dots:
        if (dot_coord[0]+1, dot_coord[1]) in sides["L"] or \
           (dot_coord[0]-1, dot_coord[1]) in sides["L"] or \
           (dot_coord[0], dot_coord[1]+1) in sides["L"] or \
           (dot_coord[0], dot_coord[1]-1) in sides["L"]:
            sides["L"].append(dot_coord)
            new_xs += 1
        elif (dot_coord[0]+1, dot_coord[1]) in sides["R"] or \
             (dot_coord[0]-1, dot_coord[1]) in sides["R"] or \
             (dot_coord[0], dot_coord[1]+1) in sides["R"] or \
             (dot_coord[0], dot_coord[1]-1) in sides["R"]:
            sides["R"].append(dot_coord)
            new_ys += 1
        else:
            still_not_yet_reached_dots.append(dot_coord)
    not_yet_reached_dots = still_not_yet_reached_dots

#display_grid()

print("part 2:", len(set(sides["R"]).difference(set(all_loop_coords))))
