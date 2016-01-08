import random
import xy
import xyz

def cube(x, y, z):
    return xyz.Cube((x - 0.5, y - 0.5, z - 0.5), (x + 0.5, y + 0.5, z + 0.5))

def main():
    random.seed(34)
    shapes = []
    n = 7
    for x in range(-n, n + 1):
        for z in range(-n, n + 1):
            y = random.randint(-5, 5) * 0.1
            shapes.append(cube(x, y, z))
    scene = xyz.Scene(shapes)
    paths = scene.render((20, 10, 20), (0, 0, 0), (0, 1, 0), 60, 1, 0.1, 100, 0.05)
    # paths.append([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)])
    drawing = xy.Drawing(paths).rotate(90).scale_to_fit(315, 380)
    drawing = drawing.sort_paths_greedy().join_paths()
    drawing.render().write_to_png('three.png')
    xy.draw(drawing)

if __name__ == '__main__':
    main()
