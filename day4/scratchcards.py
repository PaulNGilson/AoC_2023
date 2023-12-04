import re
import math

file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

winning_points = 0
card_counts = [1 for x in range(0, len(data))]

for i in range(0, len(data)-1):
    line = data[i]
    card_number_s, card_winners_s, card_numbers_s = re.split(': | \| ', line)
    card_winners = re.split("  | ", card_winners_s.strip())
    card_numbers = re.split("  | ", card_numbers_s.strip())
    wins = len(set(card_winners).intersection(set(card_numbers)))
    copies_of_this_card = card_counts[i]
    for j in range(1, wins+1):
        card_counts[i+j] += copies_of_this_card
    winning_points += math.floor(2**(wins-1))

print("part 1:", winning_points)
print("part 2:", sum(card_counts))
