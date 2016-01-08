class Tree(object):

    def __init__(self, shapes):
        self.root = Node(shapes)
        self.root.split()

    def intersect(self, o, d, tmin, tmax):
        return self.root.intersect(o, d, tmin, tmax)

class Node(object):

    def __init__(self, shapes):
        self.shapes = shapes
        self.axis = None
        self.point = None
        self.left = None
        self.right = None

    def intersect(self, o, d, tmin, tmax):
        axis = self.axis
        point = self.point
        if axis is None:
            return self.intersect_shapes(o, d)
        tsplit = (point - o[axis]) / d[axis]
        if (o[axis] < point) or (o[axis] == point and d[axis] <= 0):
            first, second = self.left, self.right
        else:
            first, second = self.right, self.left
        if tsplit > tmax or tsplit <= 0:
            return first.intersect(o, d, tmin, tmax)
        elif tsplit < tmin:
            return second.intersect(o, d, tmin, tmax)
        else:
            inf = 1e9
            h1 = first.intersect(o, d, tmin, tsplit)
            if h1 is None:
                h1 = inf
            if h1 <= tsplit:
                result = h1
            else:
                h2 = second.intersect(o, d, tsplit, min(tmax, h1))
                if h2 is None:
                    h2 = inf
                if h1 <= h2:
                    result = h1
                else:
                    result = h2
            if result >= inf:
                result = None
            return result

    def intersect_shapes(self, o, d):
        ts = [x.intersect(o, d) for x in self.shapes]
        ts = [x for x in ts if x is not None]
        return min(ts) if ts else None

    def score(self, axis, point):
        left, right = self.partition(axis, point)
        return max(len(left), len(right))

    def partition(self, axis, point):
        left = []
        right = []
        for shape in self.shapes:
            a, b = shape.box()
            v1 = a[axis]
            v2 = b[axis]
            if v1 <= point:
                left.append(shape)
            if v2 >= point:
                right.append(shape)
        return left, right

    def split(self, depth=0):
        if len(self.shapes) < 8:
            return
        xs = []
        ys = []
        zs = []
        for shape in self.shapes:
            (x1, y1, z1), (x2, y2, z2) = shape.box()
            xs.append(x1)
            ys.append(y1)
            zs.append(z1)
            xs.append(x2)
            ys.append(y2)
            zs.append(z2)
        xs = sorted(set(xs))
        ys = sorted(set(ys))
        zs = sorted(set(zs))
        best = len(self.shapes) * 0.85
        bestAxis = None
        bestPoint = None
        points = [xs[len(xs) / 2], ys[len(ys) / 2], zs[len(zs) / 2]]
        for axis, point in enumerate(points):
            score = self.score(axis, point)
            if score < best:
                best = score
                bestAxis = axis
                bestPoint = point
        if bestAxis is None:
            return
        l, r = self.partition(bestAxis, bestPoint)
        self.shapes = None
        self.axis = bestAxis
        self.point = bestPoint
        self.left = Node(l)
        self.right = Node(r)
        self.left.split(depth + 1)
        self.right.split(depth + 1)
