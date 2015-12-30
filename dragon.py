import time
import xy

def main(iteration):
    t = xy.Turtle()
    for i in range(1, 2 ** iteration):
        t.forward(8)
        if (((i & -i) << 1) & i) != 0:
            t.circle(-8, 90)
        else:
            t.circle(8, 90)

    im = t.render()
    im.write_to_png('dragon.png')

    device = xy.Device()
    time.sleep(3)
    device.pen_up()
    device.home()
    # TODO: scale / translate paths to proper plotter range
    for path in t.get_paths():
        device.draw(path)

if __name__ == '__main__':
    main(11)
