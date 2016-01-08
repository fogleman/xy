import itertools
import util

class Scene(object):

    def __init__(self, shapes=None):
        self.shapes = shapes or []

    def add(self, shape):
        self.shapes.append(shape)

    def paths(self):
        result = []
        for shape in self.shapes:
            result.extend(shape.paths())
        return result

    def intersect(self, o, d):
        ts = [x.intersect(o, d) for x in self.shapes]
        ts = [x for x in ts if x is not None]
        return min(ts) if ts else None

    def clip_paths(self, eye, step):
        paths = self.paths()
        result = []
        for path in paths:
            result.extend(self.clip(path, eye, step))
        return result

    def clip(self, path, eye, step):
        result = []
        points = util.chop(path, step)
        visible = [self.visible(eye, point) for point in points]
        items = zip(visible, points)
        for visible, group in itertools.groupby(items, lambda x: x[0]):
            points = [x[1] for x in group]
            if visible and len(points) > 1:
                result.append(points)
        return result

    def visible(self, eye, point):
        v = util.sub(eye, point)
        o = point
        d = util.normalize(v)
        t = self.intersect(o, d)
        if t is not None and t < util.length(v):
            return False
        return True
