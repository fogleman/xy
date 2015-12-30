from collections import namedtuple
from math import radians, sin, cos, hypot, atan2
from shapely.geometry import Polygon, MultiPolygon, LineString, MultiLineString, LinearRing

try:
    import cairo
except Exception:
    pass

PEN_UP = 0
PEN_DOWN = 40

DECIMALS = 3

Bounds = namedtuple('Bounds', ['x1', 'y1', 'x2', 'y2'])
Size = namedtuple('Size', ['width', 'height'])

class GCode(object):

    @staticmethod
    def from_file(path):
        with open(path, 'r') as fp:
            return GCode(fp.read())

    @staticmethod
    def from_points(points):
        lines = []
        lines.append('M1 %f' % PEN_UP)
        lines.append('G0 X%f Y%f' % points[0])
        lines.append('M1 %f' % PEN_DOWN)
        for point in points:
            lines.append('G1 X%f Y%f' % point)
        lines.append('M1 %f' % PEN_UP)
        return GCode(lines)

    @staticmethod
    def from_geometry(geometry):
        t = type(geometry)
        if t == Polygon:
            g = GCode()
            for x in geometry.interiors:
                g += GCode.from_geometry(x)
            g += GCode.from_geometry(geometry.exterior)
            return g
        if t == LineString or t == LinearRing:
            points = list(geometry.coords)
            if t == LinearRing:
                points.append(points[0])
            return GCode.from_points(points)
        if t in (MultiPolygon, MultiLineString):
            lines = []
            for x in geometry:
                g = GCode.from_geometry(x)
                lines.extend(g.lines)
            return GCode(lines)
        raise Exception('unrecognized geometry type')

    @staticmethod
    def from_geometries(geometries):
        g = GCode()
        for geometry in geometries:
            g += GCode.from_geometry(geometry)
        return g

    @staticmethod
    def from_shape(shape):
        g = GCode()
        parts = list(shape.parts) + [len(shape.points)]
        for i1, i2 in zip(parts, parts[1:]):
            points = map(tuple, shape.points[i1:i2])
            g += GCode.from_points(points)
        return g

    @staticmethod
    def from_shapes(shapes):
        g = GCode()
        for shape in shapes:
            g += GCode.from_shape(shape)
        return g

    def __init__(self, code=None):
        if code is None:
            self.code = ''
        elif isinstance(code, basestring):
            self.code = code
        elif isinstance(code, GCode):
            self.code = code.code
        else:
            self.code = '\n'.join(map(str, code))

    def __str__(self):
        return self.code

    def __add__(self, other):
        return GCode(self.lines + GCode(other).lines)

    @property
    def lines(self):
        return self.code.split('\n')

    @property
    def bounds(self):
        x = []
        y = []
        for line in self.lines:
            for token in line.split():
                if token[0] == 'X':
                    x.append(float(token[1:]))
                if token[0] == 'Y':
                    y.append(float(token[1:]))
        return Bounds(min(x), min(y), max(x), max(y))

    @property
    def size(self):
        b = self.bounds
        return Size(b.x2 - b.x1, b.y2 - b.y1)

    @property
    def width(self):
        return self.size.width

    @property
    def height(self):
        return self.size.height

    @property
    def area(self):
        w, h = self.size
        return w * h

    def save(self, path):
        with open(path, 'w') as fp:
            fp.write(self.code)

    def origin(self):
        return self.move(0, 0, 0, 0)

    def move(self, x, y, ax, ay):
        x1, y1, x2, y2 = self.bounds
        dx = x1 + (x2 - x1) * ax - x
        dy = y1 + (y2 - y1) * ay - y
        return self.translate(-dx, -dy)

    def translate(self, dx, dy):
        lines = []
        for line in self.lines:
            tokens = []
            for token in line.split():
                if token[0] == 'X':
                    token = 'X' + str(float(token[1:]) + dx)
                elif token[0] == 'Y':
                    token = 'Y' + str(float(token[1:]) + dy)
                tokens.append(token)
            lines.append(' '.join(tokens))
        return GCode(lines)

    def scale(self, sx, sy):
        lines = []
        for line in self.lines:
            tokens = []
            for token in line.split():
                if token[0] == 'X':
                    token = 'X' + str(float(token[1:]) * sx)
                elif token[0] == 'Y':
                    token = 'Y' + str(float(token[1:]) * sy)
                elif token[0] == 'I':
                    token = 'I' + str(float(token[1:]) * sx)
                elif token[0] == 'J':
                    token = 'J' + str(float(token[1:]) * sy)
                tokens.append(token)
            lines.append(' '.join(tokens))
        return GCode(lines)

    def rotate(self, angle):
        c = cos(radians(angle))
        s = sin(radians(angle))
        lines = []
        x = y = i = j = 0
        for line in self.lines:
            for token in line.split():
                if token[0] == 'X':
                    x = float(token[1:])
                elif token[0] == 'Y':
                    y = float(token[1:])
                elif token[0] == 'I':
                    i = float(token[1:])
                elif token[0] == 'J':
                    j = float(token[1:])
            rx = round(x * c - y * s, DECIMALS)
            ry = round(y * c + x * s, DECIMALS)
            ri = round(i * c - j * s, DECIMALS)
            rj = round(j * c + i * s, DECIMALS)
            tokens = []
            for token in line.split():
                if token[0] == 'X':
                    token = 'X' + str(rx)
                elif token[0] == 'Y':
                    token = 'Y' + str(ry)
                elif token[0] == 'I':
                    token = 'I' + str(ri)
                elif token[0] == 'J':
                    token = 'J' + str(rj)
                tokens.append(token)
            lines.append(' '.join(tokens))
        return GCode(lines)

    def rotate_to_fit(self, width, height):
        for a in range(0, 180, 5):
            g = self.rotate(a).origin()
            if g.width <= width and g.height <= height:
                return g
        return None

    def get_scale_to_fit(self, width, height, padding=0):
        width -= padding * 2
        height -= padding * 2
        return min(width / self.width, height / self.height)

    def scale_to_fit(self, width, height, padding=0):
        s = self.get_scale_to_fit(width, height, padding)
        return self.scale(s, s).origin()

    def rotate_and_scale_to_fit(self, width, height, padding=0):
        gs = []
        width -= padding * 2
        height -= padding * 2
        for a in range(0, 180, 5):
            g = self.rotate(a)
            s = min(width / g.width, height / g.height)
            g = g.scale(s, s).origin()
            gs.append((s, g))
        print max(gs, key=lambda x: x[0])[0]
        g = max(gs, key=lambda x: x[0])[1]
        return g

    def clamp(self, minx, miny, maxx, maxy):
        lines = []
        for line in self.lines:
            tokens = []
            for token in line.split():
                if token[0] == 'X':
                    token = 'X' + str(max(float(token[1:]), minx))
                    token = 'X' + str(min(float(token[1:]), maxx))
                elif token[0] == 'Y':
                    token = 'Y' + str(max(float(token[1:]), miny))
                    token = 'Y' + str(min(float(token[1:]), maxy))
                tokens.append(token)
            lines.append(' '.join(tokens))
        return GCode(lines)

    def render(self, x1, y1, x2, y2, scale):
        width = int(round((x2 - x1) * scale))
        height = int(round((y2 - y1) * scale))
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
        dc = cairo.Context(surface)
        dc.set_source_rgb(0, 0, 0)
        dc.paint()
        dc.scale(scale, -scale)
        dc.translate(0, y1 - y2)
        dc.translate(-x1, -y1)
        dc.set_line_cap(cairo.LINE_CAP_ROUND)
        dc.set_line_join(cairo.LINE_JOIN_ROUND)
        dc.set_line_width(0.25)
        dc.set_source_rgb(1, 1, 1)
        x = y = z = i = j = 0
        px = py = 0
        for line in self.lines:
            tokens = line.split()
            if not tokens:
                continue
            if tokens[0][0] == 'N':
                tokens.pop(0)
            for token in tokens:
                if token[0] == 'X':
                    x = float(token[1:])
                elif token[0] == 'Y':
                    y = float(token[1:])
                elif token[0] == 'Z':
                    z = float(token[1:])
                elif token[0] == 'I':
                    i = float(token[1:])
                elif token[0] == 'J':
                    j = float(token[1:])
            if tokens[0] == 'G0':
                dc.move_to(x, y)
            elif tokens[0] == 'G1':
                dc.line_to(x, y)
            elif tokens[0] in ['G2', 'G3']:
                cx = px + i
                cy = py + j
                r = hypot(i, j)
                a1 = atan2(py - cy, px - cx)
                a2 = atan2(y - cy, x - cx)
                dc.new_sub_path()
                if tokens[0] == 'G3':
                    dc.arc(cx, cy, r, a1, a2)
                else:
                    dc.arc_negative(cx, cy, r, a1, a2)
            dc.stroke()
            dc.move_to(x, y)
            px, py = x, y
        return surface
