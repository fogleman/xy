from math import sin, cos, pi, hypot
from poisson_disc import poisson_disc
import random
import time
import xy

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
    points = xy.sort_points(points)
    print len(points)
    device = xy.Device()
    time.sleep(3)
    device.pen_up()
    device.home()
    for cx, cy in points:
        r = (0.03125 + random.random() * 0.0625) * mm
        device.draw(circle(cx, cy, r, 36))
    device.home()

if __name__ == '__main__':
    main()
