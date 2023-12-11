file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

rows_to_double = []
cols_to_double = []
for row in range(0, len(data)):
    if "#" not in data[row]:
        rows_to_double.append(row)
for col in range(0, len(data[0])):
    hash_found = False
    for row in range(0, len(data)):
        if "#" == data[row][col]:
            hash_found = True
    if not hash_found:
        cols_to_double.append(col)

# for visualisation and debugging in part 1 i.e. expansion_amount=2
# galaxy_grid = []
# for row in range(0, len(data)):
#     expanded_row = ""
#     for col in range(0, len(data[0])):
#         if col in cols_to_double:
#             expanded_row += ".."
#         else:
#             expanded_row += data[row][col]
#     galaxy_grid.append(expanded_row)
#     if row in rows_to_double:
#         galaxy_grid.append(expanded_row)
# 
# def display_grid():
#     for line in galaxy_grid:
#         print(line)
#     print("")
# 
#display_grid()

galaxy_coords_no_expansion = []
for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        if data[row][col] == "#":
            galaxy_coords_no_expansion.append((row, col))

def calculate_total_distances(expansion_amount, galaxy_coords):
    total_distances_more_expansion = 0
    while len(galaxy_coords) > 1:
        current_galaxy = galaxy_coords.pop()
        for distant_galaxy in galaxy_coords:
            factor_cols = sum(x in range(min(current_galaxy[1], distant_galaxy[1]), max(current_galaxy[1], distant_galaxy[1])) for x in cols_to_double)
            factor_rows = sum(x in range(min(current_galaxy[0], distant_galaxy[0]), max(current_galaxy[0], distant_galaxy[0])) for x in rows_to_double)
            total_distances_more_expansion += (abs(current_galaxy[0]-distant_galaxy[0]) + abs(current_galaxy[1]-distant_galaxy[1]) + factor_cols*(expansion_amount-1) + factor_rows*(expansion_amount-1))
    return total_distances_more_expansion

print("part 1:", calculate_total_distances(2, galaxy_coords_no_expansion.copy()))
print("part 2:", calculate_total_distances(1000000, galaxy_coords_no_expansion.copy()))
