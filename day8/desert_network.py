import re
import math

#file = open("input.txt", "r")
file = open("input_test.txt", "r")
#file = open("input_test_part_2.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

directions = list(data[0].strip())
node_routes = {}
for nr in data[2:]:
    matches = re.search(r'([A-Z]{3}) = \(([A-Z]{3}), ([A-Z]{3})\)', nr)
    node_from, node_l, node_r = matches.groups()
    node_routes[node_from] = {"L": node_l, "R": node_r}

current_node = "AAA"
steps = 0
while current_node != "ZZZ":
    direction = directions[0]
    current_node = node_routes[current_node][direction]
    directions = directions[1:] + [directions[0]]
    steps += 1

print("part 1:", steps)

# part 2 begins

file = open("input.txt", "r")
#file = open("input_test_part_2.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

directions = list(data[0].strip())
node_routes = {}
for nr in data[2:]:
    matches = re.search(r'([A-Z0-9]{3}) = \(([A-Z0-9]{3}), ([A-Z0-9]{3})\)', nr)
    node_from, node_l, node_r = matches.groups()
    node_routes[node_from] = {"L": node_l, "R": node_r}

# def ghosts_not_on_z(current_ghost_nodes):
#     outcome = [x for x in current_ghost_nodes if x[-1] != "Z"]
#     # if len(outcome) < len(current_ghost_nodes):
#     #     print(f"bad ghosts: {len(outcome)} (of {len(current_ghost_nodes)})")
#     return outcome

current_ghost_nodes = [x for x in node_routes.keys() if x[-1] == "A"]

# debugging...
# it seems that, despite not starting at ??A, each ghost always returns to Z
# after the same number of steps - it's some weird property of the test data; I
# don't know how/whether I should know that, or had to discover it
# 
# current_ghost_nodes = [current_ghost_nodes[5]]

# steps = 0
# while ghosts_not_on_z(current_ghost_nodes):
#     direction = directions[0]
#     for i in range(0, len(current_ghost_nodes)):
#         current_ghost_nodes[i] = node_routes[current_ghost_nodes[i]][direction]
#     directions = directions[1:] + [directions[0]]
#     steps += 1
# print(steps)

# debugging...

ghosts_steps = []
for current_ghost_node in current_ghost_nodes:
    ghost_steps = 0
    directions = list(data[0].strip())
    while current_ghost_node[-1] != "Z":
        direction = directions[0]
        current_ghost_node = node_routes[current_ghost_node][direction]
        directions = directions[1:] + [directions[0]]
        ghost_steps += 1
    ghosts_steps.append(ghost_steps)

print("part 2:", math.lcm(*ghosts_steps))
