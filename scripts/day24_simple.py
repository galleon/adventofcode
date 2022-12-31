#!/bin/python3

import re
import sys
import time
from collections import defaultdict

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/24"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/24_test"

translations = {
    "^": complex(0, -1),  # MOVE UP
    "v": complex(0, 1),  # MOVE DOWN
    ">": complex(1, 0),  # MOVE RIGHT
    "<": complex(-1, 0),  # MOVE LEFT
}

possible_moves = [
    complex(0, -1),  # MOVE DOWN
    complex(0, 1),  # MOVE UP
    complex(1, 0),  # MOVE RIGHT
    complex(-1, 0),  # MOVE LEFT
    complex(0, 0),  # WAIT
]


def show(blizzards, w, h, start, exit_):
    inverse_translations = {v: k for k, v in translations.items()}

    s = []
    for y in range(-1, h + 1, 1):
        for x in range(-1, w + 1, 1):
            z = complex(x, y)
            if z == start:
                s.append("E")
            elif z == exit_:
                s.append("S")
            elif z in blizzards:
                if len(blizzards[z]) > 1:
                    s.append(f"{len(blizzards[z])}")
                else:
                    s.append(inverse_translations[blizzards[z][0]])
            elif x == -1 or y == -1 or x == w or y == h:
                s.append("#")
            else:
                s.append(".")
        s.append("\n")
    s.append("\n")

    return "".join(s)


def cplx2tuple(c):
    return (int(c.real), int(c.imag))


def is_inside(pos, w, h, start, exit_):
    if pos == exit_ or pos == start:
        return True

    x, y = cplx2tuple(pos)

    return x in range(w) and y in range(h)


def conservation_law(x, w, h):
    return complex(int(x.real) % w, int(x.imag) % h)


def step_blizzards(blizzards, w, h, start, exit_):
    new_blizzards = defaultdict(list)
    for y in range(h):
        for x in range(w):
            z = complex(x, y)
            if z in blizzards:
                for b in blizzards[z]:
                    new_blizzards[conservation_law(z + b, w, h)].append(b)

    return new_blizzards


def solve():
    print(f"Using file {FILE}")
    blizzards = defaultdict(list)
    blocks = open(FILE).read().split("\n\n")
    start, exit_ = None, None

    lines = blocks[0].splitlines()

    w = len(lines[0]) - 2
    h = len(lines) - 2

    for y, line in enumerate(lines, start=0):
        for x, c in enumerate(line, start=0):
            if c in "><^v#.":
                if c == ".":
                    if start is None:
                        start = complex(x - 1, y - 1)
                    else:
                        exit_ = complex(x - 1, y - 1)
                elif c in "><^v":
                    blizzards[complex(x - 1, y - 1)].append(translations[c])
            else:
                raise ValueError(f"Unknown character {c}")

    print(f"Map size: {w}x{h} (start: {start}, exit: {exit_})")

    def part1(blizzards, w, h, start, exit_):
        queue = set([start])

        t = 0
        while True:
            t += 1
            blizzards = step_blizzards(blizzards, w, h, start, exit_)

            candidates = {z + m for z in queue for m in possible_moves}
            # Are we done ?
            if exit_ in candidates:
                return t, blizzards

            # candidates shall be inside the map and not on a blizzard
            candidates = list(
                filter(
                    lambda z: is_inside(z, w, h, start, exit_) and z not in blizzards,
                    candidates,
                )
            )
            queue = set(candidates)

    def part2(blizzards, w, h, start, exit_):
        s1, blizzards = part1(blizzards, w, h, start, exit_)
        s2, blizzards = part1(blizzards, w, h, exit_, start)
        s3, blizzards = part1(blizzards, w, h, start, exit_)
        return s1 + s2 + s3, blizzards

    ti = time.time()
    print(f"Part one: {part1(blizzards, w, h, start, exit_)[0]}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(blizzards, w, h, start, exit_)[0]}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
