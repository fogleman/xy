from device import Device
from math import sin, cos, pi, hypot
from poisson_disc import poisson_disc
import random
import time
import util

PEN_UP = 0
PEN_DOWN = 40

def circle(cx, cy, r, n):
    result = []
    for i in range(n + 1):
        p = i / float(n)
        a = 2 * pi * p
        x = cx + cos(a) * r
        y = cy + sin(a) * r
        result.append((x, y))
    return result

def main():
    mm = 25.4
    w = 11 * mm
    h = 8.5 * mm
    p = 0.5 * mm
    s = 0.25 * mm
    points = poisson_disc(p, p, w - p * 2, h - p * 2, s, 32)
    points = util.sort_points(points)
    print len(points)
    device = Device('/dev/tty.wchusbserial1420')
    time.sleep(3)
    device.pen(PEN_UP)
    device.home()
    for cx, cy in points:
        r = (0.03125 + random.random() * 0.0625) * mm
        c = circle(cx, cy, r, 36)
        device.move(*c[0])
        device.pen(PEN_DOWN)
        for x, y in c:
            device.move(x, y)
        device.pen(PEN_UP)
    device.home()

if __name__ == '__main__':
    main()
