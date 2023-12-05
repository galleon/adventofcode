from argparse import ArgumentParser

from aoc.common import AdventDay


class AdventDay2(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=2, test=test)

    def read_input(self):
        games = {}
        with open(self.filename, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                parts = line.strip().split(": ")
                game_id = int(parts[0].split(" ")[1])
                subsets = parts[1].split("; ")

                ll = []
                for subset in subsets:
                    dd = {}
                    for color in subset.split(", "):
                        cnt, col = color.split(" ")
                        dd[col] = int(cnt)
                    ll.append(dd)
                games[game_id] = ll
            return games

    def part1(self):
        def is_game_possible(game, available_cubes):
            max_needed_in_game = {"red": 0, "green": 0, "blue": 0}
            for subset in game:
                for color, cnt in subset.items():
                    # Ensure color is valid and count is an integer
                    if color in max_needed_in_game:
                        max_needed_in_game[color] = max(max_needed_in_game[color], cnt)
                    else:
                        print(f"Warning: Invalid color '{color}'")

            return all(
                max_needed_in_game[color] <= available_cubes[color]
                for color in max_needed_in_game
            )

        games = self.read_input()

        # Available cubes
        available_cubes = {"red": 12, "green": 13, "blue": 14}

        # Determine which games are possible
        possible_games = [
            game_id
            for game_id, game in games.items()
            if is_game_possible(game, available_cubes)
        ]

        # Sum of IDs of possible games
        sum_possible_games = sum(possible_games)

        return sum_possible_games

    def part2(self):
        def min_cubes_for_game(game):
            min_needed = {"red": 0, "green": 0, "blue": 0}
            for subset in game:
                for color, count_str in subset.items():
                    # Convert count to integer
                    count = int(count_str)
                    # Update minimum needed count for each color
                    if count > min_needed[color]:
                        min_needed[color] = count
            return min_needed

        def calculate_power(min_needed):
            # Multiply the minimum numbers of red, green, and blue cubes
            return min_needed["red"] * min_needed["green"] * min_needed["blue"]

        games = self.read_input()

        # Calculate the minimum cubes required and power for each game
        min_cubes_per_game = {
            game_id: min_cubes_for_game(game) for game_id, game in games.items()
        }

        # Calcule power for each game
        power_per_game = {
            game_id: calculate_power(min_cubes)
            for game_id, min_cubes in min_cubes_per_game.items()
        }

        # Return sum of powers for all games
        return sum(power_per_game.values())


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

    day = AdventDay2(test=args.test)

    print(day.solve())
