from fnmatch import fnmatch
from functools import lru_cache

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

@lru_cache(maxsize=None)
def get_permutations(spring_data_string, contiguous_springs_tuple):
    contiguous_springs = list(contiguous_springs_tuple)
    perms = 0
    still_to_try = [(spring_data_string, contiguous_springs)]
    while still_to_try:
        spring_string, required_hashes = still_to_try.pop()
        if "#" in spring_string:
            next_hash_index = spring_string.index("#")
        else:
            next_hash_index = len(spring_string)-1
        potential_indexes = [n for (n,e) in enumerate(spring_string) if e == "?" and n < next_hash_index] + [next_hash_index]
        for potential_index in potential_indexes:
            if len(required_hashes) > 1:
                string_to_match = spring_string[:potential_index+required_hashes[0]+1]
                potential_match = "."*potential_index + "#"*required_hashes[0] + "."
                if fnmatch(potential_match, string_to_match):
                    still_to_try.append((spring_string[len(potential_match):], required_hashes[1:]))
            else:
                string_to_match = spring_string[:potential_index+required_hashes[0]]
                potential_match = "."*potential_index + "#"*required_hashes[0]
                if fnmatch(potential_match, string_to_match) and "#" not in spring_string[len(potential_match):]:
                    perms += 1
    return perms

@lru_cache(maxsize=None)
def calculate_pieces(remaining_spring_string, contiguous_springs_tuple, remaining_factor):
    contiguous_springs = list(contiguous_springs_tuple)
    total = 0
    if remaining_factor == 1:
        total += get_permutations(remaining_spring_string, tuple(contiguous_springs))
    else:
        needed_length = sum(contiguous_springs) + len(contiguous_springs) - 1
        for i in range(needed_length, len(remaining_spring_string)-needed_length+1):
            if remaining_spring_string[i-1] != "." and remaining_spring_string[i] != "#":
                total += get_permutations(remaining_spring_string[:i-1]+"#", tuple(contiguous_springs)) * calculate_pieces(remaining_spring_string[i+1:], tuple(contiguous_springs), remaining_factor-1)
    return total

def main(factor):
    linenum = 1
    total = 0
    for line in data:
        spring_data_string_folded, contiguous_springs_string_folded = line.split()
        spring_data_string = "?".join([spring_data_string_folded]*factor)
        contiguous_springs_folded = [int(x) for x in contiguous_springs_string_folded.split(",")]
        perms = calculate_pieces(spring_data_string, tuple(contiguous_springs_folded), factor)
        #print("linenum", linenum, perms)
        total += perms
        linenum += 1
    return total

print("part 1:", main(1))
print("part 2:", main(5))
