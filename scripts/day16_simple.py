#!/bin/python3

import functools
import sys
import time

sys.setrecursionlimit(10000)

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/16"


def solve():
    print(f"Using file {FILE}")
    with open(FILE, "r", encoding="utf-8") as f:
        network = {}
        for line in f:
            line = line.strip().split(" ")
            name = line[1]
            rate = int(line[4].split("=")[-1].split(";")[0])
            valves = [word.split(",")[0] for word in line[9:]]

            network[name] = {"rate": rate, "valves": valves}

        @functools.cache
        def part1(opened, minutes, position):
            # The state is made of:
            # - the set of opened valves
            # - the number of minutes left
            # - the current valve (i.e. the one we are currently at)
            # The goal is to maximize the sum of the rates of the opened valves at the end of the time

            if minutes <= 0:
                return 0

            best = 0
            s = network[position]
            for valve in s["valves"]:
                best = max(best, part1(opened, minutes - 1, valve))

            if position not in opened and s["rate"] > 0 and minutes > 0:
                # defrost the set
                opened = set(opened)
                opened.add(position)
                minutes -= 1
                new_sum = minutes * s["rate"]

                for valve in s["valves"]:
                    best = max(
                        best,
                        new_sum + part1(frozenset(opened), minutes - 1, valve),
                    )

            return best

        @functools.cache
        def part2(opened, minutes, position):
            """
            TL;DR: Just do part one basically, then do it again once done to simulate the elephant.
            """

            if minutes <= 0:
                return part1(opened, 26, "AA")

            best = 0
            s = network[position]
            for valve in s["valves"]:
                best = max(best, part2(opened, minutes - 1, valve))

            if position not in opened and s["rate"] > 0 and minutes > 0:
                # defrost the set
                opened = set(opened)
                opened.add(position)
                minutes -= 1
                new_sum = minutes * s["rate"]

                for valve in s["valves"]:
                    best = max(
                        best,
                        new_sum + part2(frozenset(opened), minutes - 1, valve),
                    )

            return best

        ti = time.time()
        print(f"Part one: {part1(frozenset(), 30, 'AA')}")
        print(f"Time: {time.time() - ti:.2f}s")
        ti = time.time()
        print(f"Part two: {part2(frozenset(), 26, 'AA')}")
        print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
