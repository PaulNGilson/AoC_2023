import math

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

times = [int(x) for x in data[0].split()[1:]]
distances = [int(x) for x in data[1].split()[1:]]

total_winning_ways = []
for i in range(0, len(times)):
    winning_ways = 0
    button_hold = 0
    while button_hold <= times[i]:
        attempt_distance = button_hold * (times[i]-button_hold)
        if attempt_distance > distances[i]:
            winning_ways += 1
        button_hold += 1
    #print(winning_ways)
    total_winning_ways.append(winning_ways)

print("part 1:", math.prod(total_winning_ways))

# part 2 begins

time_part_2 = int("".join(data[0].split()[1:]))
distance_part_2 = int("".join(data[1].split()[1:]))

button_hold = 0
winning_ways = 0
while button_hold <= time_part_2:
    attempt_distance = button_hold * (time_part_2-button_hold)
    if attempt_distance > distance_part_2:
        winning_ways += 1
    button_hold += 1
print("part 2:", winning_ways)
