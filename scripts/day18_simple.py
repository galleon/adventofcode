#!/bin/python3

import functools
import sys
import time

import numpy as np

sys.setrecursionlimit(10000)

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/18"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/18_test"
#


def solve():
    print(f"Using file {FILE}")
    line = None
    with open(FILE, "r", encoding="utf-8") as f:
        lines = []
        for line in f:
            line = line.strip()
            lines.append(list(map(int, line.split(","))))

    print(len(lines))

    def neighbors(x, y, z):
        return set(
            [
                (x + 1, y, z),
                (x - 1, y, z),
                (x, y + 1, z),
                (x, y - 1, z),
                (x, y, z + 1),
                (x, y, z - 1),
            ]
        )

    def part1():
        # Initial conditions
        all_cubes = [(x, y, z) for x, y, z in lines]
        print(
            max(x for x, y, z in all_cubes),
            max(y for x, y, z in all_cubes),
            max(z for x, y, z in all_cubes),
        )

        result = 0
        seen_cubes = set()
        # if a cube has a neighbor, touching faces will be seen twice (once from each cube)
        for cube in all_cubes:
            # all faces are visible
            result += 6
            # go through all neighbors and remove 2 if there is an intersection and the neighbor has been seen
            for neighbor in neighbors(*cube):
                if neighbor in seen_cubes:
                    result -= 2
            seen_cubes.add(cube)

        print(result)
        return result

    def part2():
        cubes = set([(x, y, z) for x, y, z in lines])

        maxx = max(x for x, y, z in cubes)
        maxy = max(y for x, y, z in cubes)
        maxz = max(z for x, y, z in cubes)
        print(maxx, maxy, maxz)

        # Take a bigger cube to make sure we know some points that are outside
        all_cubes = set(
            [
                (x, y, z)
                for x in range(maxx + 1)
                for y in range(maxy + 1)
                for z in range(maxz + 1)
            ]
        )

        spaces = all_cubes - cubes

        result = 0
        seen_cubes = set()
        # if a cube has a neighbor, touching faces will be seen twice (once from each cube)
        for cube in cubes:
            # all faces are visible
            result += 6
            # go through all neighbors and remove 2 if there is an intersection and the neighbor has been seen
            for neighbor in neighbors(*cube):
                if neighbor in seen_cubes:
                    result -= 2
            seen_cubes.add(cube)

        assert cubes == seen_cubes

        # Find only internal spaces
        external = (-1, -1, -1)
        spaces.add(external)
        queue = [external]  # <- we know this point is outside
        # Iterate over all spaces al remove external ones from the set
        while queue:
            space = queue.pop()
            if space in spaces:
                spaces.remove(space)
                queue.extend(neighbors(*space))

        # Remove faces that see a cube or a space
        for space in spaces:
            result += 6
            for neighbor in neighbors(*space):
                if neighbor in seen_cubes:
                    result -= 2
            seen_cubes.add(space)

        print(result)

        return result

    ti = time.time()
    print(f"Part one: {part1()}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2()}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
