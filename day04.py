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


class AdventDay4(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=4, test=test)

    def read_input(self):
        boards = {}
        #        with open(f"{self.filename}_test", "r") as f:
        with open(f"{self.filename}", "r") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(": ")
                print(parts)
                card_num = int(parts[0].split()[1])
                subsets = parts[1].split(" | ")
                print(card_num, subsets[0], subsets[1])
                winning_numbers = [int(x) for x in subsets[0].split()]
                all_numbers = [int(x) for x in subsets[1].split()]

                boards[card_num] = [winning_numbers, all_numbers]

            return boards

    def part1(self):
        boards = self.read_input()

        def calculate_points(winning_numbers, all_numbers):
            # Convert winning numbers to a set for efficient lookup
            winning_set = set(winning_numbers)
            matches = 0
            points = 0

            for number in all_numbers:
                if number in winning_set:
                    matches += 1
                    if matches == 1:  # Only add points starting from the first match
                        points += 1
                    else:  # Double the points for the second, third, and fourth matches
                        points *= 2

            return matches, points

        p = 0
        for card_num, boards in boards.items():
            winning_numbers, all_numbers = boards
            matches, points = calculate_points(winning_numbers, all_numbers)
            print(f"Card {card_num}: {matches} matches, {points} points")
            p += points

        return p

    def part2(self):
        boards = self.read_input()

        def count_matches_and_win_copies(cards):
            # Initialize a dictionary to keep track of the number of copies of each card
            card_copies = {
                card: 1 for card in cards
            }  # Start with one copy of each card
            processed_cards = {}

            for card, (winning_numbers, all_numbers) in cards.items():
                if card in processed_cards:
                    continue  # Skip if this card has been processed

                matches = sum(1 for num in all_numbers if num in winning_numbers)
                processed_cards[card] = matches  # Mark this card as processed

                # For each match, win copies of the next cards
                next_cards = list(cards.keys())[list(cards.keys()).index(card) + 1 :]
                for i in range(matches):
                    if i < len(next_cards):
                        card_copies[next_cards[i]] += card_copies[card]

            return sum(card_copies.values())

        return count_matches_and_win_copies(boards)

        return 0


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

    day = AdventDay4(test=args.test)

    print(day.solve())
