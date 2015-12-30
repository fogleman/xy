import xy

def turn(i):
    left = (((i & -i) << 1) & i) != 0
    return 'L' if left else 'R'

def main():
    iteration = 11
    n = 2 ** iteration - 1
    t = xy.Turtle()
    for i in range(1, n + 1):
        t.forward(8)
        if turn(i) == 'L':
            t.circle(-8, 90, 36)
        else:
            t.circle(8, 90, 36)
    im = t.render()
    im.write_to_png('turtle.png')

if __name__ == '__main__':
    main()
