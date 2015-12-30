from shapely.geometry import Polygon, MultiPolygon
import shapefile
import xy

STATES = '/Users/fogleman/Workspace/Carolina/shapefiles/cb_2014_us_state_20m/albers.shp'
COUNTIES = '/Users/fogleman/Workspace/Carolina/shapefiles/cb_2013_us_county_5m/albers.shp'

def shape_to_polygons(shape):
    result = []
    parts = list(shape.parts) + [len(shape.points)]
    for i1, i2 in zip(parts, parts[1:]):
        points = map(tuple, shape.points[i1:i2])
        result.append(Polygon(points))
    return result

def load_shapes(path):
    skip = set(['02', '15', '60', '66', '69', '78', '72'])
    result = []
    sf = shapefile.Reader(path)
    for item in sf.shapeRecords():
        if item.record[0] in skip:
            continue
        result.extend(shape_to_polygons(item.shape))
    return result

def main():
    mm = 25.4
    w = 8.5 * mm
    h = 11 * mm
    p = 0.5 * mm
    states = MultiPolygon(load_shapes(STATES))
    # counties = MultiPolygon(load_shapes(COUNTIES))
    # counties = counties.simplify(100)
    g = xy.GCode.from_geometry(states)
    g = g.rotate(90)
    g = g.scale_to_fit(w, h, p).move(w / 2, p, 0.5, 0)
    # im = g.render(0, 0, w, h, 96 / mm)
    # im.write_to_png('usa.png')
    # g.save('usa.nc')
    device = xy.Device()
    device.home()
    device.gcode(g)

if __name__ == '__main__':
    main()
