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


class AdventDay3(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=3, test=test)

    def read_input(self):
        board = []
        #        with open(f"{self.filename}_test", "r") as f:
        with open(f"{self.filename}", "r") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = [x for x in line.strip()]

                board.append(parts)

            return board

    def part1(self):
        board = self.read_input()

        def is_symbol(ch):
            return not (ch.isdigit() or ch == ".")

        def get_adjacent_numbers(i, j):
            numbers = set()
            # Check horizontal, vertical, and diagonal neighbors for numbers
            for x, y in [
                (i - 1, j),
                (i + 1, j),
                (i, j - 1),
                (i, j + 1),
                (i - 1, j - 1),
                (i - 1, j + 1),
                (i + 1, j - 1),
                (i + 1, j + 1),
            ]:
                if 0 <= x < rows and 0 <= y < cols and board[x][y].isdigit():
                    numbers.add(get_part_number(x, y))
            return list(numbers)

        def get_part_number(i, j):
            part_number = board[i][j]
            # Expand to the left
            left = j - 1
            while left >= 0 and board[i][left].isdigit():
                part_number = board[i][left] + part_number
                left -= 1

            # Expand to the right
            right = j + 1
            while right < cols and board[i][right].isdigit():
                part_number += board[i][right]
                right += 1

            return part_number

        def sum_part_numbers(symbols_info):
            all_numbers = []
            for numbers in symbols_info.values():
                all_numbers.extend(numbers)
            return sum(int(number) for number in all_numbers)

        rows, cols = len(board), len(board[0])
        symbols_info = {}

        for i in range(rows):
            for j in range(cols):
                if is_symbol(board[i][j]):
                    # Record the symbol's sign and position
                    symbol_key = (board[i][j], (i, j))
                    # Find all adjacent numbers to this symbol
                    associated_numbers = get_adjacent_numbers(i, j)
                    symbols_info[symbol_key] = associated_numbers

        return sum_part_numbers(symbols_info)

    def part2(self):
        board = self.read_input()

        def is_symbol(ch):
            return not (ch.isdigit() or ch == ".")

        def get_adjacent_numbers(i, j):
            numbers = set()
            # Check horizontal, vertical, and diagonal neighbors for numbers
            for x, y in [
                (i - 1, j),
                (i + 1, j),
                (i, j - 1),
                (i, j + 1),
                (i - 1, j - 1),
                (i - 1, j + 1),
                (i + 1, j - 1),
                (i + 1, j + 1),
            ]:
                if 0 <= x < rows and 0 <= y < cols and board[x][y].isdigit():
                    numbers.add(get_part_number(x, y))
            return list(numbers)

        def get_part_number(i, j):
            part_number = board[i][j]
            # Expand to the left
            left = j - 1
            while left >= 0 and board[i][left].isdigit():
                part_number = board[i][left] + part_number
                left -= 1

            # Expand to the right
            right = j + 1
            while right < cols and board[i][right].isdigit():
                part_number += board[i][right]
                right += 1

            return part_number

        def sum_part_numbers(symbols_info):
            all_numbers = []
            for numbers in symbols_info.values():
                all_numbers.extend(numbers)
            return sum(int(number) for number in all_numbers)

        def sum_product_of_gears(symbols_info):
            total_sum = 0
            for symbol, numbers in symbols_info.items():
                if symbol[0] == "*" and len(numbers) == 2:
                    total_sum += int(numbers[0]) * int(numbers[1])
            return total_sum

        rows, cols = len(board), len(board[0])
        symbols_info = {}

        for i in range(rows):
            for j in range(cols):
                if is_symbol(board[i][j]):
                    # Record the symbol's sign and position
                    symbol_key = (board[i][j], (i, j))
                    # Find all adjacent numbers to this symbol
                    associated_numbers = get_adjacent_numbers(i, j)
                    symbols_info[symbol_key] = associated_numbers

        return sum_product_of_gears(symbols_info)


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

    day = AdventDay3(test=args.test)

    print(day.solve())
