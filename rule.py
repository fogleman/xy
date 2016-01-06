from shapely import geometry
import xy

def compute_row(rule, previous):
    row = []
    previous = '00' + previous + '00'
    for i in range(len(previous) - 2):
        x = int(previous[i:i+3], 2)
        y = '1' if rule & (1 << x) else '0'
        row.append(y)
    return ''.join(row)

def compute_rows(rule, n):
    rows = ['1']
    for _ in range(n - 1):
        rows.append(compute_row(rule, rows[-1]))
    return rows

def pad(rows):
    result = []
    n = len(max(rows, key=len))
    for row in rows:
        p = (n - len(row)) / 2 + 1
        row = '.' * p + row + '.' * p
        result.append(row)
    return result

def trim(rows):
    return [row.strip('.') for row in rows]

def crop(rows):
    w = len(rows[0])
    h = len(rows)
    n = h / 2
    i = w / 2 - n / 2
    j = i + n
    return [row[i:j] for row in rows[-n:]]

def crop_diagonal(rows):
    rows = trim(rows)
    result = []
    for i, row in enumerate(rows):
        if i < len(rows) / 2:
            result.append(row)
        else:
            j = 2 * (i - len(rows) / 2 + 1)
            result.append(row[j:-j])
    return result

def trim_pair(pair, d):
    line = geometry.LineString(pair)
    p1 = line.interpolate(d)
    p2 = line.interpolate(line.length - d)
    return ((p1.x, p1.y), (p2.x, p2.y))

def form_pairs(rows):
    pairs = []
    for y, row in enumerate(rows):
        if y == 0:
            continue
        for x, value in enumerate(row):
            if value != '1':
                continue
            i = x - len(rows[-1]) / 2
            j = y
            if rows[y - 1][x - 1] == '1':
                pairs.append(((i - 1, j - 1), (i, j)))
            if rows[y - 1][x] == '1':
                pairs.append(((i, j - 1), (i, j)))
            if rows[y - 1][x + 1] == '1':
                pairs.append(((i + 1, j - 1), (i, j)))
    points = set()
    for (x1, y1), (x2, y2) in pairs:
        points.add((x1, y1))
        points.add((x2, y2))
    return pairs, points

def create_drawing(rule, h):
    rows = compute_rows(rule, h)
    rows = pad(rows)
    rows = crop_diagonal(rows)
    # rows = crop(rows)
    rows = pad(rows)
    pairs, points = form_pairs(rows)
    paths = [trim_pair(x, 0.25) for x in pairs]
    for x, y in points:
        paths.append(xy.circle(x, y, 0.25))
    drawing = xy.Drawing(paths)
    drawing = drawing.scale(1, -1).rotate(45)
    drawing = drawing.scale_to_fit(315, 380)
    return drawing

def main():
    h = 128
    for rule in [30]:#range(256):
        print rule
        drawing = create_drawing(rule, h)
        im = drawing.render()#line_width=1.25)
        im.write_to_png('rule%03d.png' % rule)
        drawing = drawing.sort_paths_greedy()
        xy.draw(drawing)

if __name__ == '__main__':
    main()
