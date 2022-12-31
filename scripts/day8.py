import operator
import re
from argparse import ArgumentParser
from collections import defaultdict
from os import O_TRUNC, stat
from sys import maxsize as MAX_SIZE

import numpy as np
from dotenv.main import load_dotenv

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay8(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=8, test=test)

    def load_input(self):
        print("Loading input...")
        lines = []
        with open(self.filename, "r") as f:
            for line in f.readlines():
                lines.append(list(map(lambda x: int(x), list(line.strip()))))
        return lines

    def part1(self):
        b = self.load_input()

        nrow = len(b)
        ncol = len(b[0])

        print(nrow, ncol)

        count = 0
        for j in range(1, nrow - 1):
            for i in range(1, ncol - 1):
                if (
                    b[j][i] > max([b[j][ii] for ii in range(i)])
                    or b[j][i] > max([b[j][ii] for ii in range(i + 1, ncol)])
                    or b[j][i] > max([b[jj][i] for jj in range(j)])
                    or b[j][i] > max([b[jj][i] for jj in range(j + 1, nrow)])
                ):
                    count += 1
        return count + 2 * (nrow + ncol) - 4

    def part2(self):
        b = self.load_input()
        nrow = len(b)
        ncol = len(b[0])

        print(nrow, ncol)

        best_scenic_score = 0
        for j in range(1, nrow - 1):
            for i in range(1, ncol - 1):
                v1 = [b[j][ii] for ii in range(i - 1, -1, -1)]
                v2 = [b[j][ii] for ii in range(i + 1, ncol)]
                v3 = [b[jj][i] for jj in range(j - 1, -1, -1)]
                v4 = [b[jj][i] for jj in range(j + 1, nrow)]

                i1 = next((index for index, x in enumerate(v1) if x >= b[j][i]), None)
                i2 = next((index for index, x in enumerate(v2) if x >= b[j][i]), None)
                i3 = next((index for index, x in enumerate(v3) if x >= b[j][i]), None)
                i4 = next((index for index, x in enumerate(v4) if x >= b[j][i]), None)

                scenic_score = (
                    (len(v1) if i1 is None else i1 + 1)
                    * (len(v2) if i2 is None else i2 + 1)
                    * (len(v3) if i3 is None else i3 + 1)
                    * (len(v4) if i4 is None else i4 + 1)
                )

                if scenic_score > best_scenic_score:
                    best_scenic_score = scenic_score

        return best_scenic_score


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

    day = AdventDay8(test=args.test)

    print(day.solve())
