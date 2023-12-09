file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

def calculate_diffs(nums):
    num_diffs = []
    for i in range(0, len(nums)-1):
        num_diffs.append(nums[i+1]-nums[i])
    return num_diffs

total_end = 0
total_start = 0
for line in data:
    sequences = [[int(x) for x in line.split()]]
    while len(set(sequences[-1])) > 1:
        sequences.append(calculate_diffs(sequences[-1]))
    
    next_add_end = 0
    next_add_start = 0
    for num_diffs in reversed(sequences):
        # part 1
        num_diffs.append(next_add_end + num_diffs[-1])
        next_add_end = num_diffs[-1]
        
        # part 2
        num_diffs.insert(0, num_diffs[0] - next_add_start)
        next_add_start = num_diffs[0]
    #print(sequences)
    total_end += sequences[0][-1]
    total_start += sequences[0][0]

print("part 1:", total_end)
print("part 2:", total_start)
