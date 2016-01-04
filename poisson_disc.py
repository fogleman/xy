from math import pi, sin, cos, hypot, floor
from shapely.geometry import LineString
import random

class Grid(object):
    def __init__(self, r):
        self.r = r
        self.size = r / 2 ** 0.5
        self.points = {}
        self.lines = {}
    def normalize(self, x, y):
        i = int(floor(x / self.size))
        j = int(floor(y / self.size))
        return (i, j)
    def nearby(self, x, y):
        points = []
        lines = []
        i, j = self.normalize(x, y)
        for p in range(i - 2, i + 3):
            for q in range(j - 2, j + 3):
                if (p, q) in self.points:
                    points.append(self.points[(p, q)])
                if (p, q) in self.lines:
                    lines.append(self.lines[(p, q)])
        return points, lines
    def insert(self, x, y, line=None):
        points, lines = self.nearby(x, y)
        for bx, by in points:
            if hypot(x - bx, y - by) < self.r:
                return False
        i, j = self.normalize(x, y)
        if line:
            for other in lines:
                if line.crosses(other):
                    return False
            self.lines[(i, j)] = line
        self.points[(i, j)] = (x, y)
        return True
    def remove(self, x, y):
        i, j = self.normalize(x, y)
        self.points.pop((i, j))
        self.lines.pop((i, j))

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
    while active:
        ax, ay, aa, ad = record = random.choice(active)
        for i in range(n):
            # a = random.random() * 2 * pi
            # a = aa + (random.random() - 0.5) * pi / 2
            a = random.gauss(aa, pi / 8)
            d = random.random() * r + r
            x = ax + cos(a) * d
            y = ay + sin(a) * d
            if x < x1 or y < y1 or x > x2 or y > y2:
                continue
            pair = ((ax, ay), (x, y))
            line = LineString(pair)
            if not grid.insert(x, y, line):
                continue
            pairs.append(pair)
            active.append((x, y, a, ad + d))
            break
        else:
            active.remove(record)
    return grid.points.values(), pairs
