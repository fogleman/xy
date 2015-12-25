from device import Device
import time

def main():
    device = Device('/dev/tty.wchusbserial1420')
    # time.sleep(2)
    device.home()
    device.move(10, 10)
    device.home()
    device.pen(40)
    time.sleep(1)
    device.pen(0)

if __name__ == '__main__':
    main()
