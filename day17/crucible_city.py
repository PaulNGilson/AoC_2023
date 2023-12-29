file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

cells = {}

for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        cells[(row, col)] = {"cost": int(data[row][col]), \
                             "N": {}, \
                             "S": {}, \
                             "E": {}, \
                             "W": {}}

# calculate a valid total heat loss we can use for pruning poor route
current_min_heat_loss = 0
current = (0, 0)
next_dir = "E"
while current != (len(data)-1, len(data[0])-1):
    if next_dir == "E":
        current = (current[0], current[1]+1)
        current_min_heat_loss += cells[(current[0], current[1])]["cost"]
        next_dir = "S"
    elif next_dir == "S":
        current = (current[0]+1, current[1])
        current_min_heat_loss += cells[(current[0], current[1])]["cost"]
        next_dir = "E"
#print(current_min_heat_loss)
best_route = {"heatloss": current_min_heat_loss, "directions": "ESES...SES"}

def viable_route_and_update(route, heatloss_increase, max_dir):
    global best_route
    potential_new_heatloss = route["heatloss"] + heatloss_increase
    if potential_new_heatloss >= best_route["heatloss"]:
        return False, None
    number_moves_in_dir = len(route["heading"])
    direction = route["heading"][-1]
    cell_bests = cells[(route["coords"][0], route["coords"][1])][direction]

    if cell_bests.get(number_moves_in_dir) and cell_bests[number_moves_in_dir] <= potential_new_heatloss:
        return False, None
    else:
        cells[(route["coords"][0], route["coords"][1])][direction][number_moves_in_dir] = potential_new_heatloss
        i = number_moves_in_dir+1
        while i <= max_dir:
            if cell_bests.get(i) and cell_bests[i] >= potential_new_heatloss:
                del cells[(route["coords"][0], route["coords"][1])][direction][i]
            i += 1
        if route["coords"] == (len(data)-1, len(data[0])-1):
            if best_route["heatloss"] > potential_new_heatloss:
                best_route = {"heatloss": potential_new_heatloss, "directions": route["so_far"]+direction}
                #print("new best route:", best_route)
            return False, None
        else:
            return True, potential_new_heatloss

# part 1 begins

routes = [{"coords": (0, 1), "heading": "E", "heatloss": 0, "so_far": ""},{"coords": (1, 0), "heading": "S", "heatloss": 0, "so_far": ""}]

while routes:
    route = routes.pop()
    heatloss_increase = cells[(route["coords"][0], route["coords"][1])]["cost"]
    was_viable, new_heatloss = viable_route_and_update(route, heatloss_increase, 3)
    if was_viable:
        if route["heading"][-1] == "E":
            if route["coords"][0] > 0:
                routes.append({"coords": (route["coords"][0]-1, route["coords"][1]), "heading": "N", "heatloss": new_heatloss, "so_far": route["so_far"]+"E"})
            if route["coords"][0] < len(data)-1:
                routes.append({"coords": (route["coords"][0]+1, route["coords"][1]), "heading": "S", "heatloss": new_heatloss, "so_far": route["so_far"]+"E"})
            if len(route["heading"]) < 3 and route["coords"][1] < len(data[0])-1: # we can go further east
                routes.append({"coords": (route["coords"][0], route["coords"][1]+1), "heading": route["heading"]+"E", "heatloss": new_heatloss, "so_far": route["so_far"]+"E"})
        elif route["heading"][-1] == "W":
            if route["coords"][0] > 0:
                routes.append({"coords": (route["coords"][0]-1, route["coords"][1]), "heading": "N", "heatloss": new_heatloss, "so_far": route["so_far"]+"W"})
            if route["coords"][0] < len(data)-1:
                routes.append({"coords": (route["coords"][0]+1, route["coords"][1]), "heading": "S", "heatloss": new_heatloss, "so_far": route["so_far"]+"W"})
            if len(route["heading"]) < 3 and route["coords"][1] > 0:
                routes.append({"coords": (route["coords"][0], route["coords"][1]-1), "heading": route["heading"]+"W", "heatloss": new_heatloss, "so_far": route["so_far"]+"W"})
        elif route["heading"][-1] == "S":
            if route["coords"][1] > 0: # west
                routes.append({"coords": (route["coords"][0], route["coords"][1]-1), "heading": "W", "heatloss": new_heatloss, "so_far": route["so_far"]+"S"})
            if route["coords"][1] < len(data[0])-1:
                routes.append({"coords": (route["coords"][0], route["coords"][1]+1), "heading": "E", "heatloss": new_heatloss, "so_far": route["so_far"]+"S"})
            if len(route["heading"]) < 3 and route["coords"][0] < len(data)-1:
                routes.append({"coords": (route["coords"][0]+1, route["coords"][1]), "heading": route["heading"]+"S", "heatloss": new_heatloss, "so_far": route["so_far"]+"S"})
        elif route["heading"][-1] == "N":
            if route["coords"][1] > 0: # west
                routes.append({"coords": (route["coords"][0], route["coords"][1]-1), "heading": "W", "heatloss": new_heatloss, "so_far": route["so_far"]+"N"})
            if route["coords"][1] < len(data[0])-1:
                routes.append({"coords": (route["coords"][0], route["coords"][1]+1), "heading": "E", "heatloss": new_heatloss, "so_far": route["so_far"]+"N"})
            if len(route["heading"]) < 3 and route["coords"][0] > 0:
                routes.append({"coords": (route["coords"][0]-1, route["coords"][1]), "heading": route["heading"]+"N", "heatloss": new_heatloss, "so_far": route["so_far"]+"N"})
    #time.sleep(0.01)

#print(cells[(len(data)-1, len(data[0])-1)])
print("part 1:", best_route)

# part 2 begins

cells = {}

for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        cells[(row, col)] = {"cost": int(data[row][col]), \
                             "N": {}, \
                             "S": {}, \
                             "E": {}, \
                             "W": {}}

best_route = {"heatloss": 5000, "directions": "EEEE...SSSS"}

routes = [{"coords": (0, 1), "heading": "E", "heatloss": 0, "so_far": ""},{"coords": (1, 0), "heading": "S", "heatloss": 0, "so_far": ""}]

while routes:
    route = routes.pop()
    heatloss_increase = cells[(route["coords"][0], route["coords"][1])]["cost"]
    was_viable, new_heatloss = viable_route_and_update(route, heatloss_increase, 10)
    if was_viable:
        if route["heading"][-1] == "E":
            if route["coords"][0] > 0 and len(route["heading"]) >= 4:
                routes.append({"coords": (route["coords"][0]-1, route["coords"][1]), "heading": "N", "heatloss": new_heatloss, "so_far": route["so_far"]+"E"})
            if route["coords"][0] < len(data)-1 and len(route["heading"]) >= 4:
                routes.append({"coords": (route["coords"][0]+1, route["coords"][1]), "heading": "S", "heatloss": new_heatloss, "so_far": route["so_far"]+"E"})
            if len(route["heading"]) < 10 and route["coords"][1] < len(data[0])-1: # we can go further east
                routes.append({"coords": (route["coords"][0], route["coords"][1]+1), "heading": route["heading"]+"E", "heatloss": new_heatloss, "so_far": route["so_far"]+"E"})
        elif route["heading"][-1] == "W":
            if route["coords"][0] > 0 and len(route["heading"]) >= 4:
                routes.append({"coords": (route["coords"][0]-1, route["coords"][1]), "heading": "N", "heatloss": new_heatloss, "so_far": route["so_far"]+"W"})
            if route["coords"][0] < len(data)-1 and len(route["heading"]) >= 4:
                routes.append({"coords": (route["coords"][0]+1, route["coords"][1]), "heading": "S", "heatloss": new_heatloss, "so_far": route["so_far"]+"W"})
            if len(route["heading"]) < 10 and route["coords"][1] > 0:
                routes.append({"coords": (route["coords"][0], route["coords"][1]-1), "heading": route["heading"]+"W", "heatloss": new_heatloss, "so_far": route["so_far"]+"W"})
        elif route["heading"][-1] == "S":
            if route["coords"][1] > 0 and len(route["heading"]) >= 4: # west
                routes.append({"coords": (route["coords"][0], route["coords"][1]-1), "heading": "W", "heatloss": new_heatloss, "so_far": route["so_far"]+"S"})
            if route["coords"][1] < len(data[0])-1 and len(route["heading"]) >= 4:
                routes.append({"coords": (route["coords"][0], route["coords"][1]+1), "heading": "E", "heatloss": new_heatloss, "so_far": route["so_far"]+"S"})
            if len(route["heading"]) < 10 and route["coords"][0] < len(data)-1:
                routes.append({"coords": (route["coords"][0]+1, route["coords"][1]), "heading": route["heading"]+"S", "heatloss": new_heatloss, "so_far": route["so_far"]+"S"})
        elif route["heading"][-1] == "N":
            if route["coords"][1] > 0 and len(route["heading"]) >= 4: # west
                routes.append({"coords": (route["coords"][0], route["coords"][1]-1), "heading": "W", "heatloss": new_heatloss, "so_far": route["so_far"]+"N"})
            if route["coords"][1] < len(data[0])-1 and len(route["heading"]) >= 4:
                routes.append({"coords": (route["coords"][0], route["coords"][1]+1), "heading": "E", "heatloss": new_heatloss, "so_far": route["so_far"]+"N"})
            if len(route["heading"]) < 10 and route["coords"][0] > 0:
                routes.append({"coords": (route["coords"][0]-1, route["coords"][1]), "heading": route["heading"]+"N", "heatloss": new_heatloss, "so_far": route["so_far"]+"N"})

#print(cells[(len(data)-1, len(data[0])-1)])
print("part 2:", best_route)
