from poisson_disc import poisson_disc
import random
import xy

random.seed(8675309)
points, pairs = poisson_disc(0, 0, 315, 315, 1, 16)
drawing = xy.Drawing(pairs)
print len(drawing.paths)
# drawing = drawing.linemerge()
# print len(drawing.paths)
drawing.render().write_to_png('test.png')
paths = drawing.paths
paths = xy.sort_paths_greedy(paths)
paths = xy.join_paths(paths)
print len(paths)
xy.draw(paths)
