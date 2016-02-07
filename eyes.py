import math
import random
import xy

def ellipse(x, y, rx, ry, n=36):
    result = []
    for i in range(n + 1):
        p = i / float(n)
        a = 2 * math.pi * p
        px = x + math.cos(a) * rx
        py = y + math.sin(a) * ry
        result.append((px, py))
    return result

def create_eye(x, y):
    result = []
    r = (random.random() * 1 + 1) * 0.2
    a = random.random() * 0.8 + 0.1
    rx = r * a
    ry = r * (1 - a)
    s = rx + random.random() * 0.025
    result.append(ellipse(x + s, y, rx, ry))
    result.append(ellipse(x - s, y, rx, ry))
    r = (random.random() * 1 + 1) * 0.05
    a = random.random() * 0.8 + 0.1
    da = random.random() * 2 * math.pi
    d = random.random() * 0.1
    dx = math.cos(da) * d
    dy = math.sin(da) * d
    result.append(ellipse(dx + x + s, dy + y, r * a, r * (1 - a)))
    result.append(ellipse(dx + x - s, dy + y, r * a, r * (1 - a)))
    r = (random.random() * 1 + 1) * 0.2
    a = random.random() * 0.8 + 0.1
    result.append(ellipse(x, y - 0.25, r * a, r * (1 - a)))
    o = 0.25 + r * (1 - a) + random.random() * 0.25
    r = random.random() ** 2 * 4 + 0.1
    d = random.random() * 0.2 + 0.05
    sign = random.choice([1, -1])
    da = math.degrees(math.atan2(d, r))
    if sign > 0:
        result.append(xy.arc(x, y - o + r * sign, r, 270 - da, 270 + da))
    else:
        result.append(xy.arc(x, y - o + r * sign, r, 90 - da, 90 + da))
    return result

def create_paths():
    result = []
    for y in range(6*3):
        for x in range(5*3):
            result.extend(create_eye(x, y))
    return result

def main():
    paths = create_paths()
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    drawing = drawing.sort_paths_greedy()
    im = drawing.render()
    im.write_to_png('eyes.png')
    # xy.draw(drawing)

if __name__ == '__main__':
    main()
