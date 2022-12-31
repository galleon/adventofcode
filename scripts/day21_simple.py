#!/bin/python3

import sys
import time

from z3 import *

# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/21_test"
FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/21"


def solve():
    print(f"Using file {FILE}")
    lines = []
    with open(FILE, "r", encoding="utf-8") as f:
        for line in f:
            lines.append(line.strip())

    def part1(lines):
        solver = Solver()
        vars = {}
        for i, line in enumerate(lines):
            left, right = line.split(": ")
            op0 = f"{left}"
            if op0 not in vars.keys():
                vars[op0] = Int(op0)
            right = right.split()
            if len(right) == 3:
                op1 = f"{right[0]}"
                op_ = right[1]
                op2 = f"{right[2]}"
                if op1 not in vars.keys():
                    vars[op1] = Int(op1)
                if op2 not in vars.keys():
                    vars[op2] = Int(op2)
                if op_ == "+":
                    solver.add(vars[op0] == vars[op1] + vars[op2])
                elif op_ == "*":
                    solver.add(vars[op0] == vars[op1] * vars[op2])
                elif op_ == "-":
                    solver.add(vars[op0] == vars[op1] - vars[op2])
                elif op_ == "/":
                    solver.add(vars[op0] == vars[op1] / vars[op2])
                else:
                    print("error operator unknown")
            elif len(right) == 1:
                v = int(right[0])
                solver.add(vars[op0] == v)

        checked = solver.check()

        if checked == sat:
            model = solver.model()
            return model[vars["root"]].as_long()

        raise Exception("No solution found")

    def part2(line):
        # Initial conditions
        solver = Optimize()
        vars = {}
        for i, line in enumerate(lines):
            left, right = line.split(": ")
            op0 = f"{left}"
            if op0 != "humn" and op0 not in vars.keys():
                vars[op0] = Int(op0)
            right = right.split(" ")
            if len(right) == 3:

                op1 = f"{right[0]}"
                op_ = right[1]
                op2 = f"{right[2]}"

                if op0 == f"root":
                    solver.add(vars[op1] == vars[op2])
                else:
                    if op1 not in vars.keys():
                        vars[op1] = Int(op1)
                    if op2 not in vars.keys():
                        vars[op2] = Int(op2)
                    if op_ == "+":
                        solver.add(vars[op0] == vars[op1] + vars[op2])
                    elif op_ == "*":
                        solver.add(vars[op0] == vars[op1] * vars[op2])
                    elif op_ == "-":
                        solver.add(vars[op0] == vars[op1] - vars[op2])
                    elif op_ == "/":
                        solver.add(vars[op0] == vars[op1] / vars[op2])
                    else:
                        print("error operator unknown")
            elif len(right) == 1 and op0 != "humn":
                v = int(right[0])
                solver.add(vars[op0] == v)

        checked = solver.check()

        if checked == sat:
            model = solver.model()
            return model[vars["humn"]].as_long()

        raise Exception("No solution found")

    ti = time.time()
    print(f"Part one: {part1(lines)}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2(lines)}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
