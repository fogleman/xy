from math import radians
import random
import xy
import xyz

def cube(x, y, z):
    return xyz.Cube((x - 0.5, y - 0.5, z - 0.5), (x + 0.5, y + 0.5, z + 0.5))

def sphere(x, y, z, r, axis=2):
    if axis == 0:
        s = xyz.Sphere(r)
        m = xyz.rotate((0, 1, 0), radians(90)).translate((x, y, z))
        return xyz.TransformedShape(s, m)
    if axis == 1:
        s = xyz.Sphere(r)
        m = xyz.rotate((1, 0, 0), radians(90)).translate((x, y, z))
        return xyz.TransformedShape(s, m)
    if axis == 2:
        return xyz.Sphere(r, (x, y, z))

def pipe(a, b, r):
    x1, y1, z1 = a
    x2, y2, z2 = b
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    if dx:
        c = xyz.Cylinder(r, -dx / 2.0, dx / 2.0)
        m = xyz.rotate((0, 1, 0), radians(-90)).translate(((x1 + x2) / 2.0, y1, z1))
        return xyz.TransformedShape(c, m)
    if dy:
        c = xyz.Cylinder(r, -dy / 2, dy / 2)
        m = xyz.rotate((1, 0, 0), radians(-90)).translate((x1, (y1 + y2) / 2.0, z1))
        return xyz.TransformedShape(c, m)
    if dz:
        c = xyz.Cylinder(r, z1, z2)
        m = xyz.translate((x1, y1, 0))
        return xyz.TransformedShape(c, m)

def main():
    shapes = []
    for x in range(-4, 5):
        for y in range(-4, 5):
            z = random.random() * 2
            r = random.random() + 0.5
            shapes.append(xyz.Sphere(r, (x, y, z)))
            # shapes.append(pipe((x, y, 0), (x, y, z), 0.25))
            # shapes.append(sphere(x, y, z, 0.25))

    # shapes.append(sphere(0, 0, 0, 0.5))
    # shapes.append(pipe((0, 1, 2), (0, 3, 2), 0.25))
    # shapes.append(pipe((-3, -1, 5), (3, -1, 5), 0.25))
    # shapes.append(sphere(-3, -1, 5, 0.25))
    # shapes.append(sphere(3, -1, 5, 0.25))
    # shapes.append(sphere(0, 1, 2, 0.25))
    # shapes.append(sphere(0, 3, 2, 0.25))
    # shapes.append(pipe((0, 0, 1), (0, 0, 4), 0.25))
    # shapes.append(pipe((0, 1, 0), (0, 1, 3), 0.25))

    # shapes.append(pipe((-1, 0, 0), (1, 0, 0), 0.5))
    # shapes.append(pipe((0, -1, 0), (0, 1, 0), 0.5))
    # shapes.append(pipe((0, 0, -1), (0, 0, 1), 0.5))
    # shapes.append(sphere(-1, 0, 0, 0.5, 0))
    # shapes.append(sphere(0, -1, 0, 0.5, 1))
    # shapes.append(sphere(0, 0, -1, 0.5, 2))
    # shapes.append(sphere(1, 0, 0, 0.5, 0))
    # shapes.append(sphere(0, 1, 0, 0.5, 1))
    # shapes.append(sphere(0, 0, 1, 0.5, 2))
    scene = xyz.Scene(shapes)
    paths = scene.render((20, 20, 10), (0, 0, 0), (0, 0, 1), 30, 1, 0.1, 100, 0.05)
    # paths.append([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)])
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    drawing = drawing.sort_paths_greedy().join_paths()
    drawing.render().write_to_png('three.png')
    # xy.draw(drawing)

if __name__ == '__main__':
    main()
