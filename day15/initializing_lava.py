from collections import defaultdict

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()

data = data_raw[0].split(",")

def reindeer_hash(s):
    current_value = 0
    for c in s:
        current_value += ord(c)
        current_value *= 17
        current_value = current_value % 256
    return current_value

results_sum = 0
for s in data:
    results_sum += reindeer_hash(s)
print("part 1:", results_sum)

# part 2 begins

boxes = {}
for b in range(0, 256):
    boxes[b] = defaultdict(int)

for s in data:
    if "=" in s:
        label, focal_length = s.split("=")
        box_num = reindeer_hash(label)
        boxes[box_num][label] = int(focal_length)
    else:
        label = s.rstrip("-")
        box_num = reindeer_hash(label)
        if boxes[box_num].get(label):
            boxes[box_num].pop(label)

total_focusing_power = 0

for box_num in boxes:
    slot_num = 1
    for lens in boxes[box_num].keys():
        focusing_power = (box_num+1) * slot_num * boxes[box_num][lens]
        slot_num += 1
        total_focusing_power += focusing_power

print("part 2:", total_focusing_power)
