from argparse import ArgumentParser
from collections import defaultdict

import time

import numpy as np

from aoc.common import AdventDay
from aoc.data import Board, Graph
from heapq import heappop, heappush

import re

import portion as P


class AdventDay15(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=15, test=test)

    def load_input(self):
        print("Loading input...")
        outputs = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

            sensors, beacons = list(), list()

            for line in lines:
                if line.strip():
                    tuples = re.findall(r"x=(-?\d+), y=(-?\d+)", line)
                    sensors.append((int(tuples[0][0]), int(tuples[0][1])))
                    beacons.append((int(tuples[1][0]), int(tuples[1][1])))

            return sensors, beacons

    def part(self, sensors, beacons, y_target):
        ranges = []
        for (sx, sy), (bx, by) in zip(sensors, beacons):
            dist = abs(sx - bx) + abs(sy - by)
            if abs(y_target - sy) < dist:
                k = dist - abs(y_target - sy)
                ranges.append(range(sx - k, sx + k + 1))

        ranges.sort(key=lambda x: x[0])

        # Merging overlaping ranges
        found_overlap = True
        while found_overlap:
            found_overlap = False
            for r1, r2 in zip(ranges, ranges[1:]):
                if set(r1) & set(r2):
                    union = set(r1) | set(r2)
                    ranges[ranges.index(r1)] = range(min(union), max(union) + 1)
                    ranges.pop(ranges.index(r2))
                    found_overlap = True
                if found_overlap:
                    break

        return ranges

    def part1(self):
        sensors, beacons = self.load_input()

        t1 = time.time()
        all = self.part(sensors, beacons, 2_000_000)

        result = sum(len(r) for r in all)

        print(f"{result} in {time.time() - t1:.2f} seconds")
        return result - 1

    def part2(self):
        sensors, beacons = self.load_input()

        t1 = time.time()
        y_target = 4_000_000

        r = range(0, y_target)

        result = set()
        for y in r:
            print(y)
            ranges = self.part(sensors, beacons, y)

            big_set = set(r)
            for rr in ranges:
                big_set = big_set - set(rr)

            if big_set:
                result = big_set.pop() * 4_000_000 + y
                break

        print(f"{result} in {time.time() - t1:.2f} seconds")
        return result


# define main
if __name__ == "__main__":
    # define the parser
    parser = ArgumentParser(description="First year Advent of Code")

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test",
        default=False,
        required=False,
    )

    args = parser.parse_args()

    day = AdventDay15(test=args.test)

    print(day.solve())
