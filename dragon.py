import xy

def main(iteration):
    t = xy.Turtle()
    for i in range(1, 2 ** iteration):
        t.forward(1)
        if (((i & -i) << 1) & i) != 0:
            t.circle(-1, 90, 36)
        else:
            t.circle(1, 90, 36)
    drawing = t.drawing.rotate_and_scale_to_fit(315, 380, step=90).scale(1, -1).origin()
    drawing.render().write_to_png('dragon.png')
    xy.draw(drawing)

if __name__ == '__main__':
    main(13)
