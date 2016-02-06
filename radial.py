import math
import random
import xy

def create_path():
    result = []
    r = random.random() * 150
    a = random.random() * 2 * math.pi
    while r < 150:
        r2 = r + 10#random.random() * 10 + 5
        a2 = a + (random.random() * 2 - 1) * math.pi / r2 * 4
        x1 = math.cos(a) * r
        y1 = math.sin(a) * r
        x2 = math.cos(a) * r2
        y2 = math.sin(a) * r2
        result.append([(x1, y1), (x2, y2)])
        result.append(xy.arc(0, 0, r2, math.degrees(a), math.degrees(a2)))
        r = r2
        a = a2
    return result

def create_paths():
    result = []
    for i in range(350):
        result.extend(create_path())
    return result

def main():
    paths = create_paths()
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    drawing = drawing.sort_paths_greedy()
    im = drawing.render()
    im.write_to_png('radial.png')
    # xy.draw(drawing)

if __name__ == '__main__':
    main()
