from math import radians
import random
import xy
import xyz

PIPES = 8
SIZE = 3
TURN_PROBABILITY = 0.3
UPDATE_RATE = 0.05

DIRECTIONS = [
    (0, -1, 0, 0), (0, 1, 0, 0),
    (1, 0, -1, 0), (1, 0, 1, 0),
    (2, 0, 0, -1), (2, 0, 0, 1),
]

def sphere(x, y, z, r, axis=2):
    return xyz.Sphere(r, (x, y, z))
    if axis == 0:
        s = xyz.Sphere(r)
        m = xyz.rotate((0, 1, 0), radians(90)).translate((x, y, z))
        return xyz.TransformedShape(s, m)
    if axis == 1:
        s = xyz.Sphere(r)
        m = xyz.rotate((1, 0, 0), radians(90)).translate((x, y, z))
        return xyz.TransformedShape(s, m)
    if axis == 2:
        return xyz.Sphere(r, (x, y, z))

def pipe(a, b, r):
    x1, y1, z1 = a
    x2, y2, z2 = b
    dx, dy, dz = x2 - x1, y2 - y1, z2 - z1
    if dx:
        c = xyz.Cylinder(r, -dx / 2.0, dx / 2.0)
        m = xyz.rotate((0, 1, 0), radians(-90)).translate(((x1 + x2) / 2.0, y1, z1))
        return xyz.TransformedShape(c, m)
    if dy:
        c = xyz.Cylinder(r, -dy / 2, dy / 2)
        m = xyz.rotate((1, 0, 0), radians(-90)).translate((x1, (y1 + y2) / 2.0, z1))
        return xyz.TransformedShape(c, m)
    if dz:
        c = xyz.Cylinder(r, z1, z2)
        m = xyz.translate((x1, y1, 0))
        return xyz.TransformedShape(c, m)

class Pipe(object):
    def __init__(self, occupied):
        self.occupied = occupied
        self.shapes = []
        self.restart()
    def add_cylinder(self, position, axis):
        x, y, z = position
        if axis == 0:
            self.shapes.append(pipe((x - 0.5, y, z), (x + 0.5, y, z), 0.25))
        if axis == 1:
            self.shapes.append(pipe((x, y - 0.5, z), (x, y + 0.5, z), 0.25))
        if axis == 2:
            self.shapes.append(pipe((x, y, z - 0.5), (x, y, z + 0.5), 0.25))
    def add_sphere(self, position):
        x, y, z = position
        self.shapes.append(sphere(x, y, z, 0.25))
    def restart(self):
        while True:
            x = random.randint(-SIZE, SIZE)
            y = random.randint(-SIZE, SIZE)
            z = random.randint(-SIZE, SIZE)
            if (x, y, z) not in self.occupied:
                break
        self.position = (x, y, z)
        self.direction = random.choice(DIRECTIONS)
        self.occupied.add(self.position)
        self.add_sphere(self.position)
    def update(self):
        x, y, z = self.position
        directions = list(DIRECTIONS)
        random.shuffle(directions)
        if random.random() > TURN_PROBABILITY:
            directions.remove(self.direction)
            directions.insert(0, self.direction)
        for direction in directions:
            axis, dx, dy, dz = direction
            nx, ny, nz = x + dx, y + dy, z + dz
            if (nx, ny, nz) in self.occupied:
                continue
            if any(n < -SIZE or n > SIZE for n in (nx, ny, nz)):
                continue
            self.position = (nx, ny, nz)
            self.occupied.add(self.position)
            mx, my, mz = x + dx / 2.0, y + dy / 2.0, z + dz / 2.0
            self.add_cylinder((mx, my, mz), axis)
            if direction != self.direction:
                self.add_sphere((x, y, z))
            self.direction = direction
            return True
        # self.add_sphere(self.position)
        # if len(self.occupied) < (SIZE * 2 + 1) ** 3:
        #     self.restart()
        #     return True
        return False

def create_drawing():
    random.seed(1004)
    occupied = set()
    pipes = [Pipe(occupied) for _ in range(PIPES)]
    for _ in range(60000):
        done = True
        for pipe in pipes:
            if pipe.update():
                done = False
        if done:
            break
    print len(occupied)
    shapes = []
    for pipe in pipes:
        pipe.add_sphere(pipe.position)
        shapes.extend(pipe.shapes)
    print len(shapes)
    scene = xyz.Scene(shapes)
    paths = scene.render((25, 25, 10), (0, 0, 0), (0, 0, 1), 60, 1, 0.1, 100, 0.05)
    # paths.append([(-1, -1), (1, -1), (1, 1), (-1, 1), (-1, -1)])
    drawing = xy.Drawing(paths).rotate(90).scale_to_fit(315, 380).rotate(-90)
    return drawing

def main():
    try:
        drawing = xy.Drawing.load('pipes.dwg')
    except Exception:
        drawing = create_drawing()
    n = 50
    o = 25
    drawing = drawing.origin().crop(n, n + o, 315 - n, 315 - n + o).scale_to_fit(315, 315)
    drawing = drawing.sort_paths_greedy().join_paths()
    drawing.render().write_to_png('pipes.png')
    # drawing.save('pipes.dwg')
    xy.draw(drawing)

if __name__ == '__main__':
    main()
