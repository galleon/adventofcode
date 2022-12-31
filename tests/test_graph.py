from aoc.data import Graph


def test_paths():
    g = Graph()
    g.add(1, 2)
    g.add(1, 3)
    g.add(2, 1)
    g.add(2, 3)
    g.add(3, 1)
    g.add(3, 2)

    paths = g.find_paths(1, 3)

    assert len(paths) == 2
