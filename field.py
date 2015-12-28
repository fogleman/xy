from device import Device
from math import hypot, atan2, sin, cos, pi
from poisson_disc import poisson_disc
import planner
import random
import time
import util

PEN_UP = 20
PEN_DOWN = 60

class Model(object):
    def __init__(self):
        self.particles = []
    def add(self, x, y, m=1.0):
        self.particles.append((x, y, m))
    def test(self, x, y):
        dx = 0
        dy = 0
        for px, py, pm in self.particles:
            d = hypot(x - px, y - py)
            if abs(d) < 1e-8:
                return (0, 0)
            angle = atan2(y - py, x - px)
            dx += pm * cos(angle) / d
            dy += pm * sin(angle) / d
        angle = atan2(dy, dx) + pi / 2
        dx = cos(angle)
        dy = sin(angle)
        return (dx, dy)

def polygon(sides, d):
    x = 0.5
    y = 0.5
    rotation = 0
    angle = 2 * pi / sides
    angles = [angle * i + rotation for i in range(sides)]
    return [(x + cos(a) * d, y + sin(a) * d) for a in angles]

def create_path(model, scale, ox, oy, x, y, m, length):
    result = []
    n = int(length * 32)
    f = float(length) / scale / n
    for j in range(n):
        result.append((ox + x * scale, oy + y * scale))
        dx, dy = model.test(x, y)
        x += dx * f * m
        y += dy * f * m
        if x < 0 or y < 0 or x > 1 or y > 1:
            break
    return result

def main():
    device = Device('/dev/tty.wchusbserial640')
    time.sleep(2)
    device.pen(PEN_UP)
    time.sleep(1)
    device.home()
    model = Model()
    for x, y in polygon(5, 0.35):
        model.add(x, y, 1)
    model.add(0.5, 0.5, 0.1)
    total = 0
    while True:
        paths = []
        print 'generating paths'
        for _ in range(100):
            x = random.random()
            y = random.random()
            path = create_path(model, 315, 0, 0, x, y, 1, 100)
            path = util.simplify(path)
            paths.append(path)
        print 'optimizing path ordering'
        paths = planner.order_paths(paths)
        print 'drawing paths'
        for path in paths:
            total += 1
            print '%5d: %2d points @ (%.3f, %.3f)' % (
                total, len(path), path[0][0], path[0][1])
            device.draw(path, PEN_UP, PEN_DOWN)

if __name__ == '__main__':
    main()
