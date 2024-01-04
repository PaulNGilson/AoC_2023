from collections import defaultdict

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

coords = {}

def get_neighbour_cells(coord):
    neighbours = {} # keys of coords, values of cells
    if coord[1] < len(data[0])-1:
        neighbours[(coord[0], coord[1]+1)] = coords[(coord[0], coord[1]+1)]
    if coord[1] > 0:
        neighbours[(coord[0], coord[1]-1)] = coords[(coord[0], coord[1]-1)]
    if coord[0] < len(data)-1:
        neighbours[(coord[0]+1, coord[1])] = coords[(coord[0]+1, coord[1])]
    if coord[0] > 0:
        neighbours[(coord[0]-1, coord[1])] = coords[(coord[0]-1, coord[1])]
    return neighbours

for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        coords[(row, col)] = data[row][col]

# note where crossroads exist so we can measure paths between them
crossroads = {}

start_cell = (-1, -1)
end_cell = (-1, -1)

crossroad_id = 0
for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        if row != 0 and row != len(data)-1:
            if data[row][col] == "." and "." not in get_neighbour_cells((row, col)).values():
                crossroads[(row, col)] = str(crossroad_id)
                crossroad_id += 1
        elif row == 0 and data[row][col] == ".":
            start_cell = (row, col)
        elif row == len(data)-1 and data[row][col] == ".":
            end_cell = (row, col)

#print(crossroads)

# tuples of start, end and length
connected_routes = []

# tuples of coordinates, steps so far, previous origin, list of past position coords
current_positions = [(start_cell, 0, "S", [])]
while current_positions:
    current_coord, distance, origin, past_positions = current_positions.pop()
    # if we're at a crossroad, we make all the possible moves downhill and add
    # those to our list of current_positions, as well as updating our path
    # lengths from the origin to the crossroad
    if current_coord == end_cell:
        connected_routes.append((origin, "E", distance))
    else:
        if current_coord in crossroads.keys():
            connected_routes.append((origin, crossroads[current_coord], distance))
            distance = 0
            origin = crossroads[current_coord]
            #print("we've reached a crossroads, so connected_routes", connected_routes)
        # keep on moving
        neighbours = get_neighbour_cells(current_coord)
        for neighbour_coord in neighbours.keys():
            if neighbours[neighbour_coord] == "." and neighbour_coord not in past_positions:
                current_positions.append((neighbour_coord, distance+1, origin, past_positions+[current_coord]))
            elif neighbours[neighbour_coord] == "v" and neighbour_coord not in past_positions and neighbour_coord[0] == current_coord[0]+1:
                current_positions.append((neighbour_coord, distance+1, origin, past_positions+[current_coord]))
            elif neighbours[neighbour_coord] == "^" and neighbour_coord not in past_positions and neighbour_coord[0] == current_coord[0]-1:
                current_positions.append((neighbour_coord, distance+1, origin, past_positions+[current_coord]))
            elif neighbours[neighbour_coord] == ">" and neighbour_coord not in past_positions and neighbour_coord[1] == current_coord[1]+1:
                current_positions.append((neighbour_coord, distance+1, origin, past_positions+[current_coord]))
            elif neighbours[neighbour_coord] == "<" and neighbour_coord not in past_positions and neighbour_coord[1] == current_coord[1]-1:
                current_positions.append((neighbour_coord, distance+1, origin, past_positions+[current_coord]))

connected_route_dict = defaultdict(dict)
for origin, destination, length in set(connected_routes):
    connected_route_dict[origin][destination] = length

#print(connected_route_dict)

routes = [("S", 0)]
lengths = []

while routes:
    route = routes.pop()
    destinations = connected_route_dict[route[0]].keys()
    for destination in destinations:
        if destination == "E":
            lengths.append(route[1]+connected_route_dict[route[0]][destination])
        else:
            routes.append((destination, route[1]+connected_route_dict[route[0]][destination]))
#print(lengths)

print("part 1:", max(lengths))

# part 2 begins

# make our graph an undirected one by adding reverses of all the possible directions
for origin in connected_route_dict.keys():
    for destination in connected_route_dict[origin]:
        if destination != "E" and origin != "S":
            connected_route_dict[destination][origin] = connected_route_dict[origin][destination]

# with an undirected graph, we now need to make sure it's acyclic and prevent
# loops, so keep track of where a route has visited this time
routes = [("S", 0, ["S"])]
lengths = []

while routes:
    route = routes.pop()
    destinations = connected_route_dict[route[0]].keys()
    for destination in destinations:
        if destination not in route[2]:
            if destination == "E":
                lengths.append(route[1]+connected_route_dict[route[0]][destination])
            else:
                routes.append((destination, route[1]+connected_route_dict[route[0]][destination], route[2]+[destination]))
#print(lengths)

print("part 2:", max(lengths))

"""
With my crossroad labels:

#S#####################
#.......#########...###
#######.#########.#.###
###.....#.>0>.###.#.###
###v#####.#v#.###.#.###
###1>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>2#
#.#.#v#######v###.###v#
#...#3>.#...>4>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>5>.#.>6###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################E#

Recommended route:

S->1->0->4->2->6->E

{
('S', '1', 15),
('0', '2', 30), ('0', '4', 24),
('1', '3', 22), ('1', '0', 22),
('2', '6', 10),
('3', '5', 38), ('3', '4', 12),
('4', '5', 10), ('4', '2', 18),
('5', '6', 10),
('6', 'E', 5)
}

15+22+24+18+10+5 = 94, the part 1 answer
"""
