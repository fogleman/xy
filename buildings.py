import cv
import cv2
import numpy as np
import time
import xy

def isolate_buildings(im):
    print 'isolate_buildings'
    c = np.array([233, 240, 242])
    n = 3
    return cv2.inRange(im, c - n, c + n)

def combine_images():
    im1 = cv2.imread('/Users/fogleman/Workspace/maptiles/zoom18t.png')
    im2 = cv2.imread('/Users/fogleman/Workspace/maptiles/zoom19t.png')
    im3 = cv2.imread('/Users/fogleman/Workspace/maptiles/zoom20s.png')
    im1 = isolate_buildings(im1)
    im2 = isolate_buildings(im2)
    im3 = isolate_buildings(im3)
    im = cv2.bitwise_or(cv2.bitwise_or(im1, im2), im3)
    return im

def find_contours(im):
    print 'find_contours'
    contours, hierarchy = cv2.findContours(
        im, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    print len(contours), len(hierarchy)
    return contours

def filter_contours(contours):
    print 'filter_contours'
    result = []
    for x in contours:
        area = cv2.contourArea(x)
        if area >= 100:
            result.append(x)
    return result

def approximate_contours(contours):
    print 'approximate_contours'
    result = []
    for x in contours:
        epsilon = 0.005 * cv2.arcLength(x, True)
        approx = cv2.approxPolyDP(x, epsilon, True)
        result.append(approx)
    return result

def contour_paths(contours):
    print 'contour_paths'
    result = []
    for x in contours:
        points = [tuple(p) for p in x.ravel().reshape(-1, 2).tolist()]
        points.append(points[0])
        result.append(points)
    return result

def main():
    device = xy.Device()
    time.sleep(2)
    device.pen_up()
    time.sleep(1)
    device.home()
    print 'main'
    im = cv2.imread('/Users/fogleman/Workspace/maptiles/zoom20clean.png')
    im = isolate_buildings(im)
    # im = combine_images()
    contours = find_contours(im)
    contours = filter_contours(contours)
    print len(contours)
    im[:] = 0
    cv2.drawContours(im, contours, -1, 255, -1)
    cv2.imwrite('out.png', im)
    paths = contour_paths(contours)
    print 'scaling paths'
    drawing = xy.Drawing(paths).rotate_and_scale_to_fit(315, 380, step=90).scale(1, -1)
    drawing = drawing.move(300, 0, 1, 0)
    drawing.render().write_to_png('buildings.png')
    print 'drawing paths'
    paths = drawing.paths
    paths.sort(key=lambda path: path[0][1])
    n = 100
    for i in range(0, len(paths), n):
        print i
        group = paths[i:i+n]
        group.sort(key=lambda path: path[0][0])
        for path in group:
            device.draw(xy.simplify(path, 0.05))

if __name__ == '__main__':
    main()
