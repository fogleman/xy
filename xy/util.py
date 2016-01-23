from device import Device
from shapely.geometry import LineString
import drawing
import math
import progress
import time

def simplify(points, tolerance=0.05):
    if len(points) < 2:
        return points
    line = LineString(points)
    line = line.simplify(tolerance)
    return list(line.coords)

def simplify_paths(paths, tolerance=0.05):
    return [simplify(x, tolerance) for x in paths]

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

def remove_duplicates(paths):
    result = []
    seen = set()
    for path in paths:
        key = tuple((x, y) for x, y in path)
        if key in seen:
            continue
        seen.add(key)
        result.append(path)
    return result

def draw(x, tolerance=0.05):
    if isinstance(x, drawing.Drawing):
        x = x.paths
    device = Device()
    time.sleep(2)
    device.pen_up()
    time.sleep(1)
    device.home()
    bar = progress.Bar()
    for path in bar(x):
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
