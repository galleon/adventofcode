from argparse import ArgumentParser


from aoc.common import AdventDay


class AdventDay1(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(year=2022, day=1, test=test)
        self.answer = None

    def part1(self):
        with open(self.filename, "r") as f:
            all_lines = f.readlines()

            results = []
            x = 0
            maximum = 0
            for line in all_lines:
                l = line.strip()
                if len(l) == 0:
                    results.append(x)
                    if x > maximum:
                        maximum = x
                    x = 0
                else:
                    x += int(l)

        return maximum

    def part2(self):
        with open(self.filename, "r") as f:
            all_lines = f.readlines()

            results = []
            x = 0
            maximum = 0
            for line in all_lines:
                l = line.strip()
                if len(l) == 0:
                    results.append(x)
                    if x > maximum:
                        maximum = x
                    x = 0
                else:
                    x += int(l)

        return sum(sorted(results, reverse=True)[:3])


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

    day = AdventDay1(test=args.test)

    print(day.solve())
