# Advent of Code 2023

My attempt at the 25*2 challenges from the [2023 Advent of
Code](https://adventofcode.com/2023) challenge.

I'd like to repeat what I managed last year, so here are essentially the same
aims I had last time:

* No help from friends/colleagues/Reddit/etc. - I need to work out a solution on
  my own to all the challenges.
* I can do any _non-Advent of Code_ research I like, from looking up potential
  algorithms, studying bits of mathematics, snippets from Stack Overflow, etc.
* No AI.

...and one more for fun (although if last year is any indication, this will fall
apart in week 3!):

* Final solutions should run in sub-15s.

| Days | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|-|-|-|-|-|-|-|-|-|-|-|-|-|-|
| Stars | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: |
| Time | 50 | 51 | 72 | 49 | 37 | 6706 | 46 | 293 | 40 | 6520 | 770 | 33m 03s | 64 |

| Days | 14 | 15 | 16 | 17 | 18 | 19 | 20 | 21 | 22 | 23 | 24 | 25 |
|-|-|-|-|-|-|-|-|-|-|-|-|-|
| Stars | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: | :star2: |
| Time | 610 | 51 | 3425 | 19m 46s | 53 | 78 | 253 | 245 | 1338 | 31899 | 372 | 3360 |

:star: means just the first star, :star2: means both stars, and :custard: (just
because "custard" showed up while searching for emojis with "star" in the name)
means no stars and the day is in the past. I suspect I'll be very behind the
daily-rate, as the days get busier through December...

Times to run are just one example run, in milliseconds (unless specified
otherwise).

## Updates

After completing the challenges, I went back through them (particularly those
running slowly or just of general interest in other approaches) with some notes
below:

* Day 12: with memoization, and converting all these input lists to tuples, my
  code runs in 8m 06s - still not "fast" but does show the benefit of
  memoization even in code that's not especially well-optimised.
