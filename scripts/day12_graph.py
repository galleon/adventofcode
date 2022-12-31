from argparse import ArgumentParser
from collections import defaultdict, deque

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

        # Moving the board to a integer values
        for x in range(0, board._width + 1):
            for y in range(0, board._height + 1):
                l = board[(x, y)]
                if l == "S":
                    start = (x, y)
                    board[(x, y)] = 1
                elif l == "E":
                    board[(x, y)] = ord("z") - ord("a") + 1
                    end = (x, y)
                elif l == x_character:
                    board[(x, y)] = ord(x_character) - ord("a") + 1
                    x_positions.append((x, y))
                else:
                    board[(x, y)] = ord(l) - ord("a") + 1

        return x_positions, start, end, board

    def search_the_end(self, starting_positions, end, board):
        paths = set()
        while starting_positions:
            (x, y), d = starting_positions.popleft()
            if (x, y) in paths:
                continue
            paths.add((x, y))
            # as soon as we find the end, we return the distance - this is the shortest path
            if (x, y) == end:
                return d
            # Iterate over the neighbors
            for xx, yy in board.neighbors(x, y, valid_only=True):
                if board[(xx, yy)] <= board[(x, y)] + 1:
                    starting_positions.append(((xx, yy), d + 1))

    def part1(self):
        a_positions, start, end, board = self.load_input()

        starting_positions = deque()
        starting_positions.append((start, 0))

        return self.search_the_end(starting_positions, end, board)

    def part2(self):
        a_positions, start, end, board = self.load_input()

        starting_positions = deque()
        starting_positions.append((start, 0))

        for a_position in a_positions:
            starting_positions.append((a_position, 0))

        return self.search_the_end(starting_positions, end, board)


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
