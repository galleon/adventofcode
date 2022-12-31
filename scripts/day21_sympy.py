# code by @Flo

import re

from sympy import nsolve, symbols, simplify
from sympy.parsing.sympy_parser import parse_expr
from time import time

monkey_dir = dict(m.split(": ") for m in open("inputs/2022/21").read().splitlines())


def find_children(key):
    if len(re.findall("[+-/*]", monkey_dir[key])) == 0:
        return monkey_dir[key]
    a, o, b = monkey_dir[key].split()
    return "(" + find_children(a) + o + find_children(b) + ")"


ti = time()
print(int(eval(find_children("root"))))
print(f"Time: {time() - ti:.2f}s")


print(monkey_dir["root"])

monkey_dir["root"] = re.sub("[+/*]+", "-", monkey_dir["root"])
monkey_dir["humn"] = "x"
x = symbols("x")

ti = time()
expr = parse_expr(find_children(key="root"))
print(expr)
print(int(nsolve(expr, 0)))
print(f"Time: {time() - ti:.2f}s")
