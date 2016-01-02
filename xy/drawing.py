from shapely.affinity import translate, scale, rotate
from shapely.geometry import MultiLineString
import math

class Drawing(MultiLineString):

    @property
    def paths(self):
        return [[(x, y) for x, y in geom.coords] for geom in self.geoms]

    @property
    def width(self):
        x1, y1, x2, y2 = self.bounds
        return x2 - x1

    @property
    def height(self):
        x1, y1, x2, y2 = self.bounds
        return y2 - y1

    def translate(self, x, y):
        return Drawing(translate(self, x, y))

    def scale(self, x, y, origin='center'):
        return Drawing(scale(self, x, y, origin=origin))

    def rotate(self, angle, origin='center'):
        return Drawing(rotate(self, angle, origin=origin))

    def move(self, x, y, ax, ay):
        x1, y1, x2, y2 = self.bounds
        dx = x1 + (x2 - x1) * ax - x
        dy = y1 + (y2 - y1) * ay - y
        return self.translate(-dx, -dy)

    def origin(self):
        return self.move(0, 0, 0, 0)

    def rotate_to_fit(self, width, height, step=5):
        for a in range(0, 180, step):
            g = self.rotate(a).origin()
            if g.width <= width and g.height <= height:
                return g
        return None

    def scale_to_fit(self, width, height, padding=0):
        width -= padding * 2
        height -= padding * 2
        s = min(width / self.width, height / self.height)
        return self.scale(s, s).origin()

    def rotate_and_scale_to_fit(self, width, height, padding=0, step=5):
        gs = []
        width -= padding * 2
        height -= padding * 2
        for a in range(0, 180, step):
            g = self.rotate(a)
            s = min(width / g.width, height / g.height)
            # print a, s
            g = g.scale(s, s).origin()
            gs.append((s, g))
        return max(gs, key=lambda x: x[0])[1]

    def render(self, scale=1, margin=10):
        import cairo
        paths = self.paths
        points = [point for path in paths for point in path]
        x1 = y1 = x2 = y2 = 0
        if points:
            x1 = min(points, key=lambda (x, y): x)[0]
            x2 = max(points, key=lambda (x, y): x)[0]
            y1 = min(points, key=lambda (x, y): y)[1]
            y2 = max(points, key=lambda (x, y): y)[1]
        width = int(scale * max(x2 - x1, 1) + margin * 2)
        height = int(scale * max(y2 - y1, 1) + margin * 2)
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
        dc = cairo.Context(surface)
        dc.scale(1, -1)
        dc.translate(margin, margin)
        dc.scale(scale, scale)
        dc.translate(-x1, -y1 - height)
        dc.set_source_rgb(1, 1, 1)
        dc.paint()
        dc.arc(0, 0, 3, 0, 2 * math.pi)
        dc.set_source_rgb(1, 0, 0)
        dc.fill()
        dc.set_source_rgb(0, 0, 0)
        for path in paths:
            for x, y in path:
                dc.line_to(x, y)
            dc.stroke()
        return surface
