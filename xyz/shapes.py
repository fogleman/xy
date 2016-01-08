from __future__ import division

from math import radians, sin, cos
import util

class Triangle(object):

    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c

    def box(self):
        ax, ay, az = self.a
        bx, by, bz = self.b
        cx, cy, cz = self.c
        x1 = min(min(ax, bx), cx)
        y1 = min(min(ay, by), cy)
        z1 = min(min(az, bz), cz)
        x2 = max(max(ax, bx), cx)
        y2 = max(max(ay, by), cy)
        z2 = max(max(az, bz), cz)
        return ((x1, y1, z1), (x2, y2, z2))

    def paths(self):
        return [
            [self.a, self.b],
            [self.b, self.c],
            [self.c, self.a],
        ]

    def intersect(self, o, d):
        return util.ray_triangle_intersection(
            self.a, self.b, self.c, o, d)

class Cube(object):

    def __init__(self, a, b):
        self.a = a
        self.b = b

    def box(self):
        return (self.a, self.b)

    def paths(self):
        x1, y1, z1 = self.a
        x2, y2, z2 = self.b
        return [
            [(x1, y1, z1), (x1, y1, z2)],
            [(x1, y1, z1), (x1, y2, z1)],
            [(x1, y1, z1), (x2, y1, z1)],
            [(x1, y1, z2), (x1, y2, z2)],
            [(x1, y1, z2), (x2, y1, z2)],
            [(x1, y2, z1), (x1, y2, z2)],
            [(x1, y2, z1), (x2, y2, z1)],
            [(x1, y2, z2), (x2, y2, z2)],
            [(x2, y1, z1), (x2, y1, z2)],
            [(x2, y1, z1), (x2, y2, z1)],
            [(x2, y1, z2), (x2, y2, z2)],
            [(x2, y2, z1), (x2, y2, z2)],
        ]

    def intersect(self, o, d):
        return util.ray_cube_intersection(self.a, self.b, o, d)

class Sphere(object):

    def __init__(self, detail, radius=0.5, center=(0, 0, 0)):
        self.detail = detail
        self.radius = radius
        self.center = center
        self._paths = self.lat_lng_paths()
        # self.setup()

    def lat_lng_paths(self):
        def xyz(lat, lng, radius):
            lat, lng = radians(lat), radians(lng)
            x = radius * cos(lat) * cos(lng)
            y = radius * cos(lat) * sin(lng)
            z = radius * sin(lat)
            return (x, z, y)
        paths = []
        for lat in range(-90, 91, 5):
            path = []
            for lng in range(0, 361):
                path.append(xyz(lat, lng, self.radius))
            paths.append(path)
        for lng in range(0, 361, 5):
            path = []
            for lat in range(-90, 91):
                path.append(xyz(lat, lng, self.radius))
            paths.append(path)
        return paths

    def setup(self):
        indices = [
            (0, 3, 4), (0, 4, 1), (5, 4, 3), (5, 1, 4),
            (2, 3, 0), (1, 2, 0), (3, 2, 5), (2, 1, 5),
        ]
        positions = [
            (0, 0, -1), (1, 0, 0), (0, -1, 0),
            (-1, 0, 0), (0, 1, 0), (0, 0, 1),
        ]
        for a, b, c in indices:
            vertices = (positions[a], positions[b], positions[c])
            self._setup(self.detail, vertices)

    def _setup(self, detail, vertices):
        a, b, c = vertices
        r = self.radius
        p = self.center
        if detail == 0:
            v1 = tuple(r * a[i] + p[i] for i in xrange(3))
            v2 = tuple(r * b[i] + p[i] for i in xrange(3))
            v3 = tuple(r * c[i] + p[i] for i in xrange(3))
            self._paths.append((v1, v2))
            self._paths.append((v2, v3))
            self._paths.append((v3, v1))
        else:
            ab = util.normalize([(a[i] + b[i]) / 2.0 for i in xrange(3)])
            ac = util.normalize([(a[i] + c[i]) / 2.0 for i in xrange(3)])
            bc = util.normalize([(b[i] + c[i]) / 2.0 for i in xrange(3)])
            self._setup(detail - 1, (a, ab, ac))
            self._setup(detail - 1, (b, bc, ab))
            self._setup(detail - 1, (c, ac, bc))
            self._setup(detail - 1, (ab, bc, ac))

    def box(self):
        x, y, z = self.center
        r = self.radius
        a = (x - r, y - r, z - r)
        b = (x + r, y + r, z + r)
        return (a, b)

    def paths(self):
        return self._paths

    def intersect(self, o, d):
        r = self.radius - 0.001
        to = util.sub(o, self.center)
        b = util.dot(to, d)
        c = util.dot(to, to) - r * r
        d = b * b - c
        if d > 0:
            d = d ** 0.5
            t1 = -b - d
            if t1 > 0:
                return t1
            t2 = -b + d
            if t2 > 0:
                return t2
        return None
