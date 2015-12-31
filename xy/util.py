from device import Device
from lines import Lines
from shapely.geometry import LineString
import time

def simplify(points, tolerance=0.05):
    if len(points) < 2:
        return points
    line = LineString(points)
    line = line.simplify(tolerance)
    return list(line.coords)

def draw(x):
    if isinstance(x, Lines):
        x = x.paths
    device = Device()
    time.sleep(2)
    device.pen_up()
    time.sleep(1)
    device.home()
    for path in x:
        device.draw(path)
