from functools import reduce

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

limits = {"red": 12, "green": 13, "blue": 14}

# store what we'll need to collect for part 1's, and part 2's calculations
valid_game_ids = []
powers = []

for line in data:
    game_id = int(line.split(":")[0].split(" ")[1])
    draws = line.split(":")[1].lstrip().split(";")
    
    # for determining in part 1 if the game is considered "valid" given the
    # `limits` defined above
    valid_game = True
    
    # for counting the minimum number of cubes of each colour that would need to
    # be in the bag, for the draws to have been possible
    required_cubes = {"red": 0, "green": 0, "blue": 0}
    for draw in draws:
        colours = [x.strip() for x in draw.split(",")]
        for colour in colours:
            required_cubes[colour.split(" ")[1]] = max(required_cubes[colour.split(" ")[1]], int(colour.split(" ")[0]))
            if limits[colour.split(" ")[1]] < int(colour.split(" ")[0]):
                valid_game = False
    if valid_game:
        #print(game_id, "valid")
        valid_game_ids.append(game_id)
    #print(game_id, required_cubes)
    powers.append(reduce(lambda x, y: x*y, required_cubes.values()))

print("part 1:", sum(valid_game_ids))
print("part 2:", sum(powers))
