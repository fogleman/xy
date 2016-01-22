import math

def circle(x=0, y=0, r=1, n=36):
    result = []
    for i in range(n + 1):
        p = i / float(n)
        a = 2 * math.pi * p
        px = x + math.cos(a) * r
        py = y + math.sin(a) * r
        result.append((px, py))
    return result

def arc(x=0, y=0, r=1, a1=0, a2=360, n=36):
    result = []
    for i in range(n + 1):
        p = i / float(n)
        a = math.radians(a1 + (a2 - a1) * p)
        px = x + math.cos(a) * r
        py = y + math.sin(a) * r
        result.append((px, py))
    return result
