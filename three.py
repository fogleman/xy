from math import radians
import xy
import xyz

def cube(x, y, z):
    return xyz.Cube((x - 0.5, y - 0.5, z - 0.5), (x + 0.5, y + 0.5, z + 0.5))

def main():
    shapes = []
    m = xyz.Matrix().rotate((1, 0, 0), radians(45)).translate((0, -1, 0))
    shapes.append(xyz.TransformedShape(xyz.Disk(3), m))
    shapes.append(xyz.Sphere(1.25, (0, 0, 0)))
    shapes.append(cube(-1, 0, 0))
    shapes.append(cube(0, -1, 0))
    shapes.append(cube(0, 0, -1))
    shapes.append(cube(1, 0, 0))
    shapes.append(cube(0, 1, 0))
    shapes.append(cube(0, 0, 1))
    scene = xyz.Scene(shapes)
    paths = scene.render((10, 20, 10), (0, 0, 0), (0, 0, 1), 60, 1, 0.1, 100, 0.02)
    # paths.append([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)])
    drawing = xy.Drawing(paths).rotate(90).scale_to_fit(315, 380).rotate(-90)
    drawing = drawing.sort_paths_greedy().join_paths()
    drawing.render().write_to_png('three.png')
    # xy.draw(drawing)

if __name__ == '__main__':
    main()
