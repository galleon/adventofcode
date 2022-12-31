import numpy as np
from collections import defaultdict


class Graph(object):
    """Graph data structure, undirected by default."""

    def __init__(self, start=None, destination=None, connections=[], directed=False):
        self._start = start
        self._destination = destination
        self._graph = defaultdict(set)
        self._directed = directed
        self.add_connections(connections)

    def add_connections(self, connections):
        """Add connections (list of tuple pairs) to graph"""

        for node1, node2 in connections:
            self.add(node1, node2)

    def add(self, node1, node2):
        """Add connection between node1 and node2"""

        self._graph[node1].add(node2)
        if not self._directed:
            self._graph[node2].add(node1)

    def remove(self, node):
        """Remove all references to node"""

        for n, cxns in self._graph.items():  # python3: items(); python2: iteritems()
            try:
                cxns.remove(node)
            except KeyError:
                pass
        try:
            del self._graph[node]
        except KeyError:
            pass

    def is_connected(self, node1, node2):
        """Is node1 directly connected to node2"""

        return node1 in self._graph and node2 in self._graph[node1]

    def find_paths(self, start, end, path=[]):
        path = path + [start]
        if start == end:
            return [path]
        if start not in self:
            return []
        paths = []
        for node in self._graph[start]:
            if node not in path:
                new_paths = self.find_paths(node, end, path)
                for new_path in new_paths:
                    paths.append(new_path)
        return paths

    def count_paths(self, start, visited=defaultdict(int), twice=None):
        """Count all paths from start to end"""

        # if start is the end, return 1
        if start == self._destination:
            return 1

        if start == self._start and visited[start] > 0:
            return 0

        # if start has already been visited, return 0
        if visited[start] > 0:
            return 0

        # Add 1 to visited for start
        visited[start] += 1

        result = 0
        for node in self._graph[start]:
            result += self.count_paths(node, defaultdict(int, visited), twice)

        return result

    def count_paths_12(self, start, visited=defaultdict(int), twice=None):
        # if start is the end, return 1
        if start == self._destination:
            return 1

        # if start has already been visited, return 0
        if visited[start] > 0:
            return 0

        # Add 1 to visited for start only if lowercase (upper case node can be visited multiple times)
        if start.islower():
            visited[start] += 1

        result = 0
        for node in self._graph[start]:
            result += self.count_paths_12(node, defaultdict(int, visited), twice)

        return result

    def count_paths_12_(self, start, end="end", visited=defaultdict(int), twice=None):
        # if start is the end, return 1
        if start == end:
            return 1

        if start == self._start and visited[start] > 0:
            return 0

        # if start has already been visited, return 0
        if visited[start] > 0:
            if twice is None:
                twice = start
            else:
                return 0

        # Add 1 to visited for start only if lowercase (upper case node can be visited multiple times)
        if start.islower():
            visited[start] += 1

        result = 0
        for node in self._graph[start]:
            result += self.count_paths_12_(node, end, defaultdict(int, visited), twice)

        return result

    def __contains__(self, item):
        return item in self._graph

    def __str__(self):
        return self._graph.__str__()


class Board:

    cardinals = {
        "E": (-1, 0),
        "W": (1, 0),
        "S": (0, -1),
        "N": (0, 1),
        "NE": (-1, 1),
        "NW": (1, 1),
        "SE": (1, -1),
        "SW": (-1, -1),
    }

    def __init__(self, width=0, height=0, operator=int):
        self._width = width
        self._height = height
        self._kv = {}
        self._kv_ghost = {}
        self._operator = operator

    @staticmethod
    def from_text(values, operator=str):
        board = Board(operator=operator)
        if isinstance(values, str):
            if "\n" in values:
                values = values.split("\n")
            else:
                values = [values]
        y = 0
        for row in values:
            x = 0
            for c in row:
                board._kv[(x, y)] = operator(c)
                x += 1
            y += 1
        board._width = x
        board._height = y
        return board

    def __getitem__(self, xy):
        if self._operator is int:
            return self._kv.get(xy, 0)
        else:
            return self._kv.get(xy, " ")

    def __setitem__(self, xy, value):
        # print(f"Setting {xy} to {value} as {type(value)}")
        self._kv[xy] = value
        if xy[0] > self._width:
            self._width = xy[0]
        if xy[1] > self._height:
            self._height = xy[1]

    def __delitem__(self, key):
        del self._kv[key]

    def __iter__(self):
        return iter(self._kv)

    def __contains__(self, key):
        return key in self._kv

    def __str__(self):
        table = ""
        for j in range(max(y for _, y in self._kv) + 1):
            for i in range(max(x for x, _ in self._kv) + 1):
                table += str(self[(i, j)])
            table += "\n"
        # table = table.replace("0", ".")
        return table

    def max(self):
        return max(self._kv.values())

    def min(self):
        return min(self._kv.values())

    def sum_all(self, ghost=False):
        if ghost:
            return sum(map(int, self._kv_ghost.values()))
        else:
            return sum(map(int, self._kv.values()))

    def move_to_ghost(self, value):
        for k, v in dict(self._kv).items():
            # print(v, type(v), value, type(value))
            if v == value:
                del self._kv[k]
                self._kv_ghost[k] = value

    def is_winning(self):
        cols = [0] * self._width
        rows = [0] * self._height
        for k, v in self._kv_ghost.items():
            rows[k[0]] += 1
            if rows[k[0]] == self._width:
                return True
            cols[k[1]] += 1
            if cols[k[1]] == self._height:
                return True

        return False

    def is_empty(self):
        return len(self._kv) == 0

    def neighbors(self, x, y, diagonals=False, valid_only=False):
        offsets = ((0, -1), (1, 0), (0, 1), (-1, 0))
        if diagonals:
            offsets = (
                (-1, -1),
                (-1, 0),
                (-1, 1),
                (0, -1),
                (0, 1),
                (1, -1),
                (1, 0),
                (1, 1),
            )

        for ox, oy in offsets:
            ox = ox + x
            oy = oy + y
            if not valid_only or (ox, oy) in self._kv:
                yield ox, oy

    def unfold(self, axis: str):
        assert axis in ("x", "y")

        new_b = Board()
        pos = self._height if axis == "y" else self._width

        for (i, j), v in self._kv.items():
            if axis == "y":
                new_b[(i, j)] = v
                new_b[(i, pos + pos - j)] = v
            else:
                new_b[(pos + pos - i, j)] = v

        return new_b
