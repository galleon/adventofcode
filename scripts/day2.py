from argparse import ArgumentParser

from aoc.common import AdventDay


class AdventDay2(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=2, test=test)
        self.answer = None

    def part1(self):
        answer = [0, 0]
        # Rock,    Paper, Scissors
        # A, X .   B, Y .   C, Z .
        points = {
            "A X": 1 + 3,
            "A Y": 2 + 6,
            "A Z": 3 + 0,
            "B X": 1 + 0,
            "B Y": 2 + 3,
            "B Z": 3 + 6,
            "C X": 1 + 6,
            "C Y": 2 + 0,
            "C Z": 3 + 3,
        }
        score = 0

        # open a file and read it
        with open(self.filename, "r") as f:
            for line in f:
                # convert the string to an integer
                score += points[line.strip()]
            return score

    def part2(self):
        answer = [0, 0]
        # Rock,    Paper, Scissors
        # A, X .   B, Y .   C, Z .
        points = {
            "A X": 1 + 3,
            "A Y": 2 + 6,
            "A Z": 3 + 0,
            "B X": 1 + 0,
            "B Y": 2 + 3,
            "B Z": 3 + 6,
            "C X": 1 + 6,
            "C Y": 2 + 0,
            "C Z": 3 + 3,
        }
        score = 0
        wins = {"A": "Y", "B": "Z", "C": "X"}
        draw = {"A": "X", "B": "Y", "C": "Z"}
        lose = {"A": "Z", "B": "X", "C": "Y"}

        # open a file and read it
        with open(self.filename, "r") as f:
            for line in f:
                # convert the string to an integer
                f, s = line.strip().split()
                if s == "X":  # lose
                    score += points[f"{f} {lose[f]}"]
                elif s == "Y":
                    score += points[f"{f} {draw[f]}"]
                elif s == "Z":
                    score += points[f"{f} {wins[f]}"]

            return score


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

    day = AdventDay2(test=args.test)

    print(day.solve())
