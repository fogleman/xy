from math import pi, sin, cos, hypot, floor
from shapely.geometry import LineString
import random

class Grid(object):
    def __init__(self, r):
        self.r = r
        self.size = r / 2 ** 0.5
        self.cells = {}
    def points(self):
        return self.cells.values()
    def normalize(self, x, y):
        i = int(floor(x / self.size))
        j = int(floor(y / self.size))
        return (i, j)
    def nearby(self, x, y):
        result = []
        i, j = self.normalize(x, y)
        for p in xrange(i - 2, i + 3):
            for q in xrange(j - 2, j + 3):
                if (p, q) in self.cells:
                    result.append(self.cells[(p, q)])
        return result
    def insert(self, x, y):
        for bx, by in self.nearby(x, y):
            if hypot(x - bx, y - by) < self.r:
                return False
        i, j = self.normalize(x, y)
        self.cells[(i, j)] = (x, y)
        return True
    def remove(self, x, y):
        i, j = self.normalize(x, y)
        self.cells.pop((i, j))

def check_pairs(line, lines):
    for other in lines:
        if line.crosses(other):
            return False
    return True

def poisson_disc(x1, y1, x2, y2, r, n):
    grid = Grid(r)
    active = []
    for _ in range(64):
        x = x1 + random.random() * (x2 - x1)
        y = y1 + random.random() * (y2 - y1)
        a = random.random() * 2 * pi
        if grid.insert(x, y):
            active.append((x, y, a, 0))
    pairs = []
    lines = []
    while active:
        ax, ay, aa, ad = random.choice(active)
        for i in xrange(n):
            # a = random.random() * 2 * pi
            a = aa + (random.random() - 0.5) * pi / 2
            d = random.random() * r + r
            x = ax + cos(a) * d
            y = ay + sin(a) * d
            if x < x1 or y < y1 or x > x2 or y > y2:
                continue
            if not grid.insert(x, y):
                continue
            pair = ((ax, ay), (x, y))
            line = LineString(pair)
            # if not check_pairs(line, lines):
            #     grid.remove(x, y)
            #     continue
            pairs.append(pair)
            lines.append(line)
            active.append((x, y, a, ad + d))
            break
        else:
            active.remove((ax, ay, aa, ad))
    return grid.points(), pairs
