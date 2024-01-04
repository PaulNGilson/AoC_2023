import re
import math
from itertools import combinations
import sympy as sym

real_data = True

if real_data:
    file = open("input.txt", "r")
    test_area = (200000000000000, 400000000000000)
else:
    file = open("input_test.txt", "r")
    test_area = (7, 27)
data_raw = file.readlines()
file.close()
data = []
for line in data_raw:
    data.append(line.strip())

def line_crossing(line1, line2):
    if line1.m == line2.m:
        return None, None, False # parallel
    else: # return the coordinates x, y where the crossing occurs; ref. https://www.ncl.ac.uk/webtemplate/ask-assets/external/maths-resources/core-mathematics/geometry/equation-of-a-straight-line.html
        x = ((-line2.m * line2.x) + (line2.y) + (line1.m * line1.x) - (line1.y)) / (line1.m - line2.m)
        y = (line1.m * x) - (line1.m * line1.x) + line1.y
        return x, y, True

def time_of_crossing(line, x, y):
    if math.copysign(1, x - line.x) == math.copysign(1, line.dx) and \
        math.copysign(1, y - line.y) == math.copysign(1, line.dy):
        return "future"
    else:
        return "past"

class Line:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = int(x)
        self.y = int(y)
        self.z = int(z)
        self.dx = int(dx)
        self.dy = int(dy)
        self.dz = int(dz)
        self.m = self.dy/self.dx # gradient
    def print_me(self): # for simple debugging, where needed
        return f"Hailstone: {self.x}, {self.y}, {self.x}"

lines = []

for line in data:
    matches = re.search(r'([0-9]+),\s+([0-9]+),\s+([0-9]+)\s+\@\s+(\-?[0-9]+),\s+(\-?[0-9]+),\s+(-?[0-9]+).*', line)
    l = Line(*matches.groups())
    lines.append(l)

count_crossed_in_test_area = 0

for line1, line2 in list(combinations(lines, 2)):
    xcross, ycross, crossed = line_crossing(line1, line2)
    if crossed:
        cross_in_future_line1 = time_of_crossing(line1, xcross, ycross)
        cross_in_future_line2 = time_of_crossing(line2, xcross, ycross)
        if cross_in_future_line1 == "past" or cross_in_future_line2 == "past":
            #print(f"crossed in the past ({cross_in_future_line1}, {cross_in_future_line2})")
            pass
        elif test_area[0] <= xcross and xcross <= test_area[1] and test_area[0] <= ycross and ycross <= test_area[1]:
            #print(line1.print_me(), line2.print_me(), "crossing in test area")
            count_crossed_in_test_area += 1
        else:
            #print("crossing, but not in test area")
            pass
    else:
        #print("lines do not cross - are parallel", line1.print_me(), line2.print_me())
        pass

print("part 1:", count_crossed_in_test_area)

# part 2 begins

"""
choose an arbitrary set of hailstones - we only need three, as they give 3
equations each and we have 9 variables to solve (hence only need 9 equations):

a, b, c       - time taken until our rock "r" hits each of the three hailstones
xdr, ydr, zdr - the velocity of "r" along x, y and z axes (the difference each nanosecond)
xr, yr, zr    - the starting x, y and z of our "r"

71898010551246, 245090708552712, 99396786646740 @ 255, 110, 249
306861200731124, 119442226206543, 266670878852462 @ 116, 88, 55
110737258321423, 163146345364483, 224384576660159 @ 280, 201, 92

These hailstone values are what we'll briefly call:
x, y, z @ xd, yd, zd

Each hailstone has the same equation, for whichever axis - let's look at x, to
see where our rock "r" collides with an arbitrary hailstone:

(time * xd) + x = (time * xdr) + xr
 or
time * (xd - xdr) = xr - x
 which is
time * xd - time * xdr = xr - x

So we can create 9 equations and pass these into sympy
https://docs.sympy.org/latest/index.html
"""

# define our unknowns
a,b,c,xdr,ydr,zdr,xr,yr,zr = sym.symbols('a,b,c,xdr,ydr,zdr,xr,yr,zr')

# create the 9 equations - 3 for each hailstone, as above
eq1 = sym.Eq(a*255 - a*xdr, xr - 71898010551246)
eq2 = sym.Eq(a*110 - a*ydr, yr - 245090708552712)
eq3 = sym.Eq(a*249 - a*zdr, zr - 99396786646740)
eq4 = sym.Eq(b*116 - b*xdr, xr - 306861200731124)
eq5 = sym.Eq(b*88 - b*ydr, yr - 119442226206543)
eq6 = sym.Eq(b*55 - b*zdr, zr - 266670878852462)
eq7 = sym.Eq(c*280 - c*xdr, xr - 110737258321423)
eq8 = sym.Eq(c*201 - c*ydr, yr - 163146345364483)
eq9 = sym.Eq(c*92 - c*zdr, zr - 224384576660159)

_,_,_,_,_,_,rock_x,rock_y,rock_z = sym.solve([eq1,eq2,eq3,eq4,eq5,eq6,eq7,eq8,eq9],(a,b,c,xdr,ydr,zdr,xr,yr,zr))[0]

print("part 2:", sum([rock_x, rock_y, rock_z]))
