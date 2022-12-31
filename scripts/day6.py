from os import stat
import re
from argparse import ArgumentParser
from collections import defaultdict, deque

import numpy as np

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay6(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=6, test=test)

    def part1(self):
        with open(self.filename, "r") as f:
            all_lines = f.readlines()
            st = all_lines[0].strip()
            for i in range(len(st)):
                s = set(list(st[i : i + 4]))
                if len(s) == 4:
                    return i + 4

    def part2(self):
        with open(self.filename, "r") as f:
            all_lines = f.readlines()
            st = all_lines[0].strip()
            for i in range(len(st) - 14):
                s = set(list(st[i : i + 14]))
                if len(s) == 14:
                    return i + 14


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

    print(f"Test mode: {args.test}")

    day = AdventDay6(test=args.test)

    print(day.solve())
