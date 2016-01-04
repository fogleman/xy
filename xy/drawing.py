import math

class Drawing(object):

    def __init__(self, paths=None):
        self.paths = paths or []
        self._bounds = None

    @property
    def bounds(self):
        if not self._bounds:
            points = [(x, y) for path in self.paths for x, y in path]
            if points:
                x1 = min(x for x, y in points)
                x2 = max(x for x, y in points)
                y1 = min(y for x, y in points)
                y2 = max(y for x, y in points)
            else:
                x1 = x2 = y1 = y2 = 0
            self._bounds = (x1, y1, x2, y2)
        return self._bounds

    @property
    def width(self):
        x1, y1, x2, y2 = self.bounds
        return x2 - x1

    @property
    def height(self):
        x1, y1, x2, y2 = self.bounds
        return y2 - y1

    def transform(self, func):
        return Drawing([[func(x, y) for x, y in path] for path in self.paths])

    def translate(self, x, y):
        def func(px, py):
            return (px + x, py + y)
        return self.transform(func)

    def scale(self, x, y):
        def func(px, py):
            return (px * x, py * y)
        return self.transform(func)

    def rotate(self, angle):
        c = math.cos(math.radians(angle))
        s = math.sin(math.radians(angle))
        def func(x, y):
            return (x * c - y * s, y * c + x * s)
        return self.transform(func)

    def move(self, x, y, ax, ay):
        x1, y1, x2, y2 = self.bounds
        dx = x1 + (x2 - x1) * ax - x
        dy = y1 + (y2 - y1) * ay - y
        return self.translate(-dx, -dy)

    def origin(self):
        return self.move(0, 0, 0, 0)

    def rotate_to_fit(self, width, height, step=5):
        for a in range(0, 180, step):
            g = self.rotate(a)
            if g.width <= width and g.height <= height:
                return g.origin()
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
            gs.append((s, a, g))
        s, a, g = max(gs)
        return g.scale(s, s).origin()

    def render(self, scale=96/25.4, margin=10):
        import cairo
        x1, y1, x2, y2 = self.bounds
        print self.bounds
        width = int(scale * self.width + margin * 2)
        height = int(scale * self.height + margin * 2)
        surface = cairo.ImageSurface(cairo.FORMAT_RGB24, width, height)
        dc = cairo.Context(surface)
        dc.scale(1, -1)
        dc.translate(0, -height)
        dc.translate(margin, margin)
        dc.translate(-x1, -y1)
        dc.scale(scale, scale)
        dc.set_line_width(1.0 / scale)
        dc.set_source_rgb(1, 1, 1)
        dc.paint()
        dc.arc(0, 0, 3.0 / scale, 0, 2 * math.pi)
        dc.set_source_rgb(1, 0, 0)
        dc.fill()
        dc.set_source_rgb(0, 0, 0)
        for path in self.paths:
            for x, y in path:
                dc.line_to(x, y)
            dc.stroke()
        return surface
