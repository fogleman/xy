import sys
import xy

def load_paths(filename):
    paths = []
    with open(filename) as fp:
        for line in fp:
            points = filter(None, line.strip().split(';'))
            if not points:
                continue
            path = [tuple(map(float, x.split(','))) for x in points]
            paths.append(path)
    return paths

def main(filename):
    paths = load_paths(filename)
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    drawing = drawing.move(315 / 2.0, 380 / 2.0, 0.5, 0.5)
    im = drawing.render()
    im.write_to_png('paths.png')
    xy.draw(drawing)

if __name__ == '__main__':
    main(sys.argv[1])
