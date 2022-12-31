from argparse import ArgumentParser
from collections import Counter, defaultdict

from aoc.common import AdventDay


class AdventDay3(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=3, test=test)
        self.answer = None

    def part1(self):
        # open a file and read it

        score = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,
            "i": 9,
            "j": 10,
            "k": 11,
            "l": 12,
            "m": 13,
            "n": 14,
            "o": 15,
            "p": 16,
            "q": 17,
            "r": 18,
            "s": 19,
            "t": 20,
            "u": 21,
            "v": 22,
            "w": 23,
            "x": 24,
            "y": 25,
            "z": 26,
            "A": 27,
            "B": 28,
            "C": 29,
            "D": 30,
            "E": 31,
            "F": 32,
            "G": 33,
            "H": 34,
            "I": 35,
            "J": 36,
            "K": 37,
            "L": 38,
            "M": 39,
            "N": 40,
            "O": 41,
            "P": 42,
            "Q": 43,
            "R": 44,
            "S": 45,
            "T": 46,
            "U": 47,
            "V": 48,
            "W": 49,
            "X": 50,
            "Y": 51,
            "Z": 52,
        }

        with open(self.filename, "r") as f:
            all_lines = f.readlines()
            s = 0
            for line in all_lines:
                line = line.strip()
                l = len(line)
                l1 = line[: l // 2]
                l2 = line[l // 2 :]

                inter = set(l1).intersection(set(l2))
                for e in inter:
                    s += score[e]
            return s

    def part2(self):
        # open a file and read it
        score = {
            "a": 1,
            "b": 2,
            "c": 3,
            "d": 4,
            "e": 5,
            "f": 6,
            "g": 7,
            "h": 8,
            "i": 9,
            "j": 10,
            "k": 11,
            "l": 12,
            "m": 13,
            "n": 14,
            "o": 15,
            "p": 16,
            "q": 17,
            "r": 18,
            "s": 19,
            "t": 20,
            "u": 21,
            "v": 22,
            "w": 23,
            "x": 24,
            "y": 25,
            "z": 26,
            "A": 27,
            "B": 28,
            "C": 29,
            "D": 30,
            "E": 31,
            "F": 32,
            "G": 33,
            "H": 34,
            "I": 35,
            "J": 36,
            "K": 37,
            "L": 38,
            "M": 39,
            "N": 40,
            "O": 41,
            "P": 42,
            "Q": 43,
            "R": 44,
            "S": 45,
            "T": 46,
            "U": 47,
            "V": 48,
            "W": 49,
            "X": 50,
            "Y": 51,
            "Z": 52,
        }
        with open(self.filename, "r") as f:
            all_lines = f.readlines()
            s = 0

            d = {}

            for i, line in enumerate(all_lines):
                group = int(i / 3)
                line = line.strip()

                if group not in d:
                    d[group] = set(line)
                else:
                    d[group] = d[group].intersection(set(line))

            s = 0
            for c in d:
                for e in d[c]:
                    s += score[e]

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

    day = AdventDay3(test=args.test)

    print(day.solve())
