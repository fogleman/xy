from math import sin, cos, e, pi
import xy

def butterfly(t):
    x = sin(t) * (pow(e, cos(t)) - 2 * cos(4 * t) - pow(sin(t / 12), 5))
    y = cos(t) * (pow(e, cos(t)) - 2 * cos(4 * t) - pow(sin(t / 12), 5))
    return (x, y)

def times(t0, t1, n):
    result = []
    for i in range(n):
        p = i / float(n - 1)
        t = t0 + (t1 - t0) * p
        result.append(t)
    return result

def main():
    t0 = 0
    t1 = pi * 24
    n = 100000
    path = [butterfly(t) for t in times(t0, t1, n)]
    drawing = xy.Drawing([path]).scale_to_fit(315, 380)
    xy.draw(drawing)

if __name__ == '__main__':
    main()
