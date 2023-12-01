import string

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
#file = open("input_test_2.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

letters = string.ascii_lowercase
sum_1 = 0

# just strip letters off the left and right, such that the first and last
# characters are now are required integers
for line in data:
    simplified = line.lstrip(letters).rstrip(letters)
    calibration_value = int(simplified[0] + simplified[-1])
    sum_1 += calibration_value

print("part 1:", sum_1)

# part 2 begins

numbers = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"] + list(string.digits)
sum_2 = 0

# using the `numbers` list, look up the values - for integers, it's themselves,
# for the strings, we'll determine it by their index in `numbers`
def get_int_value(val):
    if val in string.digits:
        return val
    else:
        return numbers.index(val)+1

# we'll look for the leftmost and rightmost indexes of integers and string
# representations of numbers
for line in data:
    leftmost = {"index": 10000000000, "num": ""}
    rightmost = {"index": -1, "num": ""}
    for num in numbers:
        if num in line:
            if line.index(num) < leftmost["index"]:
                leftmost = {"index": line.index(num), "num": num}
            if line.rindex(num)+len(num)-1 > rightmost["index"]:
                rightmost = {"index": line.rindex(num)+len(num)-1, "num": num}
    
    lval = get_int_value(leftmost["num"])
    rval = get_int_value(rightmost["num"])
    sum_2 += int(str(lval) + str(rval)) # add on our line's calibration_value

print("part 2:", sum_2)
