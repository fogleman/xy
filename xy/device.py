import serial
import time

PORT = '/dev/tty.wchusbserial640'
BAUD = 115200

UP = 0
DOWN = 50

class Device(object):

    def __init__(self, port=PORT, baud=BAUD, up=UP, down=DOWN, verbose=False):
        self.serial = serial.Serial(port, baud) if port else None
        self.up = up
        self.down = down
        self.verbose = verbose

    def read(self):
        data = []
        while True:
            c = self.serial.read(1) if self.serial else '\n'
            if c == '\n':
                return ''.join(data)
            data.append(c)

    def write(self, *args):
        line = ' '.join(map(str, args))
        if self.verbose:
            print line
        if self.serial:
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

    def pen(self, position):
        self.write('M1', position)

    def pen_up(self):
        self.pen(self.up)

    def pen_down(self):
        self.pen(self.down)

    def draw(self, points, up=None, down=None):
        if not points:
            return
        self.pen(self.up if up is None else up)
        self.move(*points[0])
        self.pen(self.down if down is None else down)
        time.sleep(0.15)
        for point in points:
            self.move(*point)
        self.pen(up)

    def gcode(self, g):
        for line in g.lines:
            self.write(line)
