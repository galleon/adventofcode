from sys import maxsize as MAX_SIZE
from os import stat
import re
from argparse import ArgumentParser
from collections import defaultdict
from dotenv.main import load_dotenv

import numpy as np

from aoc.common import AdventDay
from aoc.data import Board, Graph

import sys, fileinput, re, collections, heapq, bisect, itertools, functools, copy, math


class AdventDay6(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=6, test=test)

    def read_input(self):
        """
        Parses the input text to extract seed numbers and mapping data.
        """

        races = []
        with open(self.filename, "r") as file:
            lines = file.readlines()

            if len(lines) < 2:
                raise ValueError("Input file does not contain enough data.")

            # Process the lines
            times = lines[0].strip().replace("Time:", "").split()
            distances = lines[1].strip().replace("Distance:", "").split()

            if len(times) != len(distances):
                raise ValueError("The number of times and distances do not match.")

            # Pair times and distances
            races = [
                (int(time), int(distance)) for time, distance in zip(times, distances)
            ]

        return races

    def part1(self):
        races = self.read_input()

        ways_to_win = []
        for total_time, record_distance in races:
            count = 0
            for time_held in range(total_time):
                speed = time_held  # Speed increases by 1 mm/ms for each ms the button is held
                remaining_time = total_time - time_held
                distance = speed * remaining_time
                if distance > record_distance:
                    count += 1
            ways_to_win.append(count)

        final_product = 1
        for ways in ways_to_win:
            final_product *= ways

        return final_product

    def part2(self):
        races = self.read_input()

        concatenated_time = ""
        concatenated_distance = ""

        for time, distance in races:
            concatenated_time += str(time)
            concatenated_distance += str(distance)

        total_time = int(concatenated_time)
        record_distance = int(concatenated_distance)

        a, b, c = -1, total_time, -record_distance
        delta = b**2 - 4 * a * c
        assert delta >= 0
        sqrt_val = math.sqrt(b**2 - 4 * a * c)

        # Two solutions for the quadratic equation
        sol1 = (-b + sqrt_val) / (2 * a)
        sol2 = (-b - sqrt_val) / (2 * a)

        ways_to_win = int(sol2) - int(sol1)

        return ways_to_win


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

    day = AdventDay6(test=args.test)

    print(day.solve())
