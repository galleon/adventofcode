import bisect
import collections
import copy
import fileinput
import functools
import heapq
import itertools
import math
import re
import sys
from argparse import ArgumentParser
from collections import defaultdict
from os import stat
from sys import maxsize as MAX_SIZE

import numpy as np
from dotenv.main import load_dotenv

from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay7(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=7, test=test)

    def read_input(self):
        path = []
        tree = {}
        node = tree
        with open(self.filename, "r") as f:
            all_lines = f.readlines()
            for l in all_lines:
                l = l.strip()
                if l.startswith("$ cd /"):
                    path = []
                    node = tree
                elif l.startswith("$ cd .."):
                    path.pop()
                    node = tree
                    for name in path:
                        node = node[name]
                elif l.startswith("$ cd "):
                    name = l.split()[-1]
                    path.append(name)
                    node = node[name]
                elif l.startswith("dir "):
                    name = l.split()[-1]
                    node[name] = {}
                elif l != "$ ls":
                    size, name = l.split()
                    node[name] = int(size)

        return tree

    def compute_total_size(self, node):
        stree = sum(
            val if isinstance(val, int) else self.compute_total_size(val)
            for key, val in node.items()
        )
        if stree <= 100_000:
            self.total_size += stree

        return stree

    def compute_dir_space(self, node):
        return sum(
            val if isinstance(val, int) else self.compute_dir_space(val)
            for key, val in node.items()
        )

    def prune_dir(self, node):
        stree = sum(
            val if isinstance(val, int) else self.prune_dir(val)
            for key, val in node.items()
        )
        if stree >= self.needed:
            self.smallest = min(self.smallest, stree)
        return stree

    def part1(self):
        root = self.read_input()

        self.total_size = 0
        self.compute_total_size(root)

        return self.total_size

    def part2(self):
        root = self.read_input()

        self.needed = -40_000_000 + self.compute_dir_space(root)

        self.smallest = 70_000_000

        self.prune_dir(root)

        return self.smallest


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

    day = AdventDay7(test=args.test)

    print(day.solve())
