import cv
import cv2
import numpy as np
import xy

def isolate_buildings(im):
    print 'isolate_buildings'
    c = np.array([233, 240, 242])
    n = 3
    return cv2.inRange(im, c - n, c + n)

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
    print 'main'
    im = cv2.imread('/Users/fogleman/Dropbox/long-beach.png')
    im = isolate_buildings(im)
    contours = find_contours(im)
    contours = filter_contours(contours)
    # contours = approximate_contours(contours)
    # im[:] = 0
    # cv2.drawContours(im, contours, -1, 255, -1)
    # cv2.imwrite('out.png', im)
    paths = contour_paths(contours)
    drawing = xy.Drawing(paths).rotate_and_scale_to_fit(315, 380, step=90)
    drawing.render().write_to_png('buildings.png')

if __name__ == '__main__':
    main()
