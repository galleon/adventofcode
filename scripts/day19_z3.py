#!/bin/python3

import functools
import sys
import time

from collections import defaultdict

from collections import deque

import numpy as np

from z3 import Int, Optimize, sat

sys.setrecursionlimit(10000)


FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/19"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/19_test"
#


def solve():
    print(f"Using file {FILE}")

    blueprints = []
    with open(FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            _, recipe = line.strip().split(":")
            r = []
            for part in recipe.strip().split(".")[:-1]:
                words = part.strip().split()
                costs = [0, 0, 0]
                if len(words) > 6:
                    costs[0] = int(words[4])
                    if words[8] == "clay":
                        costs[1] = int(words[7])
                    else:
                        costs[2] = int(words[7])
                else:
                    costs[0] = int(words[4])
                r.append(costs)

            blueprints.append(r)

        # print(blueprints)

    def solve(blueprint, max_minutes):
        # Amount of ore at each timestamp
        or_ = [Int("or_{}".format(i)) for i in range(max_minutes + 1)]
        # Amount of clay at each timestamp
        cl_ = [Int("cl_{}".format(i)) for i in range(max_minutes + 1)]
        # Amount of obsidian at each timestamp
        ob_ = [Int("ob_{}".format(i)) for i in range(max_minutes + 1)]
        # Amount of Geode at each timestamp
        ge_ = [Int("ge_{}".format(i)) for i in range(max_minutes + 1)]

        # Amount of ore robots(s) at each timestamp
        or_robot = [Int("or_robot_  {}".format(i)) for i in range(max_minutes + 1)]
        # Amount of clay robots(s) at each timestamp
        cl_robot = [Int("cl_robot_  {}".format(i)) for i in range(max_minutes + 1)]
        # Amount of obsidian robots(s) at each timestamp
        ob_robot = [Int("ob_robot_{}".format(i)) for i in range(max_minutes + 1)]
        # Amount of Geode robot at each timestamp
        ge_robot = [Int("ge_robot_{}".format(i)) for i in range(max_minutes + 1)]

        # Amount of ore robots(s) bought at each timestamp
        buy_or_robot = [
            Int("buy_or_robot_{}".format(i)) for i in range(max_minutes + 1)
        ]
        # Amount of clay robots(s) bought at each timestamp
        buy_cl_robot = [
            Int("buy_cl_robot_{}".format(i)) for i in range(max_minutes + 1)
        ]
        # Amount of obsidian robots(s) bought at each timestamp
        buy_ob_robot = [
            Int("buy_ob_robot_{}".format(i)) for i in range(max_minutes + 1)
        ]
        # Amount of Geode robots(s) bought at each timestamp
        buy_ge_robot = [
            Int("buy_ge_robot_{}".format(i)) for i in range(max_minutes + 1)
        ]

        # Constraints
        constraints = []

        # Initial amount of minerals is 0
        constraints.append(or_[0] == 0)
        constraints.append(cl_[0] == 0)
        constraints.append(ob_[0] == 0)
        constraints.append(ge_[0] == 0)

        # At each timestamp, the amount of mineral is the previous amount plus the income from the robots minus the cost of buying a new robot
        for i in range(1, max_minutes + 1):
            # Amount of ore at each timestamp
            constraints.append(
                or_[i]
                == or_[i - 1]
                + or_robot[i - 1]
                - (buy_or_robot[i]) * blueprint[0][0]
                - (buy_cl_robot[i]) * blueprint[1][0]
                - (buy_ob_robot[i]) * blueprint[2][0]
                - (buy_ge_robot[i]) * blueprint[3][0]
            )

            constraints.append(
                cl_[i]
                == cl_[i - 1]
                + cl_robot[i - 1]
                - (buy_or_robot[i]) * blueprint[0][1]
                - (buy_cl_robot[i]) * blueprint[1][1]
                - (buy_ob_robot[i]) * blueprint[2][1]
                - (buy_ge_robot[i]) * blueprint[3][1]
            )

            constraints.append(
                ob_[i]
                == ob_[i - 1]
                + ob_robot[i - 1]
                - (buy_or_robot[i]) * blueprint[0][2]
                - (buy_cl_robot[i]) * blueprint[1][2]
                - (buy_ob_robot[i]) * blueprint[2][2]
                - (buy_ge_robot[i]) * blueprint[3][2]
            )

            constraints.append(ge_[i] == ge_[i - 1] + ge_robot[i - 1])

        # Can take a new robot if the amount of minerals is enough
        for i in range(1, max_minutes + 1):
            constraints.append(or_robot[i] == or_robot[i - 1] + buy_or_robot[i - 1])
            constraints.append(cl_robot[i] == cl_robot[i - 1] + buy_cl_robot[i - 1])
            constraints.append(ob_robot[i] == ob_robot[i - 1] + buy_ob_robot[i - 1])
            constraints.append(ge_robot[i] == ge_robot[i - 1] + buy_ge_robot[i - 1])

        for i in range(1, max_minutes + 1):
            # Can only buy one robot at a time
            constraints.append(buy_or_robot[i] >= 0)
            constraints.append(buy_cl_robot[i] >= 0)
            constraints.append(buy_ob_robot[i] >= 0)
            constraints.append(buy_ge_robot[i] >= 0)
            constraints.append(buy_or_robot[i] <= 1)
            constraints.append(buy_cl_robot[i] <= 1)
            constraints.append(buy_ob_robot[i] <= 1)
            constraints.append(buy_ge_robot[i] <= 1)

            constraints.append(
                buy_or_robot[i] + buy_cl_robot[i] + buy_ob_robot[i] + buy_ge_robot[i]
                <= 1
            )

            # No credit allowed
            constraints.append(or_[i] >= 0)
            constraints.append(cl_[i] >= 0)
            constraints.append(ob_[i] >= 0)
            constraints.append(ge_[i] >= 0)

            # Can only increase the amount of robots
            constraints.append(or_robot[i] >= or_robot[i - 1])
            constraints.append(cl_robot[i] >= cl_robot[i - 1])
            constraints.append(ob_robot[i] >= ob_robot[i - 1])
            constraints.append(ge_robot[i] >= ge_robot[i - 1])

        # Start with one ore robot
        constraints.append(or_robot[0] == 1)
        constraints.append(cl_robot[0] == 0)
        constraints.append(ob_robot[0] == 0)
        constraints.append(ge_robot[0] == 0)

        # Factory does not produce on day 0
        constraints.append(buy_or_robot[0] == 0)
        constraints.append(buy_cl_robot[0] == 0)
        constraints.append(buy_ob_robot[0] == 0)
        constraints.append(buy_ge_robot[0] == 0)

        # Start with no mineral
        constraints.append(or_[0] == 0)
        constraints.append(cl_[0] == 0)
        constraints.append(ob_[0] == 0)
        constraints.append(ge_[0] == 0)

        # Objective: maximize the amount of geode at time max_minutes=100
        objective = ge_[max_minutes]

        # Solve the problem
        solver = Optimize()
        solver.add(constraints)
        solver.maximize(objective)
        # solver.set_objective(objective)
        if solver.check() == sat:
            model = solver.model()
            # print("The maximum amount of geodes is {}".format(model[ge_[max_minutes]]))
            # for i in range(max_minutes + 1):
            #     print(
            #         f"{i:2d}",
            #         f"{str(model[or_[i]]).rjust(2, ' ')}",
            #         f"{str(model[cl_[i]]).rjust(2, ' ')}",
            #         f"{str(model[ob_[i]]).rjust(2, ' ')}",
            #         f"{str(model[ge_[i]]).rjust(2, ' ')}",
            #         "---",
            #         f"{str(model[buy_or_robot[i]]).rjust(2, ' ')}",
            #         f"{str(model[buy_cl_robot[i]]).rjust(2, ' ')}",
            #         f"{str(model[buy_ob_robot[i]]).rjust(2, ' ')}",
            #         f"{str(model[buy_ge_robot[i]]).rjust(2, ' ')}",
            #         "---",
            #         f"{str(model[or_robot[i]]).rjust(2, ' ')}",
            #         f"{str(model[cl_robot[i]]).rjust(2, ' ')}",
            #         f"{str(model[ob_robot[i]]).rjust(2, ' ')}",
            #         f"{str(model[ge_robot[i]]).rjust(2, ' ')}",
            #     )
            return model[ge_[max_minutes]].as_long()
        raise Exception("No solution found")

    def part1(blueprint, max_time):
        p1 = 0

        for i in range(len(blueprints)):
            b = solve(
                blueprints[i],
                24,
            )
            p1 += b * (i + 1)

        return p1

    def part2(blueprints, max_time):
        p2 = 1
        for i in range(3):
            b = solve(
                blueprints[i],
                32,
            )
            p2 *= b

        return p2

    ti = time.time()
    print(f"Part one: {part1(blueprints, 24)}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(blueprints, 32)}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
