import re
from argparse import ArgumentParser
from collections import defaultdict, deque

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay5(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=5, test=test)
        self.answer = None

    def part1(self):
        # open a file and read it
        print("Loading input...")

        with open(self.filename, "r") as f:
            lines = f.readlines()

            d = defaultdict(deque)

            for i, line in enumerate(lines):
                if line.startswith(" 1   2   3"):
                    break
                else:
                    for k in range(9):
                        dq = d[k]
                        index = 4 * k + 1
                        if len(line) > index:
                            item = line[index]
                            if item != " ":
                                dq.appendleft(item)

            i += 2
            for i, line in enumerate(lines[i:]):
                if line.startswith("move"):
                    _, n, _, f, _, t = line.strip().split()
                    for i in range(int(n)):
                        item = d[int(f) - 1].pop()
                        d[int(t) - 1].append(item)

            result = []
            for k, v in d.items():
                if len(v) > 0:
                    result.append(v.pop())

            return "".join(result)

    def part2(self):
        print("Loading input...")

        with open(self.filename, "r") as f:
            lines = f.readlines()

            d = defaultdict(deque)

            for i, line in enumerate(lines):
                if line.startswith(" 1   2   3"):
                    break
                else:
                    for k in range(9):
                        dq = d[k]
                        index = 4 * k + 1
                        if len(line) > index:
                            item = line[index]
                            if item != " ":
                                dq.appendleft(item)

            i += 2
            for i, line in enumerate(lines[i:]):
                if line.startswith("move"):
                    _, n, _, f, _, t = line.strip().split()
                    x = deque()
                    for i in range(int(n)):
                        item = d[int(f) - 1].pop()
                        x.append(item)
                    for i in range(int(n)):
                        item = x.pop()
                        d[int(t) - 1].append(item)

            result = []
            for k, v in d.items():
                if len(v) > 0:
                    result.append(v.pop())

            return "".join(result)


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

    day = AdventDay5(test=args.test)

    print(day.solve())
