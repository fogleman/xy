import math
import random
import xy

def low_pass(values, alpha):
    result = []
    y = 0.0
    for x in values:
        y = y - (alpha * (y - x))
        result.append(y)
    return result

def normalize(values, new_lo, new_hi):
    result = []
    lo = min(values)
    hi = max(values)
    for x in values:
        p = (x - lo) / (hi - lo)
        x = new_lo + p * (new_hi - new_lo)
        result.append(x)
    return result

random.seed(13)

N = 400

noises = [random.random() * 2 - 1 for _ in range(N)]
for _ in range(3):
    noises = low_pass(noises, 0.2)
noises = normalize(noises, -1, 1)

paths = []
x = 0
y = 0
m = 0.5
for i, n in enumerate(noises):
    r = i + 1 #N - i
    paths.append(xy.circle(x, y, r, 120))
    a = n * math.pi
    x += math.cos(a) * m
    y += math.sin(a) * m

drawing = xy.Drawing(paths)
s = 315 / 2.0
drawing = drawing.crop(-s, -s, s, s)
drawing.render().write_to_png('contain.png')
