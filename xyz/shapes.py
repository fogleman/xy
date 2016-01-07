from __future__ import division

import util

class Triangle(object):
    def __init__(self, a, b, c):
        self.a = a
        self.b = b
        self.c = c
    def paths(self):
        return [
            [self.a, self.b],
            [self.b, self.c],
            [self.c, self.a],
        ]
    def intersect(self, ray):
        return util.ray_triangle_intersection(
            self.a, self.b, self.c, ray.o, ray.d)

class Cube(object):
    def __init__(self, a, b):
        self.a = a
        self.b = b
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
    def intersect(self, ray):
        return util.ray_cube_intersection(self.a, self.b, ray.o, ray.d)
