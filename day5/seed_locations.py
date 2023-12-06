file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

mappings = {}
seeds = []

current_map = ""
for i in range(0, len(data)):
    line = data[i]
    if line == "":
        pass
    elif "seeds" in line:
        seeds = [int(x) for x in line.split()[1:]]
    elif "map" in line:
        current_map = line.split()[0]
        mappings[current_map] = []
    else: # numerical mappings line
        destination_range_start, source_range_start, range_length = [int(x) for x in line.strip().split()]
        mappings[current_map].append([destination_range_start, source_range_start, range_length])

def apply_mapping(mapping_name, current_val):
    new_val = current_val
    for drs, srs, rl in mappings[mapping_name]:
        if current_val in range(srs, srs+rl):
            increase = current_val-srs
            new_val = drs+increase
    return new_val

lowest_location = 2**100
for current_val in seeds:
    for mapping in mappings.keys():
        current_val = apply_mapping(mapping, current_val)
    #print(current_val)
    lowest_location = min(lowest_location, current_val)

print("part 1:", lowest_location)

# part 2 begins

# a way to check the range mappings - i.e. how many seeds before & after
# def count_total(ranges):
#     t = 0
#     for r in ranges:
#         t += 1+r[1]-r[0]
#     return t

seed_ranges = []
i = 0
while i < len(seeds):
    seed_ranges.append((seeds[i], seeds[i]+seeds[i+1]-1))
    i += 2
#print("seed ranges:", seed_ranges)
#print(count_total(seed_ranges))

def apply_range_mappings(mapping_name, initial_range):
    mapped_ranges = []
    still_to_try_to_map = [initial_range]
    for drs, srs, rl in mappings[mapping_name]:
        didnt_map = []
        for r in still_to_try_to_map:
            if r[0] > srs+rl-1:
                didnt_map += [r]
            elif r[1] < srs:
                didnt_map += [r]
            # from here onwards, we have some sort of overlap and mapping required
            elif r[0] < srs and r[1] <= srs+rl-1:
                didnt_map += [(r[0], srs-1)]
                mapped_ranges += [(drs, r[1]-srs+drs)]
            elif r[0] >= srs and r[1] > srs+rl-1:
                didnt_map += [(srs+rl, r[1])]
                mapped_ranges += [(r[0]-srs+drs, drs+rl-1)]
            elif r[0] < srs and r[1] > srs+rl-1:
                didnt_map += [(r[0], srs-1)]
                didnt_map += [(srs+rl, r[1])]
                mapped_ranges += [(drs, drs+rl-1)]
            # we don't need more logic here - all values in range at this point are mapped
            else:
                mapped_ranges += [(r[0]-srs+drs, r[1]-srs+drs)]
        still_to_try_to_map = didnt_map
    mapped_ranges += still_to_try_to_map
    return mapped_ranges

current_ranges = seed_ranges
for mapping in mappings.keys():
    new_ranges = []
    for current_range in current_ranges:
        new_ranges += apply_range_mappings(mapping, current_range)
    current_ranges = new_ranges
    #print(count_total(current_ranges))

lowest_location_part_2 = 2**100
for location_range in current_ranges:
    lowest_location_part_2 = min(lowest_location_part_2, location_range[0])

print("part 2:", lowest_location_part_2)
