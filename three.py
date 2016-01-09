from math import radians
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
        c = xyz.Cylinder(r, x1, x2)
        m = xyz.rotate((0, 1, 0), radians(90))
        return xyz.TransformedShape(c, m)
    if dy:
        c = xyz.Cylinder(r, y1, y2)
        m = xyz.rotate((1, 0, 0), radians(90))
        return xyz.TransformedShape(c, m)
    if dz:
        return xyz.Cylinder(r, z1, z2)

def main():
    shapes = []
    shapes.append(pipe((-1, 0, 0), (1, 0, 0), 0.5))
    shapes.append(pipe((0, -1, 0), (0, 1, 0), 0.5))
    shapes.append(pipe((0, 0, -1), (0, 0, 1), 0.5))
    shapes.append(sphere(-1, 0, 0, 0.5, 0))
    shapes.append(sphere(0, -1, 0, 0.5, 1))
    shapes.append(sphere(0, 0, -1, 0.5, 2))
    shapes.append(sphere(1, 0, 0, 0.5, 0))
    shapes.append(sphere(0, 1, 0, 0.5, 1))
    shapes.append(sphere(0, 0, 1, 0.5, 2))
    scene = xyz.Scene(shapes)
    paths = scene.render((10, 20, 10), (0, 0, 0), (0, 0, 1), 60, 1, 0.1, 100, 0.02)
    # paths.append([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)])
    drawing = xy.Drawing(paths).rotate(90).scale_to_fit(315, 380).rotate(-90)
    drawing = drawing.sort_paths_greedy().join_paths()
    drawing.render().write_to_png('three.png')
    # xy.draw(drawing)

if __name__ == '__main__':
    main()
