#!/bin/python3

import functools
import sys
import time

import numpy as np

sys.setrecursionlimit(10000)

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/17"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/17_pierre"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/17_test"
#


def solve():
    print(f"Using file {FILE}")
    line = None
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()

    print(len(line))

    def get_rock(type, height):
        if type == 0:
            return {(2, height), (3, height), (4, height), (5, height)}
        elif type == 1:
            return {
                (3, height),
                (2, height + 1),
                (3, height + 1),
                (4, height + 1),
                (3, height + 2),
            }
        elif type == 2:
            return {
                (4, height),
                (3, height),
                (2, height),
                (4, height + 1),
                (4, height + 2),
            }
        elif type == 3:
            return {
                (2, height),
                (2, height + 1),
                (2, height + 2),
                (2, height + 3),
            }
        elif type == 4:
            return {(2, height), (3, height), (2, height + 1), (3, height + 1)}
        else:
            raise ValueError(f"Unknown type {type}")

    def move_l(rock):
        if any(x == 0 for x, y in rock):
            return rock
        else:
            return {(x - 1, y) for x, y in rock}

    def move_r(rock):
        if any(x == 6 for x, y in rock):
            return rock
        else:
            return {(x + 1, y) for x, y in rock}

    def fall(rock):
        return {(x, y - 1) for x, y in rock}

    def elevate(rock):
        return {(x, y + 1) for x, y in rock}

    def display_top(tower, lines=10):
        t = max(y for x, y in tower)
        for i in range(lines):
            print("".join("#" if (x, t - i) in tower else "." for x in range(7)))

    @functools.cache
    def part1(line):
        # Initial conditions
        top = 0
        rock_type = 0

        tower = {(x, top) for y in range(7) for x in range(7)}
        i = 0
        rock_number = 0

        while rock_number < 2022:
            rock = get_rock(rock_number % 5, top + 4)

            landed = False
            while not landed:
                move = line[i]
                i = (i + 1) % len(line)

                if move == ">":
                    rock = move_r(rock)
                    if tower & rock:
                        rock = move_l(rock)

                else:
                    rock = move_l(rock)
                    if tower & rock:
                        rock = move_r(rock)

                rock = fall(rock)
                if tower & rock:
                    rock = elevate(rock)
                    tower |= rock

                    top = max(y for x, y in tower)

                    landed = True
                    # Debub Pilou !
                    # if rock_number == 24:
                    #     display_top(tower, 50)
                    #     break

            rock_number += 1
        return top

    def signature(tower, sh):
        top_ = max(y for x, y in tower)
        return frozenset({(x, top_ - y) for x, y in tower if top_ - y < sh})

    def part2(line):
        # Initial conditions
        top = 0

        tower = {(x, top) for y in range(7) for x in range(7)}
        position = 0
        rock_number = 0

        patterns = {}
        added = 0

        target = 1_000_000_000_000

        signature_height = 5

        while rock_number < target:
            rock = get_rock(rock_number % 5, top + 4)

            landed = False
            while not landed:
                move = line[position]
                position = (position + 1) % len(line)

                if move == ">":
                    rock = move_r(rock)
                    if tower & rock:
                        rock = move_l(rock)
                else:
                    rock = move_l(rock)
                    if tower & rock:
                        rock = move_r(rock)

                rock = fall(rock)
                if tower & rock:
                    rock = elevate(rock)
                    tower |= rock

                    top = max(y for x, y in tower)

                    landed = True

                    key = (
                        position,
                        rock_number % 5,
                    )

                    # 2022 = 2 * 3 * 337
                    # 2023 = 7 * 17 ^ 2

                    if key in patterns and rock_number > 2022:
                        # print(f"Found a pattern at {rock_number}: {key}")

                        # Get as close as possible to target
                        previous_rock_number, previous_top = patterns[key]

                        delta_top = top - previous_top
                        delta_rock_number = rock_number - previous_rock_number

                        nitem = (target - rock_number) // delta_rock_number

                        added += nitem * delta_top
                        rock_number += nitem * delta_rock_number

                    patterns[key] = (rock_number, top)
                    break

            rock_number += 1

        return top + added

    def part2_test(line):
        # Initial conditions
        top = 0
        rock_type = 0

        tower = {(x, top) for y in range(7) for x in range(7)}
        i = 0
        rock_number = 0

        target = 1_000_000_000_000

        number_of_times = target % (5 * len(line))
        target_i = number_of_times % len(line)
        target_t = number_of_times % 5

        patterns = {}

        y_bottom = 0

        max_tower_size = 0

        while rock_number < 5 * len(line):
            if rock_number % 10_000 == 0 or rock_number > 50_000:
                print(rock_number, 5 * len(line))
            rock = get_rock(rock_number % 5, top + 4)

            landed = False
            while not landed:
                move = line[i]
                i = (i + 1) % len(line)

                if move == ">":
                    rock = move_r(rock)
                    if tower & rock:
                        rock = move_l(rock)
                else:
                    rock = move_l(rock)
                    if tower & rock:
                        rock = move_r(rock)

                rock = fall(rock)

                key = (rock_number % 5, i)

                # If rock & tower collide
                if tower & rock:
                    # Move rock up
                    rock = elevate(rock)
                    # Merge rock & tower -> tower
                    tower |= rock
                    # Update top
                    top = max(y for x, y in tower)
                    # Mark rock as landed
                    landed = True

                    # Remove elements from tower
                    full_line = set()
                    y_limit = top
                    while y_limit > y_bottom and len(full_line) < 7:
                        full_line = {x for x, y in tower if y == y_limit}
                        y_limit -= 1

                    y_bottom = y_limit

                    if len(full_line) == 7:
                        reduced_tower = {(x, y) for x, y in tower if y > y_limit}
                        tower = reduced_tower
                        if len(tower) > max_tower_size:
                            max_tower_size = len(tower)

                if key in set([(target_t, target_i), (4, len(line) - 1)]):
                    # print("Found target", rock_number, top, number_of_times)
                    # return top * number_of_times + patterns[(target_t, target_i)]
                    patterns[key] = top

            rock_number += 1

        print(f"Max tower size: {max_tower_size}")
        print(f"Top for (4, len(line) - 1): {patterns[(4, len(line) - 1)]}")

        return top * number_of_times + patterns[(target_t, target_i)]

    def part2_ok(line):
        # Initial conditions
        top = 0

        tower = {(x, top) for y in range(7) for x in range(7)}
        position = 0
        rock_number = 0

        patterns = {}
        added = 0

        target = 1_000_000_000_000

        signature_height = 5

        while rock_number < target:
            rock = get_rock(rock_number % 5, top + 4)

            landed = False
            while not landed:
                move = line[position]
                position = (position + 1) % len(line)

                if move == ">":
                    rock = move_r(rock)
                    if tower & rock:
                        rock = move_l(rock)
                else:
                    rock = move_l(rock)
                    if tower & rock:
                        rock = move_r(rock)

                rock = fall(rock)
                if tower & rock:
                    rock = elevate(rock)
                    tower |= rock

                    top = max(y for x, y in tower)

                    landed = True

                    key = (
                        position,
                        rock_number % 5,
                        signature(tower, signature_height),
                    )

                    if rock_number > 2022 and key not in patterns:
                        assert (
                            False
                        ), "We have a problem bro - change your signature height"

                    if key in patterns and rock_number > 2022:
                        # Get as close as possible to target
                        previous_rock_number, previous_top = patterns[key]

                        delta_top = top - previous_top
                        delta_rock_number = rock_number - previous_rock_number

                        nitem = (target - rock_number) // delta_rock_number

                        added += nitem * delta_top
                        rock_number += nitem * delta_rock_number

                    patterns[key] = (rock_number, top)
                    break

            rock_number += 1

        print(f"{len(patterns)} patterns of height {signature_height} found")

        print(
            min(len(fs) for _, _, fs in patterns), max(len(fs) for _, _, fs in patterns)
        )

        return top + added

    ti = time.time()
    print(f"Part one: {part1(line)}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(line)}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
