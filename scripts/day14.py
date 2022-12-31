from argparse import ArgumentParser
from collections import defaultdict

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay14(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=14, test=test)

    def load_input(self):
        outputs = []
        with open(self.filename, "r") as f:
            lines = f.readlines()

            for line in lines:
                outputs.append(line.strip())

            return outputs

    def part1(self):
        lines = self.load_input()

        b = Board()

        pairs = []
        for line in lines:
            sequence = []
            for s in line.split(" -> "):
                s = s.split(",")
                sequence.append((int(s[0]), int(s[1])))
            pairs.append(sequence)

        for pair in pairs:
            x, y = pair[0]
            for i in range(1, len(pair)):
                xx, yy = pair[i]
                for i in range(min(x, xx), max(x, xx) + 1):
                    for j in range(min(y, yy), max(y, yy) + 1):
                        b[(i, j)] = 1
                x, y = xx, yy

        limit = b._height

        sx = 500
        sy = 0

        s = 0

        while True:
            if sy >= limit:
                break
            if b[(sx, sy + 1)] == 0:
                # going down
                sy += 1
            elif b[(sx - 1, sy + 1)] == 0:
                # going down left
                sx -= 1
                sy += 1
            elif b[(sx + 1, sy + 1)] == 0:
                # going down right
                sx += 1
                sy += 1
            # elif sy == 0 and b[(sx, sy)] != 0:
            #     print("reached the top")
            #     break
            else:
                # reached the bottom, start again
                b[(sx, sy)] = 2
                s += 1
                sx = 500
                sy = 0

        print(s)
        return s

    def part2(self):
        lines = self.load_input()

        b = Board()

        pairs = []
        for line in lines:
            sequence = []
            for s in line.split(" -> "):
                s = s.split(",")
                sequence.append((int(s[0]), int(s[1])))
            pairs.append(sequence)

        for pair in pairs:
            x, y = pair[0]
            for i in range(1, len(pair)):
                xx, yy = pair[i]
                for i in range(min(x, xx), max(x, xx) + 1):
                    for j in range(min(y, yy), max(y, yy) + 1):
                        b[(i, j)] = 1
                x, y = xx, yy

        limit = b._height + 2

        sx = 500
        sy = 0

        s = 0

        while True:
            # print(sx, sy)
            # if sy >= limit:
            #     print(f"reached the bottom at x -> {sx}")
            #     break
            sx, sy = 500, 0
            while sy < limit -1:
                if b[(sx, sy + 1)] == 0:
                    # going down
                    sy += 1
                elif b[(sx - 1, sy + 1)] == 0:
                    # going down left
                    sx -= 1
                    sy += 1
                elif b[(sx + 1, sy + 1)] == 0:
                    # going down right
                    sx += 1
                    sy += 1
                else:
                    break

            b[(sx, sy)] = 2
            s += 1
            if (sx, sy) == (500, 0):
                break

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

    day = AdventDay14(test=args.test)

    print(day.solve())
