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
    paths = xy.remove_duplicates(paths)
    drawing = xy.Drawing(paths).rotate_and_scale_to_fit(315, 380, step=90)
    # drawing = drawing.move(315 / 2.0, 380 / 2.0, 0.5, 0.5)
    drawing.paths = [x for x in drawing.paths if len(x) > 1]
    # drawing = drawing.simplify_paths()
    drawing = drawing.sort_paths_greedy()
    drawing = drawing.join_paths()
    # drawing = drawing.simplify_paths()
    im = drawing.render()
    im.write_to_png('paths.png')
    xy.draw(drawing)

if __name__ == '__main__':
    main(sys.argv[1])
