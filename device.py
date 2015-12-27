import serial

class Device(object):

    def __init__(self, port, verbose=False):
        self.serial = serial.Serial(port, 115200)
        self.verbose = verbose

    def read(self):
        data = []
        while True:
            c = self.serial.read(1)
            if c == '\n':
                return ''.join(data)
            data.append(c)

    def write(self, *args):
        line = ' '.join(map(str, args))
        if self.verbose:
            print line
        self.serial.write('%s\n' % line)
        response = self.read()
        if self.verbose:
            print response

    def home(self):
        self.write('G28')

    def move(self, x, y):
        x = 'X%s' % x
        y = 'Y%s' % y
        self.write('G1', x, y)

    def draw(self, points, up, down):
        if not points:
            return
        self.pen(up)
        self.move(*points[0])
        self.pen(down)
        for point in points:
            self.move(*point)
        self.pen(up)

    def pen(self, position):
        self.write('M1', position)

    def gcode(self, g):
        for line in g.lines:
            self.write(line)
