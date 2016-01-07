from device import Device
from drawing import Drawing
from shapely.geometry import LineString
import math
import time

def simplify(points, tolerance=0.05):
    if len(points) < 2:
        return points
    line = LineString(points)
    line = line.simplify(tolerance)
    return list(line.coords)

def join_paths(paths, tolerance=0.05):
    if len(paths) < 2:
        return paths
    result = [list(paths[0])]
    for path in paths[1:]:
        x1, y1 = result[-1][-1]
        x2, y2 = path[0]
        d = math.hypot(x2 - x1, y2 - y1)
        if d <= tolerance:
            result[-1].extend(path)
        else:
            result.append(list(path))
    return result

def draw(x, tolerance=0.05):
    if isinstance(x, Drawing):
        x = x.paths
    device = Device()
    time.sleep(2)
    device.pen_up()
    time.sleep(1)
    device.home()
    for i, path in enumerate(x):
        print i, len(x)
        if tolerance:
            path = simplify(path, tolerance)
        device.draw(path)

def parse_svg_path(line):
    paths = []
    path = []
    for token in line.split():
        cmd = token[0].upper()
        x, y = map(float, token[1:].split(','))
        if cmd == 'M':
            if len(path) > 1:
                paths.append(path)
            path = [(x, y)]
        elif cmd == 'L':
            path.append((x, y))
    if len(path) > 1:
        paths.append(path)
    return paths
