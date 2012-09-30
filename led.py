import sys
sys.path.append('uspp')

import uspp

from transform import transform_led, reverse_led

class LedScreenException(Exception):
    pass

class LedScreen(object):
    """
    """

    def __init__(self, fname='/dev/ttyACM0', brate=115200):
        self.tty = uspp.SerialPort(fname, speed=brate)

    def __setitem__(self, tup, val):
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise Exception("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise Exception("val should be a tuple of length 3")

        self.tty.write(chr(reverse_led(tup)) + ''.join(map(lambda x: chr(x), val)))

if __name__ == '__main__':
    screen = LedScreen()
    screen[0, 0] = (10, 10, 10)


    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

