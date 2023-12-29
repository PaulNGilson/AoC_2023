file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

def build_starting_cells():
    cells = {}
    for row in range(0, len(data)):
        for col in range(0, len(data[0])):
            cells[(row, col)] = {"beams": [], "cell_val": data[row][col]}
    return cells

def count_beam_cells(current_cells):
    count = 0
    for row in range(0, len(data)):
        for col in range(0, len(data[0])):
            if len(current_cells[(row, col)]["beams"]) == 1:
                count += 1
    return(count)

def print_cells():
    for row in range(0, len(data)):
        output = ""
        for col in range(0, len(data[0])):
            if cells[(row, col)]["beams"] == []:
                output += cells[(row, col)]["cell_val"]
            else:
                if len(cells[(row, col)]["beams"]) == 1:
                    output += "#"
                else:
                    output += str(len(cells[(row, col)]["beams"]))
        print(output)

def calculate_beams(current_beams, cells):
    while current_beams:
        beam_row, beam_col, beam_dir = current_beams.pop()
        if beam_dir == "E":
            beam_col += 1
        elif beam_dir == "W":
            beam_col -= 1
        elif beam_dir == "S":
            beam_row += 1
        else: # "N"
            beam_row -= 1
        
        #print("beam is now", beam_row, beam_col, beam_dir)
        
        gone_off_edge = False
        # has it fallen off the edge?
        if beam_col not in range(0, len(data[0])):
            gone_off_edge = True
        if beam_row not in range(0, len(data)):
            gone_off_edge = True
        
        repeating_a_beam = False
        # are we repeating a beam already done?
        if not gone_off_edge and beam_dir in cells[(beam_row, beam_col)]["beams"]:
            repeating_a_beam = True
        
        if not gone_off_edge and not repeating_a_beam:
            # adds to our list of beams entering cells
            cells[(beam_row, beam_col)]["beams"] = beam_dir
            cell_val_of_beam = cells[(beam_row, beam_col)]["cell_val"]
            if beam_dir == "N":
                if cell_val_of_beam == "|":
                    current_beams.append((beam_row, beam_col, beam_dir))
                elif cell_val_of_beam == "-":
                    current_beams.append((beam_row, beam_col, "W"))
                    current_beams.append((beam_row, beam_col, "E"))
                elif cell_val_of_beam == "\\":
                    current_beams.append((beam_row, beam_col, "W"))
                elif cell_val_of_beam == "/":
                    current_beams.append((beam_row, beam_col, "E"))
                else: # "."
                    current_beams.append((beam_row, beam_col, beam_dir))
            elif beam_dir == "S":
                if cell_val_of_beam == "|":
                    current_beams.append((beam_row, beam_col, beam_dir))
                elif cell_val_of_beam == "-":
                    current_beams.append((beam_row, beam_col, "W"))
                    current_beams.append((beam_row, beam_col, "E"))
                elif cell_val_of_beam == "\\":
                    current_beams.append((beam_row, beam_col, "E"))
                elif cell_val_of_beam == "/":
                    current_beams.append((beam_row, beam_col, "W"))
                else: # "."
                    current_beams.append((beam_row, beam_col, beam_dir))
            elif beam_dir == "W":
                if cell_val_of_beam == "|":
                    current_beams.append((beam_row, beam_col, "N"))
                    current_beams.append((beam_row, beam_col, "S"))
                elif cell_val_of_beam == "-":
                    current_beams.append((beam_row, beam_col, beam_dir))
                elif cell_val_of_beam == "\\":
                    current_beams.append((beam_row, beam_col, "N"))
                elif cell_val_of_beam == "/":
                    current_beams.append((beam_row, beam_col, "S"))
                else: # "."
                    current_beams.append((beam_row, beam_col, beam_dir))
            elif beam_dir == "E":
                if cell_val_of_beam == "|":
                    current_beams.append((beam_row, beam_col, "N"))
                    current_beams.append((beam_row, beam_col, "S"))
                elif cell_val_of_beam == "-":
                    current_beams.append((beam_row, beam_col, beam_dir))
                elif cell_val_of_beam == "\\":
                    current_beams.append((beam_row, beam_col, "S"))
                elif cell_val_of_beam == "/":
                    current_beams.append((beam_row, beam_col, "N"))
                else: # "."
                    current_beams.append((beam_row, beam_col, beam_dir))
        
        # print_cells()
        # print(current_beams)
        # print(count_beam_cells())
        # print("")
    return cells

# a list of beams exiting cells
current_beams = [(0, -1, "E")] # row, col, beam direction
part_1_cells = calculate_beams(current_beams, build_starting_cells())
print("part 1:", count_beam_cells(part_1_cells))

# part 2 begins

outcomes = []

for row in range(0, len(data)):
    outcome_cells = calculate_beams([(row, -1, "E")], build_starting_cells())
    outcomes.append(count_beam_cells(outcome_cells))
    outcome_cells = calculate_beams([(row, len(data[0]), "W")], build_starting_cells())
    outcomes.append(count_beam_cells(outcome_cells))
for col in range(0, len(data[0])):
    outcome_cells = calculate_beams([(-1, col, "S")], build_starting_cells())
    outcomes.append(count_beam_cells(outcome_cells))
    outcome_cells = calculate_beams([(len(data), col, "N")], build_starting_cells())
    outcomes.append(count_beam_cells(outcome_cells))

print("part 2:", max(outcomes))
