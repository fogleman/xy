from math import hypot
from shapely.geometry import LineString

def sort_points(points):
    result = []
    p = min(points)
    points.remove(p)
    result.append(p)
    while points:
        px, py = result[-1]
        p = min(points, key=lambda (x, y): hypot(x - px, y - py))
        points.remove(p)
        result.append(p)
    return result

def simplify(points, tolerance=0.1):
    if len(points) < 2:
        return points
    line = LineString(points)
    line = line.simplify(tolerance)
    return list(line.coords)
