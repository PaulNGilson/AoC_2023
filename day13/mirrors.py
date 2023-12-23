file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

patterns = []
next_pattern = []
for line in data:
    if line == "":
        patterns.append(next_pattern)
        next_pattern = []
    else:
        next_pattern.append(line)
patterns.append(next_pattern)
#print(patterns)

rows_above = 0
cols_to_left = 0

for pattern in patterns:
    #print(pattern)
    mirror = False
    current_row = 0
    while current_row < len(pattern)-1 and not mirror:
        top_row = current_row
        bottom_row = current_row + 1
        #print("top row", top_row, "bottom row", bottom_row)
        while pattern[top_row] == pattern[bottom_row]:
            top_row -= 1
            bottom_row += 1
            #print("  top row", top_row, "bottom row", bottom_row)
            if top_row < 0 or bottom_row >= len(pattern):
                mirror = True
                #print("mirror found, top row is", current_row)
                rows_above += current_row+1
                break
        current_row += 1
    
    pattern_cols = []
    for i in range(0, len(pattern[0])):
        new_col = ""
        for row in pattern:
            new_col += row[i]
        pattern_cols.append(new_col)
    current_col = 0
    while current_col < len(pattern_cols)-1 and not mirror:
        left_col = current_col
        right_col = current_col + 1
        #print("left col", left_col, "right col", right_col)
        while pattern_cols[left_col] == pattern_cols[right_col]:
            left_col -= 1
            right_col += 1
            #print("  left col", left_col, "right col", right_col)
            if left_col < 0 or right_col >= len(pattern_cols):
                mirror = True
                #print("mirror found, left col is", current_col)
                cols_to_left += current_col+1
                break
        current_col += 1

print("part 1:", 100*rows_above + cols_to_left)

# part 2 begins

rows_above = 0
cols_to_left = 0

for pattern in patterns:
    #print(pattern)
    current_row = 0
    while current_row < len(pattern)-1:
        smudges = 0
        top_row = current_row
        bottom_row = current_row + 1
        while top_row >= 0 and bottom_row < len(pattern):
            smudges += sum(1 for x,y in zip(pattern[top_row], pattern[bottom_row]) if x != y)
            top_row -= 1
            bottom_row += 1
        #print("row", current_row, "smudges", smudges)
        if smudges == 1:
            rows_above += current_row+1
        current_row += 1
    
    pattern_cols = []
    for i in range(0, len(pattern[0])):
        new_col = ""
        for row in pattern:
            new_col += row[i]
        pattern_cols.append(new_col)
    current_col = 0
    while current_col < len(pattern_cols)-1:
        smudges = 0
        left_col = current_col
        right_col = current_col + 1
        while left_col >= 0 and right_col < len(pattern_cols):
            smudges += sum(1 for x,y in zip(pattern_cols[left_col], pattern_cols[right_col]) if x != y)
            left_col -= 1
            right_col += 1
        #print("col", current_col, "smudges", smudges)
        if smudges == 1:
            cols_to_left += current_col+1
        current_col += 1

print("part 2:", 100*rows_above + cols_to_left)