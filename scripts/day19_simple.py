#!/bin/python3

import functools
import sys
import time

from collections import defaultdict

from collections import deque

import numpy as np

sys.setrecursionlimit(10000)

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/19"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/19_test"
#


def solve():
    print(f"Using file {FILE}")
    line = None

    with open(FILE, "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            lines.append(line.strip())

    blueprint = {}
    for i, line in enumerate(lines):
        blueprint_str, recipe = line.split(":")
        id = int(blueprint_str.split()[-1])
        robots = {}
        for part in recipe.strip().split("."):
            if part:
                item = part.split("robot costs")
                type = item[0].split()[-1]
                moneys = {}
                for part in item[1].split("and"):
                    pairs = part.split()
                    moneys[pairs[1].strip()] = int(pairs[0].strip())
                robots[type] = moneys

        blueprint[id] = robots

    def solve(OR_ore, CL_ore, OB_ore, OB_clay, GE_ore, GE_obsidian, time):
        best = 0
        # state is (qty_ore, qty_clay, qty_obsidian, qty_geodes, r_ore, r_clay, r_obsidian, r_geode, time)
        state = (0, 0, 0, 0, 1, 0, 0, 0, time)
        queue = set([state])
        visited = set()
        while queue:
            state = queue.pop()
            (
                qty_ore,
                qty_clay,
                qty_obsidian,
                qty_geode,
                r_ore,
                r_clay,
                r_obsidian,
                r_geode,
                time,
            ) = state

            best = max(best, qty_geode)
            if time == 0:
                continue

            max_ore = max([OR_ore, CL_ore, OB_ore, GE_ore])

            if r_ore >= max_ore:
                r_ore = max_ore
            if r_clay >= OB_clay:
                r_clay = OB_clay
            if r_obsidian >= GE_obsidian:
                r_obsidian = GE_obsidian
            if qty_ore >= time * max_ore - r_ore * (time - 1):
                qty_ore = time * max_ore - r_ore * (time - 1)
            if qty_clay >= time * OB_clay - r_clay * (time - 1):
                qty_clay = time * OB_clay - r_clay * (time - 1)
            if qty_obsidian >= time * GE_obsidian - r_obsidian * (time - 1):
                qty_obsidian = time * GE_obsidian - r_obsidian * (time - 1)

            state = (
                qty_ore,
                qty_clay,
                qty_obsidian,
                qty_geode,
                r_ore,
                r_clay,
                r_obsidian,
                r_geode,
                time,
            )

            if state in visited:
                continue
            visited.add(state)

            queue.add(
                (
                    qty_ore + r_ore,
                    qty_clay + r_clay,
                    qty_obsidian + r_obsidian,
                    qty_geode + r_geode,
                    r_ore,
                    r_clay,
                    r_obsidian,
                    r_geode,
                    time - 1,
                )
            )

            if qty_ore >= OR_ore:
                # Buy ore robot
                queue.add(
                    (
                        qty_ore - OR_ore + r_ore,
                        qty_clay + r_clay,
                        qty_obsidian + r_obsidian,
                        qty_geode + r_geode,
                        r_ore + 1,
                        r_clay,
                        r_obsidian,
                        r_geode,
                        time - 1,
                    )
                )
            if qty_ore >= CL_ore:
                # Buy clay robot
                queue.add(
                    (
                        qty_ore - CL_ore + r_ore,
                        qty_clay + r_clay,
                        qty_obsidian + r_obsidian,
                        qty_geode + r_geode,
                        r_ore,
                        r_clay + 1,
                        r_obsidian,
                        r_geode,
                        time - 1,
                    )
                )
            if qty_ore >= OB_ore and qty_clay >= OB_clay:
                # Buy obsidian robot
                queue.add(
                    (
                        qty_ore - OB_ore + r_ore,
                        qty_clay - OB_clay + r_clay,
                        qty_obsidian + r_obsidian,
                        qty_geode + r_geode,
                        r_ore,
                        r_clay,
                        r_obsidian + 1,
                        r_geode,
                        time - 1,
                    )
                )
            if qty_ore >= GE_ore and qty_obsidian >= GE_obsidian:
                # buy geode robot
                queue.add(
                    (
                        qty_ore - GE_ore + r_ore,
                        qty_clay + r_clay,
                        qty_obsidian - GE_obsidian + r_obsidian,
                        qty_geode + r_geode,
                        r_ore,
                        r_clay,
                        r_obsidian,
                        r_geode + 1,
                        time - 1,
                    )
                )
        return best

    def part1():
        # Initial conditions
        # costs = [[Int(f"v_{i}_{r}_{t}") for i, _ in enumerate(blueprint.keys())] for timein range(24)]
        # for time in range(24):

        p1 = 0

        for i in range(1, len(lines) + 1):
            b = solve(
                blueprint[i]["ore"]["ore"],
                blueprint[i]["clay"]["ore"],
                blueprint[i]["obsidian"]["ore"],
                blueprint[i]["obsidian"]["clay"],
                blueprint[i]["geode"]["ore"],
                blueprint[i]["geode"]["obsidian"],
                24,
            )
            p1 += i * b

        print(p1)

        return p1

    def part1_z3():
        # Initial conditions
        # costs = [[Int(f"v_{i}_{r}_{t}") for i, _ in enumerate(blueprint.keys())] for timein range(24)]
        # for time in range(24):

        p1 = 0

        s = Solver()
        geode = []
        for recipe in blueprint.keys():
            geode.append(Int(f"geode_{recipe}"))
            s.add(geode[-1] >= 0)

        for m in range(24):
            s.add(geode[0] == m)
            for i in range(1, len(lines) + 1):
                s.add(
                    geode[i]
                    == geode[i - 1] * blueprint[i]["geode"]["obsidian"]
                    + geode[i - 1] * blueprint[i]["geode"]["ore"]
                )
            s.add(geode[-1] >= 0)
            if s.check() == sat:
                m = s.model()
                p1 += m[geode[-1]].as_long()
            else:
                break
            s.pop()

        # for i in range(1, len(lines) + 1):
        #     b = solve(
        #         blueprint[i]["ore"]["ore"],
        #         blueprint[i]["clay"]["ore"],
        #         blueprint[i]["obsidian"]["ore"],
        #         blueprint[i]["obsidian"]["clay"],
        #         blueprint[i]["geode"]["ore"],
        #         blueprint[i]["geode"]["obsidian"],
        #         24,
        #     )
        #     p1 += i * b

        print(p1)

        return p1

    def part2():
        p2 = 1
        for i in range(1, 4):
            b = solve(
                blueprint[i]["ore"]["ore"],
                blueprint[i]["clay"]["ore"],
                blueprint[i]["obsidian"]["ore"],
                blueprint[i]["obsidian"]["clay"],
                blueprint[i]["geode"]["ore"],
                blueprint[i]["geode"]["obsidian"],
                32,
            )
            p2 *= b

        print(p2)
        return p2

    ti = time.time()
    print(f"Part one: {part1()}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2()}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
