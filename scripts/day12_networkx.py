from argparse import ArgumentParser
from collections import defaultdict, deque

import networkx as nx
from termcolor import colored

# those modules are here https://github.com/galleon/adventofcode2021/blob/main/data.py
from aoc.common import AdventDay
from aoc.data import Board, Graph


class AdventDay12(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=12, test=test)

    def load_input(self):
        print("Loading input...")
        lines = []
        with open(self.filename, "r") as f:
            for line in f.readlines():
                lines.append(line.strip())

        # Reading the board
        board = Board.from_text(lines)

        x_positions = []
        x_character = "a"

        g = nx.DiGraph()

        # Moving the board to a integer values
        for x in range(0, board._width + 1):
            for y in range(0, board._height + 1):
                l = board[(x, y)]
                if l == "S":
                    start = (x, y)
                    val = 1
                elif l == "E":
                    val = ord("z") - ord("a") + 1
                    end = (x, y)
                elif l == x_character:
                    val = ord(x_character) - ord("a") + 1
                    x_positions.append((x, y))
                else:
                    val = ord(l) - ord("a") + 1

                g.add_node((x, y), val=val)

        for x in range(0, board._width + 1):
            for y in range(0, board._height + 1):
                for xx, yy in board.neighbors(x, y, valid_only=True):
                    if g.nodes[(xx, yy)]["val"] <= g.nodes[(x, y)]["val"] + 1:
                        g.add_edge((x, y), (xx, yy))

        return x_positions, start, end, g

    def part1(self):
        a_positions, start, end, graph = self.load_input()

        return nx.shortest_path_length(graph, start, end)

    def part2(self):
        a_positions, start, end, graph = self.load_input()

        length = nx.shortest_path_length(graph, start, end)

        for a_position in a_positions:
            # This will raise an exception if there is no path
            try:
                l = nx.shortest_path_length(graph, a_position, end)
            except:
                l = length

            if l < length:
                length = l

        return length


# define main
if __name__ == "__main__":
    # define the parser
    parser = ArgumentParser(description="Second year Advent of Code")

    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test",
        default=False,
        required=False,
    )

    args = parser.parse_args()

    day = AdventDay12(test=args.test)

    print(day.solve())
