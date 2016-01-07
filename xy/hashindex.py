from collections import defaultdict
from math import hypot

class Index(object):
    def __init__(self, points, n=100):
        self.n = n
        self.x1 = min(pt[0] for pt in points)
        self.x2 = max(pt[0] for pt in points)
        self.y1 = min(pt[1] for pt in points)
        self.y2 = max(pt[1] for pt in points)
        self.bins = defaultdict(list)
        self.size = 0
        for point in points:
            self.insert(point)
    def normalize(self, x, y):
        px = (x - self.x1) / (self.x2 - self.x1)
        py = (y - self.y1) / (self.y2 - self.y1)
        i = int(round(px * self.n))
        j = int(round(py * self.n))
        return (i, j)
    def insert(self, point):
        x, y = point[:2]
        i, j = self.normalize(x, y)
        self.bins[(i, j)].append(point)
        self.size += 1
    def remove(self, point):
        x, y = point[:2]
        i, j = self.normalize(x, y)
        self.bins[(i, j)].remove(point)
        self.size -= 1
    def search(self, point):
        x, y = point[:2]
        i, j = self.normalize(x, y)
        points = []
        r = 0
        while not points:
            points.extend(self.load_ring(i, j, r))
            r += 1
        points.extend(self.load_ring(i, j, r))
        return min(points, key=lambda pt: (hypot(x - pt[0], y - pt[1]), pt[0], pt[1]))
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
    for i in range(1000):
        x = random.random()
        y = random.random()
        points.append((x, y, i))
    index = Index(points)
    x = random.random()
    y = random.random()
    print (x, y)
    print index.search((x, y))
