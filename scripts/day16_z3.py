#!/bin/python3

import functools
import sys
import time

import networkx as nx
from z3 import (
    Abs,
    And,
    BitVec,
    Bool,
    Distinct,
    Exists,
    EnumSort,
    ForAll,
    If,
    Implies,
    Int,
    Not,
    Or,
    Solver,
    sat,
    unsat,
    Ints,
)

sys.setrecursionlimit(10000)

FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/16"


def solve():
    print(f"Using file {FILE}")

    valves = {}
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip().split(" ")
            name = line[1]
            rate = int(line[4].split("=")[-1].split(";")[0])

            valves[name] = {
                "rate": rate,
                "tunnels": [word.split(",")[0] for word in line[9:]],
                "paths": {},
            }

    def bfs(frontier, end):
        depth = 1
        while True:
            next_frontier = set()
            for node in frontier:
                if node == end:
                    return depth
                next_frontier.update(valves[node]["tunnels"])
            frontier = next_frontier
            depth += 1

    def part1(time, start):
        # Consider only valves that generate flow (i.e. rate > 0)
        keys = sorted([x for x in valves if valves[x]["rate"] > 0] + ["AA"])

        # Compute costs to reach each key from each other key
        costs = [[0] * len(keys) for _ in range(len(keys))]

        for k1 in keys:
            for k2 in keys:
                if k1 == k2:
                    valves[k1]["paths"][k2] = 0
                else:
                    valves[k1]["paths"][k2] = bfs(valves[k1]["tunnels"], k2)

        for i, k1 in enumerate(keys):
            for j, k2 in enumerate(keys):
                costs[i][j] = valves[k1]["paths"][k2]

        flow = [valves[k]["rate"] for _, k in enumerate(keys)]

        print(valves)
        print(keys)
        print(costs)
        print(flow)

        max_path_length = len(keys) - 1
        nplayers = 1

        # x[i][j][k] = True if player k opens valve i at time j
        x = [
            [
                [Bool(f"open_valve_{v}_at_time_{t}_by_{p}") for v in range(len(keys))]
                for t in range(time)
            ]
            for p in range(nplayers)
        ]

        for p in range(players):
            for t1 in range(time):
                for v1 in range(len(keys)):
                    for v2 in range(len(keys)):
                        for t2 in range(t, time):
                            if v1 == v2:
                                continue
                            open_penalty = 0
                            if v1 == 0:
                                open_penalty = 1
                            if t2 - open_penalty - t1 < costs[v1][v2]:
                                # Only one of both valves can be open
                                solver.add(And(x[v1][t1][p], x[v2][t2][p]))

        for p in range(nplayers):
            solver.add(x[p][0][0] == True)

        # if a valve is open, it must be open for the entire time
        for v in range(len(keys)):
            for t1 in range(time):
                for t2 in range(t1 + 1, time):
                    for p in range(players):
                        solver.add(Implies(x[v][t1][p], x[v][t2][p]))

        # we cannot only open a single valve at a timestep
        for p in range(players):
            for t in range(time):
                # We can only open a single valve at a timestep
                m += xsum(x[i, t, u] for i in range(1, len(valves))) <= 1
                for i in range(1, len(valves)):
                    # Cannot open the same valve with all palyers
                    m += xsum(x[i, t, u] for u in range(players)) <= 1

        total_flow_released = {}
        for v in range(len(keys)):
            for t1 in range(time):
                total_flow_released[str([valve["id"], t])] = (
                    max(0, time - t1 - 1) * valve["flow"]
                )
                for t2 in range(t1 + 1, time):
                    for p1 in range(players):
                        for p2 in range(players):
                            m += x[valve["id"], t, u1] + x[valve["id"], t2, u2] <= 1

        total_flow_released = Sum(
            If(x[v][t][p], flow[v], True)
            for v in range(len(keys))
            for t in range(time)
            for p in range(players)
        )
        solver.add(total_flow_released == time)

        best = None
        iter = 0
        while True:
            iter += 1
            solver = Solver()

            solver.add(Distinct(position))
            # All positions are in the range of keys
            for i in range(max_path_length):
                solver.add(position[i] >= 0, position[i] < len(keys))

            total_flowrate = sum(
                flowrate[i] for i in position for t in range(max_path_length)
            )
            if best:
                solver.add(total_flowrate > best)

            check = solver.check()
            if check == sat:
                print(f"[{check}] so far best is: {best}")
                best = solver.model().eval(total_flowrate).as_long()
            else:
                return best

        return 0

    def part2(time, start):
        players = 2

        return 0

    ti = time.time()
    print(f"Part one: {part1(30, 'AA')}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(26, 'AA')}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
