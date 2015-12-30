from shapely.geometry import LineString

def simplify(points, tolerance=0.05):
    if len(points) < 2:
        return points
    line = LineString(points)
    line = line.simplify(tolerance)
    return list(line.coords)
