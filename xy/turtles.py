import math

def to_degrees(x):
    return math.degrees(x) % 360

class Turtle(object):

    def __init__(self):
        self.reset()

    def reset(self):
        self.x = 0
        self.y = 0
        self.h = 0
        self.pen = True
        self.path = [(self.x, self.y)]
        self.paths = []

    def clear(self):
        self.path = [(self.x, self.y)]
        self.paths = []

    def get_paths(self):
        paths = list(self.paths)
        if len(self.path) > 1:
            paths.append(self.path)
        return paths

    def pd(self):
        self.pen = True
    pendown = down = pd

    def pu(self):
        self.pen = False
        if len(self.path) > 1:
            self.paths.append(self.path)
            self.path = [(self.x, self.y)]
    penup = up = pu

    def isdown(self):
        return self.pen

    def goto(self, x, y=None):
        if y is None:
            x, y = x
        if self.pen:
            self.path.append((x, y))
        self.x = x
        self.y = y
    setpos = setposition = goto

    def setx(self, x):
        self.goto(x, self.y)

    def sety(self, x):
        self.goto(self.x, y)

    def seth(self, heading):
        self.h = heading
    setheading = seth

    def home(self):
        self.goto(0, 0)
        self.seth(0)

    def fd(self, distance):
        x = self.x + distance * math.cos(math.radians(self.h))
        y = self.y + distance * math.sin(math.radians(self.h))
        self.goto(x, y)
    forward = fd

    def bk(self, distance):
        x = self.x - distance * math.cos(math.radians(self.h))
        y = self.y - distance * math.sin(math.radians(self.h))
        self.goto(x, y)
    backward = back = bk

    def rt(self, angle):
        self.seth(self.h + angle)
    right = rt

    def lt(self, angle):
        self.seth(self.h - angle)
    left = lt

    def circle(self, radius, extent=None, steps=None):
        if extent is None:
            extent = 360
        if steps is None:
            steps = int(round(abs(2 * math.pi * radius * extent / 360)))
            steps = max(steps, 4)
        cx = self.x + radius * math.cos(math.radians(self.h + 90))
        cy = self.y + radius * math.sin(math.radians(self.h + 90))
        a1 = to_degrees(math.atan2(self.y - cy, self.x - cx))
        a2 = a1 + extent if radius >= 0 else a1 - extent
        for i in range(steps):
            p = i / float(steps - 1)
            a = a1 + (a2 - a1) * p
            x = cx + abs(radius) * math.cos(math.radians(a))
            y = cy + abs(radius) * math.sin(math.radians(a))
            self.goto(x, y)
        if radius >= 0:
            self.seth(self.h + extent)
        else:
            self.seth(self.h - extent)

    def pos(self):
        return (self.x, self.y)
    position = pos

    def towards(self, x, y=None):
        if y is None:
            x, y = x
        return to_degrees(math.atan2(y - self.y, x - self.x))

    def xcor(self):
        return self.x

    def ycor(self):
        return self.y

    def heading(self):
        return self.h

    def distance(self, x, y=None):
        if y is None:
            x, y = x
        return math.hypot(x - self.x, y - self.y)

    def render(self, scale=1, margin=10):
        import cairo
        paths = self.get_paths()
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
        dc.translate(margin, margin)
        dc.scale(scale, scale)
        dc.translate(-x1, -y1)
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
