from PIL import Image
import math
import sys
import xy

COLORS = {
    '.': (255, 255, 255),
    'X': (0, 0, 0),
}

def get_points(im, color=(0, 0, 0)):
    result = []
    w, h = im.size
    for y in range(h):
        for x in range(w):
            if im.getpixel((x, y)) == color:
                result.append((x, y))
    return result

def create_paths(x, y):
    p = 0.01
    return [[
        (x - p, y - p),
        (x + p, y - p),
        (x + p, y + p),
        (x - p, y + p),
        (x - p, y - p),
    ]]

def find_pattern(im, pattern, colors=COLORS):
    w, h = im.size
    pw, ph = len(pattern[0]), len(pattern)
    result = []
    for y in range(h - len(pattern) + 1):
        for x in range(w - len(pattern[0]) + 1):
            ok = True
            for j, row in enumerate(pattern):
                for i, c in enumerate(row):
                    if not ok or c == '?':
                        continue
                    if im.getpixel((x + i, y + j)) != colors[c]:
                        ok = False
            if ok:
                result.append((x, y))
    return result

def find_bar(im):
    pattern = [
        'XX..',
        '.XXX',
        '.XXX',
        'XX..',
    ]
    return find_pattern(im, pattern)

def find_ghosts(im):
    pattern = [
        'XXXXXX',
        'XX.XXX',
        'X...XX',
    ]
    return find_pattern(im, pattern)

def find_dots(im):
    pattern = [
        '....',
        '.XX.',
        '.XX.',
        '....',
    ]
    return find_pattern(im, pattern)

def find_big_dots(im):
    pattern = [
        '........',
        '..XXXX..',
        '.XXXXXX.',
    ]
    return find_pattern(im, pattern)

def find_curve1(im):
    pattern = [
        '..XX',
        '.X..',
        'X...',
        'X...',
    ]
    return find_pattern(im, pattern)

def find_curve2(im):
    pattern = [
        'X...',
        'X...',
        '.X..',
        '..XX',
    ]
    return find_pattern(im, pattern)

def find_curve3(im):
    pattern = [
        'XX..',
        '..X.',
        '...X',
        '...X',
    ]
    return find_pattern(im, pattern)

def find_curve4(im):
    pattern = [
        '...X',
        '...X',
        '..X.',
        'XX..',
    ]
    return find_pattern(im, pattern)

def find_big_curve1(im):
    pattern = [
        '....X',
        '..XX.',
        '.X..?',
        '.X.??',
        'X.???',
    ]
    return find_pattern(im, pattern)

def find_big_curve2(im):
    pattern = [
        'X.???',
        '.X.??',
        '.X..?',
        '..XX.',
        '....X',
    ]
    return find_pattern(im, pattern)

def find_big_curve3(im):
    pattern = [
        'X....',
        '.XX..',
        '?..X.',
        '??.X.',
        '???.X',
    ]
    return find_pattern(im, pattern)

def find_big_curve4(im):
    pattern = [
        '???.X',
        '??.X.',
        '?..X.',
        '.XX..',
        'X....',
    ]
    return find_pattern(im, pattern)

def find_small_curve1(im):
    pattern = [
        '.....',
        '..XXX',
        '.X...',
        '.X...',
        '.X...',
    ]
    return find_pattern(im, pattern)

def find_small_curve2(im):
    pattern = [
        '.X...',
        '.X...',
        '.X...',
        '..XXX',
        '.....',
    ]
    return find_pattern(im, pattern)

def find_small_curve3(im):
    pattern = [
        '.....',
        'XXX..',
        '...X.',
        '...X.',
        '...X.',
    ]
    return find_pattern(im, pattern)

def find_small_curve4(im):
    pattern = [
        '...X.',
        '...X.',
        '...X.',
        'XXX..',
        '.....',
    ]
    return find_pattern(im, pattern)

def find_lines(im):
    result = []
    pattern = [
        '??.',
        '.XX',
        '??.',
    ]
    for x, y in find_pattern(im, pattern):
        x1, y1 = x + 1, y + 1
        x2, y2 = x1, y1
        while im.getpixel((x2 + 1, y2)) == COLORS['X']:
            x2 += 1
        if x2 - x1 > 2:
            result.append([(x1, -y1), (x2, -y2)])
    pattern = [
        '?.?',
        '?X?',
        '.X.',
    ]
    for x, y in find_pattern(im, pattern):
        x1, y1 = x + 1, y + 1
        x2, y2 = x1, y1
        while im.getpixel((x2, y2 + 1)) == COLORS['X']:
            y2 += 1
        if y2 - y1 > 2:
            result.append([(x1, -y1), (x2, -y2)])

    return result

def main():
    im = Image.open(sys.argv[1])

    paths = []

    # for x, y in get_points(im):
    #     paths.extend(create_paths(x, -y))

    # maze
    paths = []
    paths.extend(find_lines(im))
    for x, y in find_curve1(im):
        paths.append(xy.arc(x + 2, -y - 2, 2, 90, 180))
    for x, y in find_curve2(im):
        paths.append(xy.arc(x + 2, -y - 1, 2, 180, 270))
    for x, y in find_curve3(im):
        paths.append(xy.arc(x + 1, -y - 2, 2, 0, 90))
    for x, y in find_curve4(im):
        paths.append(xy.arc(x + 1, -y - 1, 2, 270, 360))
    for x, y in find_big_curve1(im):
        paths.append(xy.arc(x + 4, -y - 4, 4, 90, 180))
    for x, y in find_big_curve2(im):
        paths.append(xy.arc(x + 4, -y - 0, 4, 180, 270))
    for x, y in find_big_curve3(im):
        paths.append(xy.arc(x + 0, -y - 4, 4, 0, 90))
    for x, y in find_big_curve4(im):
        paths.append(xy.arc(x + 0, -y - 0, 4, 270, 360))
    for x, y in find_small_curve1(im):
        paths.append(xy.arc(x + 2, -y - 2, 1, 90, 180))
    for x, y in find_small_curve2(im):
        paths.append(xy.arc(x + 2, -y - 2, 1, 180, 270))
    for x, y in find_small_curve3(im):
        paths.append(xy.arc(x + 2, -y - 2, 1, 0, 90))
    for x, y in find_small_curve4(im):
        paths.append(xy.arc(x + 2, -y - 2, 1, 270, 360))
    for x, y in find_bar(im):
        paths.append([(x + 1, -y - 1), (x + 18, -y - 1)])
        paths.append([(x + 1, -y - 2), (x + 18, -y - 2)])
        paths.append([(x + 1, -y - 0), (x + 1, -y - 3)])
        paths.append([(x + 18, -y - 0), (x + 18, -y - 3)])
    maze_paths = xy.join_paths(xy.sort_paths_greedy(paths))

    # ghosts
    paths = []
    for x, y in find_ghosts(im):
        paths.append(xy.arc(x + 6.5, -y + 4.5, 6.5, 0, 180))
        paths.append([(x, -y + 4.5), (x, -y - 2)])
        paths.append([(x + 13, -y + 4.5), (x + 13, -y - 2)])
        paths.append([(x, -y - 2), (x + 2, -y)])
        paths.append([(x + 4, -y - 2), (x + 2, -y)])
        paths.append([(x + 4, -y - 2), (x + 6.5, -y)])
        paths.append([(x + 13, -y - 2), (x + 13 - 2, -y)])
        paths.append([(x + 13 - 4, -y - 2), (x + 13 - 2, -y)])
        paths.append([(x + 13 - 4, -y - 2), (x + 13 - 6.5, -y)])
    ghost_paths = xy.join_paths(xy.sort_paths_greedy(paths))

    # pacman
    paths = []
    x, y = 113, -189
    paths.append(xy.arc(x, y, 6.5, 225, 135 + 360))
    x1 = x + 6.5 * math.cos(math.radians(135))
    y1 = y + 6.5 * math.sin(math.radians(135))
    x2 = x + 6.5 * math.cos(math.radians(225))
    y2 = y + 6.5 * math.sin(math.radians(225))
    paths.append([(x1, y1), (x + 2, y)])
    paths.append([(x2, y2), (x + 2, y)])
    pacman_paths = xy.join_paths(xy.sort_paths_greedy(paths))

    # dots
    paths = []
    for x, y in find_dots(im):
        paths.append(xy.circle(x + 1.5, -y - 1.5, 1))
    for x, y in find_big_dots(im):
        paths.append(xy.circle(x + 3.5, -y - 4.5, 4))
    dot_paths = xy.join_paths(xy.sort_paths_greedy(paths))

    paths = maze_paths + ghost_paths + pacman_paths + dot_paths
    drawing = xy.Drawing(paths).scale_to_fit(315, 380)
    drawing.render().write_to_png('pac.png')
    xy.draw(drawing)

if __name__ == '__main__':
    main()
