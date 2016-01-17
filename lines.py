from math import sin, cos, pi
import xy

def hexagon():
    sides = 6
    angle = 2 * pi / sides
    angles = [angle * i + pi / 2 for i in range(sides)]
    return [(cos(a), sin(a)) for a in angles]

def interpolate(a, b, t):
    x1, y1 = a
    x2, y2 = b
    x = x1 + (x2 - x1) * t
    y = y1 + (y2 - y1) * t
    return (x, y)

def lines(a, b, c, d, n):
    result = []
    for i in range(n):
        t = float(i) / (n - 1)
        p1 = interpolate(a, b, t)
        p2 = interpolate(c, d, t)
        result.append((p1, p2))
    return result

def main():
    points = [(0, 0)] + hexagon()
    corners = [
        (2, 1, 6),
        (1, 2, 0),
        (2, 0, 6),
        (0, 6, 1),
        (0, 2, 3),
        (2, 3, 4),
        (3, 4, 0),
        (4, 0, 2),
        (4, 0, 6),
        (0, 6, 5),
        (6, 5, 4),
        (5, 4, 0),
    ]
    paths = []
    for a, b, c in corners:
        p1 = points[a]
        p2 = points[b]
        p3 = points[b]
        p4 = points[c]
        paths.extend(lines(p1, p2, p3, p4, 32))
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    drawing = drawing.sort_paths_greedy()
    drawing.render().write_to_png('lines.png')

if __name__ == '__main__':
    main()
