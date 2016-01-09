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

    def __init__(self, radius=0.5, center=(0, 0, 0)):
        self.radius = radius
        self.center = center
        self._paths = self.lat_lng_paths()
        # self._paths = self.triangle_paths(5)

    def lat_lng_paths(self):
        cx, cy, cz = self.center
        def xyz(lat, lng, radius):
            lat, lng = radians(lat), radians(lng)
            x = cx + radius * cos(lat) * cos(lng)
            y = cy + radius * cos(lat) * sin(lng)
            z = cz + radius * sin(lat)
            return (x, y, z)
        paths = []
        n = 15
        for lat in range(-90 + n, 91 - n, n):
            path = []
            for lng in range(0, 361):
                path.append(xyz(lat, lng, self.radius))
            paths.append(path)
        for lng in range(0, 361, n):
            path = []
            for lat in range(-90 + n, 91 - n):
                path.append(xyz(lat, lng, self.radius))
            paths.append(path)
        return paths

    def triangle_paths(self, detail):
        paths = []
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
            paths.extend(self._triangle_paths(detail, vertices))
        return paths

    def _triangle_paths(self, detail, vertices):
        paths = []
        a, b, c = vertices
        r = self.radius
        p = self.center
        if detail == 0:
            v1 = tuple(r * a[i] + p[i] for i in xrange(3))
            v2 = tuple(r * b[i] + p[i] for i in xrange(3))
            v3 = tuple(r * c[i] + p[i] for i in xrange(3))
            paths.append((v1, v2))
            paths.append((v2, v3))
            paths.append((v3, v1))
        else:
            ab = util.normalize([(a[i] + b[i]) / 2.0 for i in xrange(3)])
            ac = util.normalize([(a[i] + c[i]) / 2.0 for i in xrange(3)])
            bc = util.normalize([(b[i] + c[i]) / 2.0 for i in xrange(3)])
            paths.extend(self._triangle_paths(detail - 1, (a, ab, ac)))
            paths.extend(self._triangle_paths(detail - 1, (b, bc, ab)))
            paths.extend(self._triangle_paths(detail - 1, (c, ac, bc)))
            paths.extend(self._triangle_paths(detail - 1, (ab, bc, ac)))
        return paths

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

class Disk(object):

    def __init__(self, radius=0.5, z=0):
        self.radius = radius
        self.z = z

    def box(self):
        r = self.radius
        z = self.z
        return ((-r, -r, z), (r, r, z))

    def paths(self):
        result = []
        r = self.radius
        z = self.z
        outer = []
        for a in range(0, 361, 10):
            a = radians(a)
            x = r * cos(a)
            y = r * sin(a)
            outer.append((x, y, z))
            result.append([(0, 0, z), (x, y, z)])
        result.append(outer)
        return result

    def intersect(self, o, d):
        if abs(d[2]) < 1e-6:
            return None
        t = (self.z - o[2]) / d[2]
        if t <= 1e-6:
            return None
        p = util.add(o, util.mul_scalar(d, t))
        dist = (p[0] * p[0] + p[1] * p[1]) ** 0.5
        if dist > self.radius:
            return None
        return t

class Cylinder(object):

    def __init__(self, radius=1, z0=-1, z1=1):
        self.radius = radius
        self.z0 = z0
        self.z1 = z1

    def box(self):
        r = self.radius
        return ((-r, -r, self.z0), (r, r, self.z1))

    def paths(self):
        result = []
        lower = []
        upper = []
        for a in range(0, 361, 15):
            a = radians(a)
            x = self.radius * cos(a)
            y = self.radius * sin(a)
            lower.append((x, y, self.z0))
            upper.append((x, y, self.z1))
            result.append([(x, y, self.z0), (x, y, self.z1)])
        result.append(lower)
        result.append(upper)
        return result

    def intersect(self, o, d):
        r = self.radius
        a = d[0] * d[0] + d[1] * d[1]
        b = 2 * o[0] * d[0] + 2 * o[1] * d[1]
        c = o[0] * o[0] + o[1] * o[1] - r * r
        q = b * b - 4 * a * c
        if q < 0:
            return None
        s = q ** 0.5
        t0 = (-b + s) / (2 * a)
        t1 = (-b - s) / (2 * a)
        if t0 > t1:
            t0, t1 = t1, t0
        z0 = o[2] + t0 * d[2]
        z1 = o[2] + t1 * d[2]
        if t0 > 1e-6 and self.z0 < z0 < self.z1:
            return t0
        if t1 > 1e-6 and self.z0 < z1 < self.z1:
            return t1
        return None

class TransformedShape(object):

    def __init__(self, shape, matrix):
        self.shape = shape
        self.matrix = matrix
        self.inverse = matrix.inverse()

    def box(self):
        a, b = self.shape.box()
        return self.matrix.box_multiply(a, b)

    def paths(self):
        paths = self.shape.paths()
        matrix = self.matrix
        return [[matrix * point for point in path] for path in paths]

    def intersect(self, o, d):
        o, d = self.inverse.ray_multiply(o, d)
        return self.shape.intersect(o, d)
