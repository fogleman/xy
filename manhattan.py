from imposm.parser import OSMParser
from math import radians, sin, cos
import time
import xy

LAT, LNG = (40.777274, -73.967161)

def laea(lat, lng, clat, clng, scale=1):
    lng, lat = radians(lng), radians(lat)
    clng, clat = radians(clng), radians(clat)
    k = (2 / (1 + sin(clat) * sin(lat) + cos(clat) * cos(lat) * cos(lng - clng))) ** 0.5
    x = k * cos(lat) * sin(lng - clng)
    y = k * (cos(clat) * sin(lat) - sin(clat) * cos(lat) * cos(lng - clng))
    return (x * scale, y * -scale)

def project(lat, lng):
    return laea(lat, lng, LAT, LNG)

class Handler(object):
    def __init__(self):
        self.nodes = {}
        self.ways = {}
        self.building_ways = []
        self.building_relations = []
    def on_coords(self, coords):
        for osmid, lng, lat in coords:
            self.nodes[osmid] = project(lat, lng)
    def on_nodes(self, nodes):
        for osmid, _, (lng, lat) in nodes:
            self.nodes[osmid] = project(lat, lng)
    def on_ways(self, ways):
        for osmid, tags, refs in ways:
            self.ways[osmid] = refs
            if 'building' in tags:
                self.building_ways.append(osmid)
    def on_relations(self, relations):
        for _, tags, members in relations:
            if 'building' in tags:
                self.building_relations.append(members)
    def create_paths(self):
        paths = []
        for osmid in self.building_ways:
            try:
                paths.append(self.create_path_for_way(osmid))
            except Exception:
                pass
        for members in self.building_relations:
            for osmid, member_type, role in members:
                if member_type != 'way':
                    continue
                try:
                    paths.append(self.create_path_for_way(osmid))
                except Exception:
                    pass
        return paths
    def create_path_for_nodes(self, refs):
        return [self.nodes[x] for x in refs]
    def create_path_for_way(self, osmid):
        return self.create_path_for_nodes(self.ways[osmid])

def main():
    device = xy.Device()
    time.sleep(2)
    device.pen_up()
    time.sleep(1)
    device.home()
    print 'parsing osm file'
    h = Handler()
    p = OSMParser(None, h.on_nodes, h.on_ways, h.on_relations, h.on_coords)
    p.parse('/Users/fogleman/Workspace/Manhattan/osm/manhattan.osm.pbf')
    print 'creating paths'
    paths = h.create_paths()
    print len(paths)
    print 'creating drawing'
    drawing = xy.Drawing(paths).scale(1, -1).scale_to_fit(315, 380)
    # print 'rendering drawing'
    # drawing.render().write_to_png('manhattan.png')
    paths = drawing.paths
    paths.sort(key=lambda path: path[0][1])
    n = 250
    for i in range(0, len(paths), n):
        print i
        for path in xy.sort_paths(paths[i:i+n], 500000):
            device.draw(xy.simplify(path, 0.1))

if __name__ == '__main__':
    main()
