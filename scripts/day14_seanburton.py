rock = set()

max_y = 0
offset = 0

for lines in open("inputs/2022/14"):
    x, y = map(int, lines.split(", "))
    rock.add((x, y))
    max_y = max(max_y, y)

sand = set()


def g(x, y):
    p = (x, y)
    if p in rock or p in sand or y == max_y + 1:
        return
    qs = [(x + dx, y + 1) for dx in (0, -1, 1)]
    for q in qs:
        g(*q)
        if not (q in sand or q in rock):
            return
    sand.add(p)


def f(x, y):
    p = (x, y)
    if p in rock or p in sand or y == max_y + 2:
        return
    f(x + 0, y + 1)
    f(x - 1, y + 1)
    f(x + 1, y + 1)
    sand.add(p)


f(500, 0)
print(len(sand))

offset = 2

f(500, 0)
