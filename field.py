from device import Device
from math import hypot, atan2, sin, cos, pi
import random
import time

PEN_UP = 0
PEN_DOWN = 40

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
            angle = atan2(y - py, x - px)
            dx += pm * cos(angle) / d
            dy += pm * sin(angle) / d
        angle = atan2(dy, dx) + pi / 2
        dx = cos(angle)
        dy = sin(angle)
        return (dx, dy)

def points(sides):
    x = 0.5
    y = 0.5
    rotation = 0
    angle = 2 * pi / sides
    rotation = rotation - pi / 2
    angles = [angle * i + rotation for i in range(sides)]
    d = 0.35
    return [(x + cos(a) * d, y + sin(a) * d) for a in angles]

def create_path(model, scale):
    result = []
    n = 256
    f = 1 / 1024.0
    x = random.random()
    y = random.random()
    for j in range(n):
        result.append((x * scale, y * scale))
        dx, dy = model.test(x, y)
        x += dx * f
        y += dy * f
        if x < 0 or y < 0 or x > 1 or y > 1:
            break
    return result

def main():
    device = Device('/dev/tty.wchusbserial1420')
    time.sleep(3)
    device.pen(PEN_UP)
    device.home()
    scale = 200
    model = Model()
    for x, y in points(5):
        model.add(x, y)
    model.add(0.5, 0.5, 0.1)
    while True:
        path = create_path(model, scale)
        device.draw(path, PEN_UP, PEN_DOWN)

if __name__ == '__main__':
    main()
