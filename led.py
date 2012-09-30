"""Low-level interface to the LED Wall at TechInc. http://techinc.nl"""

import sys
sys.path.append('uspp')

# Python serial communication module. Get it from pypi.
import uspp

from transform import transform_led, reverse_led

__all__ = ['LedScreenException', 'LedScreen']

class LedScreenException(Exception):
    pass

class LedScreen(object):
    """
    The low-level LED wall screen.
    """

    def __init__(self, fname='/dev/ttyACM0', brate=115200, dim=(12,10)):
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        self.tty = uspp.SerialPort(fname, speed=brate, timeout=0)
        self.w, self.h = dim
        self.buf = [(0, 0, 0)] * 12*10

    def __setitem__(self, tup, val):
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        if tup[0] not in range(0, self.w) or tup[1] not in range(0, self.h):
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        self.buf[reverse_led(tup)] = val

        #_ = self.tty.read()

    def push(self):
        for ind, val in enumerate(self.buf):
            self.tty.write(chr(ind) + ''.join(map(lambda x: chr(x), val)))

    def __iter__(self):
        return LedScreenIterator(self)

class LedScreenIterator(object):
    def __init__(ls):
        pass

if __name__ == '__main__':
    screen = LedScreen()
    screen[0, 0] = (10, 10, 10)


    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()

