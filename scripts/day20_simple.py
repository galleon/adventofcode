#!/bin/python3
import sys
import time

from collections import Counter

# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/20_pilou"
FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/20"
# FILE = sys.argv[1] if len(sys.argv) > 1 else "inputs/2022/20_test"
#


class Node:
    def __init__(self, value, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right


class LinkedList:
    def __init__(self):
        self.head = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        current_node = self.head
        while current_node.next:
            current_node = current_node.next
        current_node.next = new_node


def solve():
    print(f"Using file {FILE}")

    def get_l():
        l = []
        with open(FILE, "r", encoding="utf-8") as f:
            for line in f:
                l.append(Node(int(line.strip())))

        for x, y in zip(l, l[1:]):
            x.right = y
            y.left = x

        l[0].left = l[-1]
        l[-1].right = l[0]

        return l

    def solve(l):
        for x in l:
            # Find the element with value 0
            if x.value == 0:
                r = 0
                y = x
                # Find 1000th, 2000th and 3000th elements
                for _ in range(3):
                    for _ in range(1000):
                        y = y.right
                    r += y.value
                return r

    def show(l):
        for x in l:
            if x.value == 0:
                y = x.right
                while y.value != 0:
                    print(y.value)
                    y = y.right

    def mixing(l, times=1, showme=False):
        for _ in range(times):
            for x in l:
                # Remove each element one at a time
                x.left.right = x.right
                x.right.left = x.left
                a, b = x.left, x.right

                # Find the destination
                move = x.value % (len(l) - 1)

                # Move to the insertion destination
                for _ in range(move):
                    a = a.right
                    b = b.right

                # Insert the element
                a.right = x
                x.left = a
                b.left = x
                x.right = b

        if showme:
            show(l)

        return l

    def part1():
        return solve(mixing(get_l(), showme=False))

    def part2():
        l = get_l()

        for x in l:
            x.value *= 811589153

        return solve(mixing(l, 10))

    ti = time.time()
    print(f"Part one: {part1()}")
    print(f"Time: {time.time() - ti:.2f}s")
    ti = time.time()
    print(f"Part two: {part2()}")
    print(f"Time: {time.time() - ti:.2f}s")


if __name__ == "__main__":
    solve()
