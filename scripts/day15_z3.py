import re
import time
from argparse import ArgumentParser
from collections import defaultdict

import portion as P
from z3 import Abs, And, Exists, ForAll, If, Implies, Int, Not, Or, Solver, sat, unsat, Ints

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay15(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=15, test=test)

    def load_input(self):
        print("Loading input...")
        outputs = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

            v = list()

            for line in lines:
                if line.strip():
                    tuples = re.findall(r"x=(-?\d+), y=(-?\d+)", line)
                    v.append([int(tuples[0][0]), int(tuples[0][1]), int(tuples[1][0]), int(tuples[1][1])])

            return v

    def part(self, v, y_target):
        ranges = P.empty()
        for sx, sy, bx, by in v:
            dist = abs(sx-bx) + abs(sy-by)
            if abs(y_target-sy) < dist:
                k = dist - abs(y_target-sy)
                ranges = ranges | P.closed(sx - k, sx + k)

        return ranges

    def part1(self):
        v = self.load_input()

        t1 = time.time()
        all = self.part(v, 2_000_000)

        result = all.upper - all.lower
        print(f"{result} in {time.time() - t1:.2f} seconds")
        return result

    def part2(self):
        v = self.load_input()

        t1 = time.time()

        solver = Solver()

        x, y = Ints('x y')

        distance_between = lambda sx, sy, bx, by: Abs(sx-bx) + Abs(sy-by)

        solver.add(x >= 0)
        solver.add(y >= 0)
        solver.add(x <= 4_000_000)
        solver.add(y <= 4_000_000)

        for sx, sy, bx, by in v:
            solver.add(Abs(sx-x) + Abs(sy-y) > distance_between(sx, sy, bx, by))

        check = solver.check()

        result = None
        if check == sat:
            m = solver.model() #.eval(x).as_long()*4_000_000 + solver.model().eval(y).as_long()

            result = m.eval(x).as_long()*4_000_000 + m.eval(y).as_long()

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
