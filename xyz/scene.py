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

    def clip_paths(self, eye, step=0.1):
        paths = self.paths()
        result = []
        for path in paths:
            for (x1, y1), (x2, y2) in zip(path, path[1:]):
                pass
        return result
