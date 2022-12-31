from argparse import ArgumentParser
from collections import defaultdict

from aoc.common import AdventDay


class P:
    def __init__(self, v):
        self.v = v

    def __lt__(self, other):
        return self.compare(self.v, other.v) == -1

    def __gt__(self, other):
        return self.compare(other.v, self.v) == 1

    def __eq__(self, other):
        return self.compare(self.v, other.v) == 0

    def compare(self, left, right):
        # if both are int, compare them
        if isinstance(left, int) and isinstance(right, int):
            return -1 if left < right else 1 if left > right else 0
        # if any of them is int transform it to list
        if isinstance(left, int):
            left = [left]
        if isinstance(right, int):
            right = [right]
        # compare each sub-list using common length
        for lsub, rsub in zip(left, right):
            sub = self.compare(lsub, rsub)
            if sub != 0:
                return sub
        # if sublist are equal, compare length
        if len(left) < len(right):
            return -1
        if len(left) > len(right):
            return 1
        return 0


class AdventDay13(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=13, test=test)

    def load_input(self):
        print("Loading input...")

        pairs = []
        for block in open(self.filename).read().split("\n\n"):
            lines = block.split("\n")
            pairs.append([P(eval(lines[0])), P(eval(lines[1]))])

        return pairs

    def part1(self):
        pairs = self.load_input()

        result = 0
        for i, p in enumerate(pairs):
            # print(f"{i:03} {True if p[0] < p[1] else False}")
            if p[0] < p[1]:
                result += i + 1

        return result

    def part2(self):
        pairs = self.load_input()

        p2 = P([2])
        p6 = P([6])

        packets = [p2, p6]

        for p in pairs:
            for a in p:
                packets.append(a)

        packets.sort()

        return (packets.index(p2) + 1) * (packets.index(p6) + 1)


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

    day = AdventDay13(test=args.test)

    print(day.solve())
