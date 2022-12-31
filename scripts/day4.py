from argparse import ArgumentParser
from collections import Counter, defaultdict

from aoc.common import AdventDay


class AdventDay4(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=4, test=test)
        self.answer = None

    def part1(self):
        # open a file and read it
        with open(self.filename, "r") as f:

            all_lines = f.readlines()
            s = 0
            for line in all_lines:
                l1, l2 = line.strip().split(",")
                l1_min, l1_max = map(int, l1.split("-"))
                l2_min, l2_max = map(int, l2.split("-"))

                if (l1_min >= l2_min and l1_max <= l2_max) or (
                    l1_min <= l2_min and l1_max >= l2_max
                ):
                    s += 1
            return s

    def part2(self):
        with open(self.filename, "r") as f:
            all_lines = f.readlines()
            s = 0
            for line in all_lines:
                l1, l2 = line.strip().split(",")
                l1_min, l1_max = map(int, l1.split("-"))
                l2_min, l2_max = map(int, l2.split("-"))

                if (
                    l2_min in range(l1_min, l1_max + 1)
                    or l2_max in range(l1_min, l1_max + 1)
                    or l1_min in range(l2_min, l2_max + 1)
                    or l1_max in range(l2_min, l2_max + 1)
                ):
                    s += 1

            return s


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

    day = AdventDay4(test=args.test)

    print(day.solve())
