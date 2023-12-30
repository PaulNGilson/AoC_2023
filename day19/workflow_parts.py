import re

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []

# input file parsing - two different sections
workflows = {}
parts = []
workflow_section = True
for line in data_raw:
    if line.strip() == "":
        workflow_section = False
    elif workflow_section:
        workflow_name, workflow_str = re.search(r'([a-z]*){(.*)}', line.strip()).groups()
        workflows[workflow_name] = workflow_str.split(",")
    else: # parts section
        x,m,a,s = re.search(r'{x=(\d*),m=(\d*),a=(\d*),s=(\d*)}', line.strip()).groups()
        parts.append({"x":int(x), "m":int(m), "a":int(a), "s":int(s)})

def calculate_part_outcome(part):
    current_workflow = "in"
    i = 0
    while current_workflow != "A" and current_workflow != "R":
        if "<" in workflows[current_workflow][i] or ">" in workflows[current_workflow][i]:
            category, ltgt, threshold_str, outcome = re.search(r'([xmas])([<>])(\d*):([A-Za-z]*)', workflows[current_workflow][i]).groups()
            if ltgt == ">":
                if part[category] > int(threshold_str):
                    current_workflow = outcome
                    i = 0
                else:
                    i += 1
            else: # ltgt == "<"
                if part[category] < int(threshold_str):
                    current_workflow = outcome
                    i = 0
                else:
                    i += 1
        else: # we must have reached a conclusion - A, R or a new workflow
            current_workflow = workflows[current_workflow][i]
            i = 0
    return current_workflow

total_accepted_part_ratings = 0

for part in parts:
    if calculate_part_outcome(part) == "A":
        total_accepted_part_ratings += sum(part.values())

print("part 1:", total_accepted_part_ratings)

# part 2 begins

part_range_workflows = [{"x": [1, 4000], "m": [1, 4000], "a": [1, 4000], "s": [1, 4000], "workflow": "in", "workflow_index": 0}]
accepted_range_workflows = []

while part_range_workflows:
    part_range_workflow = part_range_workflows.pop()
    current_workflow = part_range_workflow["workflow"]
    i = part_range_workflow["workflow_index"]
    if current_workflow == "A":
        #print("Accepting", part_range_workflow)
        accepted_range_workflows.append(part_range_workflow)
    elif current_workflow == "R":
        #print("Rejecting", part_range_workflow)
        pass
    elif "<" in workflows[current_workflow][i] or ">" in workflows[current_workflow][i]:
        category, ltgt, threshold_str, outcome = re.search(r'([xmas])([<>])(\d*):([A-Za-z]*)', workflows[current_workflow][i]).groups()
        threshold = int(threshold_str)
        if ltgt == ">": # what numbers in our range are greater than the threshold
            if part_range_workflow[category][1] <= threshold: # none of them are big enough
                part_range_workflow["workflow_index"] += 1
                part_range_workflows.append(part_range_workflow)
            elif part_range_workflow[category][0] > threshold: # all of them are big enough
                if outcome == "A":
                    #print("Accepting", part_range_workflow)
                    accepted_range_workflows.append(part_range_workflow)
                elif outcome == "R":
                    #print("Rejecting", part_range_workflow)
                    pass
                else:
                    part_range_workflow["workflow"] = outcome
                    part_range_workflow["workflow_index"] = 0
                    part_range_workflows.append(part_range_workflow)
            else: # some are, some aren't...
                part_range_workflow_new = part_range_workflow.copy() # _new will be the successful ones
                # successful
                part_range_workflow_new["workflow"] = outcome
                part_range_workflow_new["workflow_index"] = 0
                part_range_workflow_new[category] = [threshold+1, part_range_workflow[category][1]]
                part_range_workflows.append(part_range_workflow_new)
                # unsuccessful
                part_range_workflow["workflow_index"] += 1
                part_range_workflow[category] = [part_range_workflow[category][0], threshold]
                part_range_workflows.append(part_range_workflow)
        elif ltgt == "<": # what numbers in our range are lower than the threshold
            if part_range_workflow[category][0] >= threshold: # none of them are small enough
                part_range_workflow["workflow_index"] += 1
                part_range_workflows.append(part_range_workflow)
            elif part_range_workflow[category][1] < threshold: # all of them are small enough
                if outcome == "A":
                    #print("Accepting", part_range_workflow)
                    accepted_range_workflows.append(part_range_workflow)
                elif outcome == "R":
                    #print("Rejecting", part_range_workflow)
                    pass
                else:
                    part_range_workflow["workflow"] = outcome
                    part_range_workflow["workflow_index"] = 0
                    part_range_workflows.append(part_range_workflow)
            else: # some are, some aren't...
                part_range_workflow_new = part_range_workflow.copy() # _new will be the successful ones
                # successful
                part_range_workflow_new["workflow"] = outcome
                part_range_workflow_new["workflow_index"] = 0
                part_range_workflow_new[category] = [part_range_workflow[category][0], threshold-1]
                part_range_workflows.append(part_range_workflow_new)
                # unsuccessful
                part_range_workflow["workflow_index"] += 1
                part_range_workflow[category] = [threshold, part_range_workflow[category][1]]
                part_range_workflows.append(part_range_workflow)
    elif workflows[current_workflow][i] == "A":
        #print("Accepting", part_range_workflow)
        accepted_range_workflows.append(part_range_workflow)
    elif workflows[current_workflow][i] == "R":
        #print("Rejecting", part_range_workflow)
        pass
    else: # moving to another workflow
        part_range_workflow["workflow"] = workflows[current_workflow][i]
        part_range_workflow["workflow_index"] = 0
        part_range_workflows.append(part_range_workflow)

number_of_rating_combinations = 0
for arw in accepted_range_workflows:
    number_of_rating_combinations += (arw["x"][1]-arw["x"][0]+1)*(arw["m"][1]-arw["m"][0]+1)*(arw["a"][1]-arw["a"][0]+1)*(arw["s"][1]-arw["s"][0]+1)

print("part 2:", number_of_rating_combinations)
