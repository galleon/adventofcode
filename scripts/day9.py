import operator
import re
from argparse import ArgumentParser
from collections import defaultdict

import numpy as np
from dotenv.main import load_dotenv

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay9(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=9, test=test)

    def the_tail_is(self, head, tail):
        dx = head[0] - tail[0]
        dy = head[1] - tail[1]
        if abs(dx) <= 1 and abs(dy) <= 1:
            # ok the tail is already next to the head,
            pass
        elif abs(dx) >= 2 and abs(dy) >= 2:
            return (
                head[0] - 1 if tail[0] < head[0] else head[0] + 1,
                head[1] - 1 if tail[1] < head[1] else head[1] + 1,
            )
        elif abs(dx) >= 2:
            return (head[0] - 1 if tail[0] < head[0] else head[0] + 1, head[1])
        elif abs(dy) >= 2:
            return (head[0], head[1] - 1 if tail[1] < head[1] else head[1] + 1)
        return tail

    def load_input(self):
        print("Loading input...")
        outputs = []
        with open(self.filename, "r") as f:
            for line in f.readlines():
                outputs.append(line.strip().split())

            return outputs

    def part1(self, tail_length=1):
        lines = self.load_input()

        s = (0, 0)
        head = s
        visited = set(s)
        tail = [s for _ in range(tail_length)]

        move = {"U": (-1, 0), "D": (1, 0), "L": (0, -1), "R": (0, 1)}

        for (d, n) in lines:
            for _ in range(int(n)):
                # next position of head
                head = (head[0] + move[d][0], head[1] + move[d][1])

                # move tail
                position = head
                for i, t in enumerate(tail):
                    tail[i] = self.the_tail_is(position, t)
                    position = tail[i]
                visited.add(tail[-1])

        return len(visited) - 1

    def part2(self):
        return self.part1(9)


if __name__ == "__main__":
    # define tailsheadse parser
    parser = ArgumentParser(description="First year Advent of Code")

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test",
        default=False,
        required=False,
    )

    args = parser.parse_args()

    print(f"test mode: {args.test}")

    day = AdventDay9(test=args.test)

    print(day.solve())
