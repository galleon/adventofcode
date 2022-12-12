import re
import time
from collections import defaultdict
from datetime import datetime
from os import getenv
from typing import List

import requests
from dotenv import load_dotenv


class AdventDay:
    def __init__(self, day: int = 42, year: int = 9999, test: bool = False):
        load_dotenv()
        self.SESSION_COOKIE = getenv("SESSION_COOKIE")

        if year == 9999:
            self.year = datetime.now().year
        else:
            self.year = year

        if day == 42:
            # set day to today's day
            self.day = datetime.now().day
        else:
            self.day = day

        print(f"Solving day {self.day} of year {self.year}")

        if test:
            self.filename = f"inputs/{self.year}/{self.day}_test"
        else:
            response = requests.get(
                f"https://adventofcode.com/{self.year}/day/{self.day}/input",
                cookies={"session": self.SESSION_COOKIE},
            )

            if response.status_code != 200:
                raise Exception(f"Error while fetching input: {response.status_code}")

            self.filename = f"inputs/{self.year}/{self.day}"
            with open(self.filename, "wb") as f:
                f.write(response.content)

    def part1(self):
        pass

    def part2(self):
        pass

    def submit_answer(self, part, answer):

        url = f"https://adventofcode.com/{self.year}/day/{self.day}/answer"

        response = requests.post(
            url,
            data={"level": part, "answer": answer},
            cookies={"session": self.SESSION_COOKIE},
        )
        assert response.status_code == 200
        t = response.text.lower()

        if "did you already complete it" in t:
            print("Already completed or wrong day/part.\n")
            return False

        if "that's the right answer" in t:
            print("Right answer!\n")

            if self.day == 25 and part == 1:
                print("It's Christmas! Automatically submitting second part in 5s...\n")
                time.sleep(5)
                requests.post(url, data={"level": 2, "answer": 0})
                print("done!\n")
                print(
                    f"Go check it out: https://adventofcode.com/{self.year}/day/25#part2\n"
                )

            return True

        if "you have to wait" in t:
            matches = re.compile(r"you have ([\w ]+) left to wait").findall(t)

            if matches:
                print(f"Submitting too fast, {matches[0]} left to wait.\n")
            else:
                print("Submitting too fast, slow down!\n")

            return False

        print("Wrong answer :(\n")
        return False

    def solve(self):
        return self.part1(), self.part2()
