#!/bin/python3

import re
import sys
import time

from z3 import *

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/22"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/22_test"

signe = {(-1, 0): "<", (1, 0): ">", (0, -1): "^", (0, 1): "v"}
value = {"<": 2, ">": 0, "^": 3, "v": 1}


def solve():
    print(f"Using file {FILE}")
    grid, instructions, start = {}, None, None
    blocks = open(FILE).read().split("\n\n")
    for y, line in enumerate(blocks[0].splitlines(), start=1):
        for x, c in enumerate(line, start=1):
            if c in ".#":
                if start is None:
                    start = (x, y)
                grid[x, y] = c

    instructions = re.findall(r"\d+|\D+", blocks[1].strip())

    def part1(grid, instructions, start):
        # initial conditions
        x, y = start
        dx, dy = 1, 0

        for inst in instructions:
            print(inst)

            if inst == "R":
                dy, dx = dx, -dy
            elif inst == "L":
                dx, dy = dy, -dx
            else:
                for _ in range(int(inst)):
                    x_, y_ = x + dx, y + dy
                    cell = grid.get((x_, y_))
                    if cell is None:
                        # WRAP
                        x__, y__ = x, y
                        while (x__, y__) in grid:
                            x_, y_ = x__, y__
                            x__ -= dx
                            y__ -= dy
                        cell = grid[x_, y_]
                    if cell == "#":
                        break
                    x, y = x_, y_

        answer = 1000 * y + 4 * x + value[signe[dx, dy]]

        return answer

    def wrap3d(x, y, dx, dy):
        # Wrapping the cube manually !!!
        if dx == 1:
            # Right
            if x == 50:
                return 50 + (y - 150), 150, 0, -1
            if x == 100:
                if 51 <= y <= 100:
                    return 100 + (y - 50), 50, 0, -1
                if 101 <= y <= 150:
                    return 150, 51 - (y - 100), -1, 0
            if x == 150:
                return 100, 151 - y, -1, 0
        elif dx == -1:
            # Left
            if x == 1:
                if 101 <= y <= 150:
                    return 51, 1 + (150 - y), 1, 0
                if 151 <= y <= 200:
                    return y - 150 + 50, 1, 0, 1
            if x == 51:
                if 1 <= y <= 50:
                    return 1, 151 - y, 1, 0
                if 51 <= y <= 100:
                    return y - 50, 101, 0, 1
        elif dy == 1:
            # Down
            if y == 50:
                return 100, x - 50, -1, 0
            if y == 150:
                return 50, x + 100, -1, 0
            if y == 200:
                return x + 100, 1, 0, 1
        elif dy == -1:
            # Up
            if y == 1:
                if 51 <= x <= 100:
                    return 1, x + 100, 1, 0
                if 101 <= x <= 150:
                    return x - 100, 200, 0, -1
            if y == 101:
                return 51, x + 50, 1, 0

        raise Exception(f"WRAP ERROR - {x}, {y}, {dx}, {dy}")

    def part2(grid, instructions, start):
        # initial conditions
        x, y = start
        dx, dy = 1, 0

        for inst in instructions:
            if inst == "R":
                dx, dy = -dy, dx
            elif inst == "L":
                dx, dy = dy, -dx
            else:
                for _ in range(int(inst)):
                    x_, y_ = x + dx, y + dy
                    cell = grid.get((x_, y_))
                    if cell is None:
                        # WRAP
                        x_, y_, dx_, dy_ = wrap3d(x, y, dx, dy)

                        cell = grid[x_, y_]
                        if cell == "#":
                            break  # Hit a wall
                        x, y = x_, y_
                        dx, dy = dx_, dy_
                    elif cell == "#":
                        break  # Hit a wall
                    x, y = x_, y_
        print(x, y, dx, dy)

        answer = 1000 * y + 4 * x + value[signe[dx, dy]]

        return answer

    ti = time.time()
    print(f"Part one: {part1(grid, instructions, start)}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(grid, instructions, start)}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
