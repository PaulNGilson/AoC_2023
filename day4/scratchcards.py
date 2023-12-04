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
card_counts = [1]*len(data) # start off with one copy of each card

for i in range(0, len(data)-1):
    _, card_winners_s, card_numbers_s = re.split(': | \| ', data[i])
    card_winners = re.split("  | ", card_winners_s.strip())
    card_numbers = re.split("  | ", card_numbers_s.strip())
    wins = len(set(card_winners).intersection(set(card_numbers)))
    
    # part 1 begins
    winning_points += math.floor(2**(wins-1)) # 1 for 1 win, 2 for 2, 4 for 3, etc.
    
    # part 2 begins
    for j in range(1, wins+1):
        card_counts[i+j] += card_counts[i] # add on the number of copies of the current card

print("part 1:", winning_points)
print("part 2:", sum(card_counts))
