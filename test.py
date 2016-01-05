from poisson_disc import poisson_disc
import xy

points, pairs = poisson_disc(0, 0, 300, 300, 1, 16)
# paths = [xy.circle(x, y, 0.5) for x, y in points]
# paths.extend(pairs)
paths = pairs
drawing = xy.Drawing(paths)
print len(drawing.paths)
drawing = drawing.linemerge()
print len(drawing.paths)
drawing.render().write_to_png('test.png')
