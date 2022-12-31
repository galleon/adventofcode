import operator
import re
from argparse import ArgumentParser
from collections import defaultdict
from sys import maxsize as MAX_SIZE

import numpy as np

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay10(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=10, test=test)

    def load_input(self):
        print("Loading input...")
        outputs = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

            for line in lines:
                outputs.append(line.strip())

            return outputs

    def cycle(self):
        self.iter += 1
        if self.iter == self.p:
            # Start with 20 and then move by 40
            self.p += 40
            self.result += self.x * self.iter

        if abs((self.iter - 1) % 40 - self.x) < 2:
            self.screen[(self.iter - 1) // 40][(self.iter - 1) % 40] = "#"

    def part1(self):
        lines = self.load_input()

        # period is 20 initially, then 40, then 60, etc.
        self.p = 20
        self.x = 1
        self.iter = 0
        self.result = 0

        self.screen = [[" " for x in range(40)] for y in range(6)]

        for line in lines:
            l = line.strip()

            if l.startswith("noop"):
                self.cycle()
            else:
                _, n = l.split()
                self.cycle()
                self.cycle()
                self.x = self.x + int(n)

        return self.result

    def part2(self):
        lines = self.load_input()

        self.p = 20
        self.x = 1
        self.iter = 0
        self.result = 0

        self.screen = [[" " for x in range(40)] for y in range(6)]

        for line in lines:
            l = line.strip()

            if l.startswith("noop"):
                self.cycle()
            else:
                _, n = l.split()
                self.cycle()
                self.cycle()
                self.x = self.x + int(n)

        display = ""
        for line in self.screen:
            display += "".join(line) + "\n"

        print(display)

        return self.result


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

    day = AdventDay10(test=args.test)

    print(day.solve())
