from __future__ import division

def length(vector):
    return sum(x * x for x in vector) ** 0.5

def normalize(vector):
    d = length(vector)
    return tuple(x / d for x in vector)

def distance(p1, p2):
    return sum((a - b) ** 2 for a, b in zip(p1, p2)) ** 0.5

def cross(v1, v2):
    return (
        v1[1] * v2[2] - v1[2] * v2[1],
        v1[2] * v2[0] - v1[0] * v2[2],
        v1[0] * v2[1] - v1[1] * v2[0],
    )

def dot(v1, v2):
    x1, y1, z1 = v1
    x2, y2, z2 = v2
    return x1 * x2 + y1 * y2 + z1 * z2

def add(v1, v2):
    return tuple(a + b for a, b in zip(v1, v2))

def sub(v1, v2):
    return tuple(a - b for a, b in zip(v1, v2))

def mul(v1, v2):
    return tuple(a * b for a, b in zip(v1, v2))

def div(v1, v2):
    return tuple(a / b if b else 0 for a, b in zip(v1, v2))

def mul_scalar(v, s):
    return tuple(a * s for a in v)

def div_scalar(v, s):
    return tuple(a / s for a in v)

def neg(vector):
    return tuple(-x for x in vector)

def vector_min(v1, v2):
    return tuple(min(x, y) for x, y in zip(v1, v2))

def vector_max(v1, v2):
    return tuple(max(x, y) for x, y in zip(v1, v2))

def interpolate(v1, v2, t):
    return add(v1, mul_scalar(sub(v2, v1), t))

def chop(path, step):
    result = []
    for a, b in zip(path, path[1:]):
        v = sub(b, a)
        l = length(v)
        result.append(a)
        d = step
        while d < l:
            result.append(interpolate(a, b, d / l))
            d += step
        result.append(b)
    return result

def normal_from_points(a, b, c):
    x1, y1, z1 = a
    x2, y2, z2 = b
    x3, y3, z3 = c
    ab = (x2 - x1, y2 - y1, z2 - z1)
    ac = (x3 - x1, y3 - y1, z3 - z1)
    x, y, z = cross(ab, ac)
    d = (x * x + y * y + z * z) ** 0.5
    return (x / d, y / d, z / d)

def bounding_box(positions):
    (x0, y0, z0) = (x1, y1, z1) = positions[0]
    for x, y, z in positions:
        x0 = min(x0, x)
        y0 = min(y0, y)
        z0 = min(z0, z)
        x1 = max(x1, x)
        y1 = max(y1, y)
        z1 = max(z1, z)
    return (x0, y0, z0), (x1, y1, z1)

def flatten(array):
    result = []
    for value in array:
        result.extend(value)
    return result

def ray_triangle_intersection(v1, v2, v3, o, d):
    eps = 1e-6
    e1 = sub(v2, v1)
    e2 = sub(v3, v1)
    p = cross(d, e2)
    det = dot(e1, p)
    if abs(det) < eps:
        return None
    inv = 1 / det
    t = sub(o, v1)
    u = dot(t, p) * inv
    if u < 0 or u > 1:
        return None
    q = cross(t, e1)
    v = dot(d, q) * inv
    if v < 0 or v > 1:
        return None
    t = dot(e2, q) * inv
    if t > eps:
        return t
    return None

def ray_cube_intersection(a, b, o, d):
    nx = (a[0] - o[0]) / d[0] if d[0] else 0
    ny = (a[1] - o[1]) / d[1] if d[1] else 0
    nz = (a[2] - o[2]) / d[2] if d[2] else 0
    fx = (b[0] - o[0]) / d[0] if d[0] else 0
    fy = (b[1] - o[1]) / d[1] if d[1] else 0
    fz = (b[2] - o[2]) / d[2] if d[2] else 0
    if nx > fx: nx, fx = fx, nx
    if ny > fy: ny, fy = fy, ny
    if nz > fz: nz, fz = fz, nz
    t0 = nx
    if ny > t0: t0 = ny
    if nz > t0: t0 = nz
    t1 = fx
    if fy < t1: t1 = fy
    if fz < t1: t1 = fz
    if t0 >= 0 and t0 < t1:
        return t0
    return None
