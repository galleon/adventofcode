import re
from argparse import ArgumentParser
from collections import defaultdict
import operator

import numpy as np
from dotenv.main import load_dotenv

from aoc.common import AdventDay
from aoc.data import Board, Graph

from collections import deque
from math import prod


class AdventDay11(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=11, test=test)

    def load_input(self):
        print("Loading input...")

        product = 1
        monkeys = []

        for block in open(self.filename).read().split("\n\n"):
            lines = block.split("\n")
            current_monkey = {}
            current_monkey["items"] = list(
                map(int, lines[1][len("  Starting items: ") :].split(", "))
            )

            operation = lines[2].split(" = ")[1].split(" ")
            # print(f"lambda x: x {operation[1]} {operation[2]}".replace("old", "x"))
            current_monkey["operation"] = eval(
                f"lambda x: x {operation[1]} {operation[2]}".replace("old", "x")
            )

            product *= 1
            # test will be a list of 3 elements: [divisor, monkey1, monkey2]
            current_monkey["test"] = [int(lines[3].split(" by ")[1])]
            product *= current_monkey["test"][0]
            current_monkey["test"].append(int(lines[4].split(" to monkey ")[1]))
            current_monkey["test"].append(int(lines[5].split(" to monkey ")[1]))

            current_monkey["inspected"] = 0

            monkeys.append(current_monkey)

        return product, monkeys

    def process(self, values, part):
        if part == 1:
            divide_by = 3
            rounds = 20
        else:
            divide_by = 1
            rounds = 10_000

        product, monkeys = values

        for _ in range(rounds):
            for m in monkeys:
                for item in m["items"]:
                    m["inspected"] += 1

                    new_item = m["operation"](item)
                    # divide by 3 or not
                    new_item = int(new_item / divide_by)

                    if new_item % m["test"][0] == 0:
                        monkeys[m["test"][1]]["items"].append(new_item % product)
                    else:
                        # print("Thrown to monkey", sendt[monkey]][0])
                        monkeys[m["test"][2]]["items"].append(new_item % product)

                m["items"] = []

        return prod(
            sorted([monkey["inspected"] for monkey in monkeys], reverse=True)[:2]
        )

    def part1(self):
        return self.process((self.load_input()), 1)

    def part2(self):
        return self.process((self.load_input()), 2)


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

    day = AdventDay11(test=args.test)

    print(day.solve())
