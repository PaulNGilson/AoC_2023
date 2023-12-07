file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

hands = []

card_values = {"A":14, "K":13, "Q":12, "J":11, "T":10, "9":9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2}

hand_types = {"5OK":7, "4OK":6, "FH":5, "3OK":4, "2P":3 , "1P": 2, "HC": 1}

# we'll firstly use sets to determine hand type, then a bit of card counting for
# those that are a bit similar e.g. four-of-a-kind and full house
def get_hand_type(cards):
    if len(set(cards)) == 1:
        return "5OK"
    elif len(set(cards)) == 2:
        if 4 in [cards.count(x) for x in set(cards)]:
            return "4OK"
        else:
            return "FH"
    elif len(set(cards)) == 3:
        if 3 in [cards.count(x) for x in set(cards)]:
            return "3OK"
        else:
            return "2P"
    elif len(set(cards)) == 4:
        return "1P"
    else:
        return "HC"

def val_cards_only(cards, val_lookup):
    vals = ""
    for card in cards:
        card_val = val_lookup[card]
        vals += f"{card_val:02d}"
    return vals

for line in data:
    hand, bid = line.split()
    cards = [x for x in hand]
    hands.append({
        #"hand": hand,
        "bid": int(bid),
        #"type": hand_type(cards),
        "hand_val": str(hand_types[get_hand_type(cards)]) + val_cards_only(cards, card_values), # x xx xx xx xx xx
        "rank": -1,
    })

hands.sort(key=lambda x: int(x["hand_val"]))

total_winnings = 0
for i in range(0, len(hands)):
    hands[i]["rank"] = i+1
    total_winnings += hands[i]["rank"]*hands[i]["bid"]

print("part 1:", total_winnings)

# part 2 begins

card_values_part_2 = {"A":14, "K":13, "Q":12, "T":10, "9":9, "8":8, "7":7, "6":6, "5":5, "4":4, "3":3, "2":2, "J":1}

hands_part_2 = []

def get_max_joker_hand_val(cards):
    if "J" not in set(cards):
        return hand_types[get_hand_type(cards)]
    elif cards == ["J", "J", "J", "J", "J"]:
        return 7
    possible_vals = []
    for c in set(cards).difference(set("J")):
        joker_subbed_cards = [x for x in cards if x != "J"] + [c]*cards.count("J")
        possible_vals.append(hand_types[get_hand_type(joker_subbed_cards)])
    return max(possible_vals)

for line in data:
    hand, bid = line.split()
    cards = [x for x in hand]
    joker_hand_val = get_max_joker_hand_val(cards)
    hands_part_2.append({
        #"hand": hand,
        "bid": int(bid),
        #"type": hand_type(cards),
        "hand_val": str(joker_hand_val) + val_cards_only(cards, card_values_part_2), # x xx xx xx xx xx
        "rank": -1,
    })

hands_part_2.sort(key=lambda x: int(x["hand_val"]))

total_winnings_part_2 = 0
for i in range(0, len(hands)):
    hands_part_2[i]["rank"] = i+1
    total_winnings_part_2 += hands_part_2[i]["rank"]*hands_part_2[i]["bid"]

print("part 2:", total_winnings_part_2)
