import xy

def main():
    paths = []
    for i in range(50):
        x = i / 100.0
        paths.append([
            (0 + x, 0 + x),
            (1 - x, 0 + x),
            (1 - x, 1 - x),
            (0 + x, 1 - x),
            (0 + x, 0 + x),
        ])
    paths = [xy.xkcdify(path, 0.005, 0.01/4) for path in paths]
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    im = drawing.render()
    im.write_to_png('xkcd.png')
    # xy.draw(drawing)

if __name__ == '__main__':
    main()
