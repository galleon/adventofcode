#!/bin/python3

import sys
import time

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/25"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/25_test"

snafu2base = {"=": -2, "-": -1, "0": 0, "1": 1, "2": 2}

base2snafu = {v: k for k, v in snafu2base.items()}


def solve():
    print(f"Using file {FILE}")
    blocks = open(FILE).read().split("\n\n")

    lines = blocks[0].splitlines()

    def part1(lines):
        result = 0
        for y, line in enumerate(lines, start=0):
            l = len(line)
            x = 0
            for i, d in enumerate(line, start=0):
                x += 5 ** (l - i - 1) * snafu2base[d]
            result += x

        base5_number = ""
        while result > 0:
            remainder = result % 5
            result = result // 5
            if remainder > 2:
                result += 1
                remainder -= 5
            base5_number = base2snafu[remainder] + base5_number

        return base5_number

    def part2(lines):
        return 0

    ti = time.time()
    print(f"Part one: {part1(lines)}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(lines)}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
