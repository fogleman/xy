from collections import defaultdict
from math import hypot

class Index(object):
    def __init__(self, points, n=100):
        self.points = points
        self.n = n
        self.x1 = min(x for x, y in points)
        self.x2 = max(x for x, y in points)
        self.y1 = min(y for x, y in points)
        self.y2 = max(y for x, y in points)
        self.bins = defaultdict(list)
        for x, y in points:
            self.insert(x, y)
    def normalize(self, x, y):
        px = (x - self.x1) / (self.x2 - self.x1)
        py = (y - self.y1) / (self.y2 - self.y1)
        i = int(round(px * self.n))
        j = int(round(py * self.n))
        return (i, j)
    def insert(self, x, y):
        i, j = self.normalize(x, y)
        self.bins[(i, j)].append((x, y))
    def remove(self, x, y):
        i, j = self.normalize(x, y)
        self.bins[(i, j)].remove((x, y))
    def search(self, x, y):
        i, j = self.normalize(x, y)
        r = 0
        points = self.load_ring(i, j, 0)
        while r <= 1 or not points:
            points.extend(self.load_ring(i, j, r))
            r += 1
        return min(points, key=lambda (px, py): hypot(x - px, y - py))
    def load_ring(self, i, j, r):
        result = []
        for p in range(i - r, i + r + 1):
            result.extend(self.bins[(p, j - r)])
            result.extend(self.bins[(p, j + r)])
        for q in range(j - r + 1, j + r):
            result.extend(self.bins[(i - r, q)])
            result.extend(self.bins[(i + r, q)])
        return result

if __name__ == '__main__':
    import random
    points = []
    for _ in range(1000):
        x = random.random()
        y = random.random()
        points.append((x, y))
    index = Index(points)
    x = random.random()
    y = random.random()
    print (x, y)
    print index.search(x, y)
