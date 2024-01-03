file = open("input.txt", "r")
#file = open("input_test.txt", "r")
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

coords = {}
furthest_reached = []
for row in range(0, len(data)):
    for col in range(0, len(data[0])):
        cell_content = data[row][col]
        if cell_content == "S":
            coords[(row, col)] = {"cell": ".", "visited": "even"}
            furthest_reached.append((row, col))
        elif cell_content == "#":
            coords[(row, col)] = {"cell": "#", "visited": "rock"}
        else:
            coords[(row, col)] = {"cell": data[row][col], "visited": None}

def get_valid_positions(position):
    valid_positions = []
    row, col = position
    # right
    if row < len(data[0])-1 and not coords[(row+1, col)]["visited"]:
        valid_positions.append((row+1, col))
    # left
    if row > 0 and not coords[(row-1, col)]["visited"]:
        valid_positions.append((row-1, col))
    # down
    if col < len(data)-1 and not coords[(row, col+1)]["visited"]:
        valid_positions.append((row, col+1))
    # up
    if col > 0 and not coords[(row, col-1)]["visited"]:
        valid_positions.append((row, col-1))
    #print("new valid positions", valid_positions)
    return valid_positions

steps_so_far = 0

while steps_so_far < 64:
    new_furthest_reached = []
    steps_so_far += 1
    for position in furthest_reached:
        valid_positions = get_valid_positions(position)
        new_furthest_reached += valid_positions
        for valid_position in valid_positions:
            if steps_so_far % 2 == 0: # even number of steps
                coords[(valid_position)]["visited"] = "even"
            else:
                coords[(valid_position)]["visited"] = "odd"
    furthest_reached = new_furthest_reached

#print(furthest_reached)

reached = 0
for row in range(0, len(data)):
    output_line = ""
    for col in range(0, len(data[0])):
        if coords[(row, col)]["visited"] == "even":
            output_line += "O"
            reached += 1
        else:
            output_line += coords[(row, col)]["cell"]
    #print(output_line)
print("part 1:", reached)

# part 2 begins

"""
Planning; N.B. execution was done in a new file, with tweaked functions.

Grids are odd numbered but square - odd/even step spaces will alternate as we
start moving into interconnected grids i.e.:

+-----+-----+-----+
|     |     |     |
|     |  E  |     |
|     | EOE |     |
|     |EOEOE|     |
|    E|OEOEO|E    |
+-----+-----+-----+
|   EO|EOEOE|OE   |
|  EOE|OEOEO|EOE  |
| EOEO|EOSOE|OEOE |
|  EOE|OEOEO|EOE  |
|   EO|EOEOE|OE   |
+-----+-----+-----+
|    E|OEOEO|E    |
|     |EOEOE|     |
|     | EOE |     |
|     |  E  |     |
|     |     |     |
+-----+-----+-----+



Let's name some of the grids we'll need to consider and count, assuming we'll
cover ground something like:

+---------+---------+
|         |    O    |
|         |   O     |
|         |  O      |
|         | O       |
|         |O        |
|        O|         |
|       O |         |
|      O  |         |
|     O   |         |
+---------+---------+
|    O    |         |
|   O     |         |
|  O      |         |
| O       |         |
|O        |         |
| O       |         |
|  O      |         |
|   O     |         |
|    O    |         |
+---------+---------+

 mNo
mM Oo
W S E
rR Tt
 rSt

So with our "S" being the starting grid (shortly to be renamed itself, too), we
have WESN at the far left/right/bottom/top, and some others at NE, NW, etc.
We'll look at those (upper and lower case) grid names later.



Question: do we cover all cells of a single grid, once we have reached all 4
corners, and does that happen at the same time for all four corners?

Answer: we don't cover *all* the cells after 130 steps - not just due to rocks,
but due to areas like this in the input data:

.#.
#.#
.#.

making some unreachable. Rather than programmatically handle this, just created
input_unreachable.txt as a fixed-up file with those 11 cells filled with "#".

...but we do cover all the cells at the same time, as the corners are all
reached, at least.



26501365 steps required, so we're looking at Odd total steps.

From the starting grid, we have the following line across the middle:

.................................................................S [...]

so that's 65 steps to reach the edge of the first grid (heading West), 66 steps
to reach the first cell of the next grid (heading West) - I'll call this a
"2-star":

.2.
212
.2.

As we can traverse an entire grid in 131 steps, if we had step count 66+(1*131)
= 197 we'd be in the first cell of a 3-star:

..3..
.323.
32123
.323.
..3..

E.g. if we had step count 66+(2*131) = 328 we'd be in the first cell of a
4-star.

So for 26501365 steps... if we had step count 66+(202299*131) = 26501235 we'd be
in the first cell of a 202301-star.

But that number of steps leaves us 26501365-26501235 = 130 steps short, so
another 130 steps and we're in the last cell of that grid (as predicted, given
the diamond-space-shaped input data).



How many grids, of each type, are we dealing with? Thinking back to:

 mNo
mM Oo
W   E
rR Tt
 rSt

we're now looking at the blank grids in the middle. Where G is a single grid of
the 131*131 cells, we'll call:

G - 1-star

.g.
gGg - 2-star
.g.

..G..
.GgG.
GgGgG - 3-star
.GgG.
..G..

...g...
..gGg..
.gGgGg.
gGgGgGg - 4-star
.gGgGg.
..gGg..
...g...

so for each N-star, how many grids are we dealing with, in total and in terms of
the variant types?

1-star - 1 grid - variant types 1,0 (we'll call the central one first type G, so G,g)
2-star - 5 grids - 1,4
3-star - 13 grids - 9,4
4-star - 25 grids - 9,16

N^2 + (N-1)^2 is the formula for the total number of grids
1 + 0 = 1
4 + 1 = 5
9 + 4 = 13
16 + 9 = 25

The arrangement of variant types is an odd/even thing - for 1-star and 3-star,
the N^2 is the first in the G,g arrangement; for 2-star and 4-star it's the
second.

We're dealing with a 202301-star - so that's odd so N^2 is first:

40925694601,40925290000 for G,g

But while we're dealing with a 202301-star, those final grids at the furthest
reaches are not entirely filled in - refer back to this from earlier:

 mNo
mM Oo
W S E
rR Tt
 rSt

it's grids S and neighbouring ones that are totally filled in - the others like
W, m, M, etc. are partial e.g.:

+---+---+---+
|   |   | O |
|   |   |O.O|
|   |  O|   |
+---+---+---+
|   | O |
|   |O  |
|  O|   |
+---+---+
| O |
|O  |
| O |
+---+---+ etc

so we've got a totally filled 202300-star of grids, followed by:

1 * West-most grid
x * M well-filled (~7/8) NW type grids
y * m partly-filled (~1/8) NW type grids

...and then the same for North-most, O and o
...and then the same for East-most, T and t
...and then the same for South-most, R and r

We need to calculate x and y.

Assume we have a 4-star totally filled in set of grids:

.........
....g....
...gGg...
..gGgGg..
.gGgGgGg. - 4-star
..gGgGg..
...gGg...
....g....
.........

then we extend to include NSEW

....N....
....g....
...gGg...
..gGgGg..
WgGgGgGgE - 4-star
..gGgGg..
...gGg...
....g....
....S....

then all the extras:

...mNo...
..mMgOo..
.mMgGgOo.
mMgGgGgOo
WgGgGgGgE - 4-star
rRgGgGgTt
.rRgGgTt.
..rRgTt..
...rSt...

that's 4 lower cases of each and 3 upper cases of each

so if we start with our 202300-star totally filled in set of grids, we now have
our x and y values:

1 * West-most, North, South and East grid
202299 * M well-filled (~7/8) NW type grids, and O, R and T
202300 * m partly-filled (~1/8) NW type grids, and o, r and t



The central grid, with "S", of type "G" is a special case as we start in the
middle but regardless of that, we can count how many Odd and Even reachable
spaces there are in it, and therefore all other type "G" grids:

Odd: 7442
Even: 7456

and so the reverse grid of type "g" would be the inverse of those two counts,
were every cell to have been reached.

So, from above:

40924885401,40925290000 in our G,g arrangement means:

40924885401 G-type grids, of Odd: 7442 (and Even: 7456)

40925290000 g-type grids, of 0dd: 7456 (and Even: 7442)



As we've done the filled-in grids, now we need to do the partially filled in
grids. There are quite a few types: 12 in total.

We'll need to know the starting ordinance (Odd or Even) for each of the
12, as we start from the various corners and edges.

Our G-type grids have Even at all the corners and mid-points of the edges; the
g-types are Odds at the corners, of course.

See step_counter_part2.py notes (at the end) for the contination, maths and
final answers.
"""
