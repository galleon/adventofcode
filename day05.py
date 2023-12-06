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


class AdventDay5(AdventDay):
    def __init__(self, test: bool = False):
        super().__init__(day=5, test=test)

    def read_input(self):
        """
        Parses the input text to extract seed numbers and mapping data.
        """

        def parse_mapping(mapping_lines):
            return [tuple(map(int, line.split())) for line in mapping_lines]

        def parse_input(input_text):
            sections = input_text.split("\n\n")
            seeds = list(map(int, sections[0].split(":")[1].strip().split()))
            maps = [
                parse_mapping(section.strip().split("\n")[1:])
                for section in sections[1:]
            ]
            return seeds, maps

        with open(self.filename, "r") as file:
            input_text = file.read()

        return parse_input(input_text)

    def part1(self):
        seeds, maps = self.read_input()

        def find_destination_number(source_number, mapping_rules):
            for dest_start, src_start, length in mapping_rules:
                if src_start <= source_number < src_start + length:
                    return dest_start + (source_number - src_start)
            return source_number  # Return the number itself if not found in mapping

        def process_seed_through_maps(seed, maps):
            for mapping in maps:
                seed = find_destination_number(seed, mapping)
            return seed

        location_numbers = [process_seed_through_maps(seed, maps) for seed in seeds]
        return min(location_numbers)

    def part2(self):
        seeds, maps = self.read_input()

        def process_range_through_maps(seed_range, maps):
            # Go through the different types of maps
            for mapping in maps:
                seed_range = transform_range(seed_range, mapping)
            return seed_range

        def transform_range(input_range, mapping_rules):
            transformed_ranges = []
            # Go through the seed ranges
            for start, length in input_range:
                end = start + length
                # Go through the different sub-mappings
                for dest_start, src_start, src_length in mapping_rules:
                    src_end = src_start + src_length
                    # Check if the seed range overlaps with the sub-mapping
                    if src_start < end and src_end > start:
                        overlap_start = max(start, src_start)
                        overlap_end = min(end, src_end)
                        overlap_length = overlap_end - overlap_start
                        transformed_start = dest_start + (overlap_start - src_start)
                        transformed_ranges.append((transformed_start, overlap_length))
            return merge_transformed_ranges(transformed_ranges)

        def merge_transformed_ranges(transformed_ranges):
            # Merge final sub mappings
            merged = []
            for start, length in sorted(transformed_ranges):
                if not merged or start > merged[-1][0] + merged[-1][1]:
                    merged.append([start, length])
                else:
                    merged[-1][1] = max(merged[-1][1], start + length - merged[-1][0])
            return [(start, length) for start, length in merged]

        final_ranges = []
        for i in range(0, len(seeds), 2):
            # Go through the seed ranges
            seed_start, seed_length = seeds[i], seeds[i + 1]
            final_ranges.append((seed_start, seed_length))

        final_locations = process_range_through_maps(final_ranges, maps)
        lowest_location = min(start for start, _ in final_locations)
        return lowest_location


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

    day = AdventDay5(test=args.test)

    print(day.solve())
