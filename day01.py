import argparse
import tempfile
import re

def find_first_last_digit(s):
    first_digit = None
    last_digit = None

    # Find the first digit
    for char in s:
        if char.isdigit():
            first_digit = char
            break

    # Find the last digit
    for char in reversed(s):
        if char.isdigit():
            last_digit = char
            break

    return int(first_digit), int(last_digit)

def find_first_last_digit_2(s):
    # Mapping of digit words to their numerical values
    digit_map = {
        "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4,
        "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9
    }

    # Function to find all occurrences of a substring in a string
    def find_all_occurrences(sub, string):
        start = 0
        while start < len(string):
            start = string.find(sub, start)
            if start == -1: break
            yield start
            start += len(sub) # move to the next possible start position

    found_digits = []
    for word, value in digit_map.items():
        for index in find_all_occurrences(word, s):
            found_digits.append((index, value))

    for i in range(10):
        for index in find_all_occurrences(str(i), s):
            found_digits.append((index, i))

    # Sort the found digits by their indices
    found_digits.sort()

    if not found_digits:
        return None, None

    # Extract the first and last digit values based on their indices
    first_digit = found_digits[0][1]
    last_digit = found_digits[-1][1]

    return first_digit, last_digit


def part_1(filename):
    counter: int = 0
    # open a file and read it
    with open(filename, "r") as f:
        prev = None
        try:
            # read the file line by line
            for line in f:
                # convert the string to an integer
                #
                c1, cn = find_first_last_digit(line)

                number = c1*10+cn
                
                # add the line to the counter
                counter += number
            # read a line and convert to int

            token = f.readline()
        except ValueError:
            print(f"Error {ValueError} with file {filename}")
    return counter


def part_2(filename):
    counter: int = 0
    # open a file and read it
    with open(filename, "r") as f:
        prev = None
        try:
            # read the file line by line
            for line in f:
                # convert the string to an integer
                #
                c1, cn = find_first_last_digit_2(line)

                number = c1*10+cn
                
                # add the line to the counter
                counter += number
            # read a line and convert to int

            token = f.readline()
        except ValueError:
            print(f"Error {ValueError} with file {filename}")
    return counter


# define main
if __name__ == "__main__":
    # define the parser
    parser = argparse.ArgumentParser(description="Day 1 Challenge")
    parser.add_argument(
        "--filename",
        help="The file to read",
        type=str,
        required=False,
        default="inputs/2023/2",
    )
    parser.add_argument(
        "--test",
        action="store_true",
        help="Run the test",
        default=False,
        required=False,
    )

    args = parser.parse_args()

    if args.test:
        # create a temp file
        with tempfile.NamedTemporaryFile(mode="w") as f:
            # write some data to the file
            f.write("1\n2\n3\n4\n")
            # rewind the file
            f.seek(0)
            assert part_1(f.name) == 3
        with tempfile.NamedTemporaryFile(mode="w") as f:
            # write some data to the file
            f.write("4\n3\n2\n1")
            # rewind the file
            f.seek(0)
            #
            assert part_(f.name) == 0
        with tempfile.NamedTemporaryFile(mode="w") as f:
            # write some data to the file
            f.write("4\n4\n4\n4")
            # rewind the file
            f.seek(0)
            #
            assert part_1(f.name) == 0
        with tempfile.NamedTemporaryFile() as f:
            # write some data to the file
            f.write(b"")
            # rewind the file
            f.seek(0)
            #
            assert part_1(f.name) == 0
        with tempfile.NamedTemporaryFile() as f:
            # write some data to the file
            f.write(b"4\n3\n4\n3")
            # rewind the file
            f.seek(0)
            #
            assert part_1(f.name) == 1
        with tempfile.NamedTemporaryFile() as f:
            f.write(b"199\n200\n208\n210\n200\n207\n240\n269\n260\n263")
            f.seek(0)
            assert part_2(f.name) == 5
    else:
        print(part_1(args.filename), part_2(args.filename))
