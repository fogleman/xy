import xy
import xyz

def cube(x, y, z):
    return xyz.Cube((x - 0.5, y - 0.5, z - 0.5), (x + 0.5, y + 0.5, z + 0.5))

def main():
    paths = []
    paths.extend(cube(0, 0, 0).paths())
    paths.extend(cube(0, 1, 0).paths())
    paths.extend(cube(0, 2, 0).paths())
    paths.extend(cube(-1, 0, 0).paths())
    paths.extend(cube(-2, 0, 0).paths())
    paths.extend(cube(1, 0, 0).paths())
    paths.extend(cube(2, 0, 0).paths())
    paths.extend(cube(0, 0, 1).paths())
    paths.extend(cube(0, 0, 2).paths())
    m = xyz.Matrix().look_at((-2, 3, 6), (0, 0, 0), (0, 1, 0))
    m = m.perspective(60, 1, 0.1, 10)
    # m = m.orthographic(-2, 2, -2, 2, -10, 10)
    paths = [[(m * (x, y, z, 1)) for x, y, z in path] for path in paths]
    paths = [[xyz.div_scalar(p, p[3])[:3] for p in path] for path in paths]
    paths = [[p[:2] for p in path if -1 <= p[-1] <= 1] for path in paths]
    paths = filter(None, paths)
    paths.append([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)])
    drawing = xy.Drawing(paths).scale_to_fit(315, 315)
    drawing.render().write_to_png('three.png')

if __name__ == '__main__':
    main()
