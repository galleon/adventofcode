#!/bin/python3

import re
import sys
import time

from collections import defaultdict, Counter

from z3 import *

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/23"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/23_test"

directions = {
    "N": (0, -1),
    "S": (0, 1),
    "E": (1, 0),
    "W": (-1, 0),
    "NE": (1, -1),
    "NW": (-1, -1),
    "SE": (1, 1),
    "SW": (-1, 1),
}

look_at = {
    "N": {"NW", "N", "NE"},
    "S": {"SW", "S", "SE"},
    "E": {"NE", "E", "SE"},
    "W": {"NW", "W", "SW"},
}

considered = ["N", "S", "W", "E"]

signs = {(0, -1): "^", (0, 1): "v", (1, 0): ">", (-1, 0): "<"}


def show(elves):
    minx = min(x for x, y in elves)
    maxx = max(x for x, y in elves)
    miny = min(y for x, y in elves)
    maxy = max(y for x, y in elves)

    for y in range(miny, maxy + 1):
        print("".join("#" if (x, y) in elves else "." for x in range(minx, maxx + 1)))
    print()


def show_directions(elves, where):
    minx = min(x for x, y in elves)
    maxx = max(x for x, y in elves)
    miny = min(y for x, y in elves)
    maxy = max(y for x, y in elves)

    for y in range(miny, maxy + 1):
        for x in range(minx, maxx + 1):
            if (x, y) in where.keys():

                to = where[x, y]
                dx = to[0] - x
                dy = to[1] - y

                assert (
                    (dx == 0 and dy == 1)
                    or (dx == 0 and dy == -1)
                    or (dx == 1 and dy == 0)
                    or (dx == -1 and dy == 0)
                )

                print(signs[to[0] - x, to[1] - y], end="")
            else:
                if (x, y) in elves:
                    print("#", end="")
                else:
                    print(".", end="")
        print()


def solve():
    print(f"Using file {FILE}")
    elves = set()
    blocks = open(FILE).read().split("\n\n")
    for y, line in enumerate(blocks[0].splitlines(), start=0):
        for x, c in enumerate(line, start=0):
            if c in "#":
                elves.add((x, y))

    show(elves)

    def part1(elves):
        r = 0
        moving = True

        while moving:
            moving = False

            # Shall we move?
            shall_move = set()
            for x, y in elves:
                for d in directions:
                    _x, _y = x + directions[d][0], y + directions[d][1]
                    if (_x, _y) in elves:
                        shall_move.add((x, y))
                        break

            if not shall_move:
                print("No more move")
                return r

            where = {}
            for x, y in shall_move:
                for i in range(4):
                    dir = considered[(i + r) % 4]
                    can_move = True
                    for d in look_at[dir]:
                        _x, _y = x + directions[d][0], y + directions[d][1]
                        if (_x, _y) in elves:
                            can_move = False
                            break
                    if can_move and (x, y) not in where:
                        where[(x, y)] = (
                            x + directions[dir][0],
                            y + directions[dir][1],
                        )
                        break

            c = Counter(where.values())

            new_elves = set()

            # show_directions(elves, where)

            for x, y in elves:
                if (x, y) in where and c[where[x, y]] == 1:
                    moving = True
                    new_elves.add(where[x, y])
                else:
                    new_elves.add((x, y))

            elves = new_elves

            dx = max(x for x, y in elves) - min(x for x, y in elves) + 1
            dy = max(y for x, y in elves) - min(y for x, y in elves) + 1

            r += 1

            # print(f"== End of Round {r} ==")
            # show(elves)

            if r > 9:
                break

        return dx * dy - len(elves)

    def part2(elves):
        r = 0
        moving = True

        while moving:
            moving = False

            # Shall we move?
            shall_move = set()
            for x, y in elves:
                for d in directions:
                    _x, _y = x + directions[d][0], y + directions[d][1]
                    if (_x, _y) in elves:
                        shall_move.add((x, y))
                        break

            if not shall_move:
                print("No more move")
                return r + 1

            where = {}
            for x, y in shall_move:
                for i in range(4):
                    dir = considered[(i + r) % 4]
                    can_move = True
                    for d in look_at[dir]:
                        _x, _y = x + directions[d][0], y + directions[d][1]
                        if (_x, _y) in elves:
                            can_move = False
                            break
                    if can_move and (x, y) not in where:
                        where[(x, y)] = (
                            x + directions[dir][0],
                            y + directions[dir][1],
                        )
                        break

            c = Counter(where.values())

            new_elves = set()

            # show_directions(elves, where)

            for x, y in elves:
                if (x, y) in where and c[where[x, y]] == 1:
                    moving = True
                    new_elves.add(where[x, y])
                else:
                    new_elves.add((x, y))

            elves = new_elves

            dx = max(x for x, y in elves) - min(x for x, y in elves) + 1
            dy = max(y for x, y in elves) - min(y for x, y in elves) + 1

            r += 1

            # print(f"== End of Round {r} ==")
            # show(elves)

            # if r > 9:
            #    break

    ti = time.time()
    print(f"Part one: {part1(elves)}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(elves)}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
