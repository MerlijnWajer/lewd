"""Low-level interface to the LED Wall at TechInc. http://techinc.nl"""

import sys
sys.path.append('uspp')

# Python serial communication module. Get it from pypi.
import uspp

from transform import transform_led, reverse_led

__all__ = ['LedScreenException', 'LedScreen']


_ = """
TODO:
- Make it run standalone (that is, without requiring the nodejs to set up some
initial stuff)
- Add (optional!) buffering to just send an entire frame at once, seeing led
frames are mostly accessed using __setitem__
- Add __iter__ support
- Add (low-level!) networking support
- Layer for even nicer led access?

FUTURE:
- Middleware for more ``noob friendly'' API. (Pushing XML, JSON, etc)
- Networking (WebSockets, etc)
- Authentication API? (Including logging)
- Think about nice ways to make writing animations easy (brainsmoke did
something nice in python, probably port his code)

FUTURE-FUTURE:
- Maemo 5 application?
- Web interface for switching animations (probably using websockets to
communicate to middleware)
- Web interface to actually control leds as well (websockets, perhaps something
nice interactive can be done using canvas as well)
"""

class LedScreenException(Exception):
    pass

class LedScreen(object):
    """
    The low-level LED wall screen.
    """

    def __init__(self, fname='/dev/ttyACM0', brate=115200, dim=(12,10)):
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        self.tty = uspp.SerialPort(fname, speed=brate)
        self.w, self.h = dim

    def __setitem__(self, tup, val):
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        if tup[0] not in range(0, self.w) or tup[1] not in range(0, self.h):
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        self.tty.write(chr(reverse_led(tup)) + ''.join(map(lambda x: chr(x), val)))

    def __iter__(self):
        return LedScreenIterator(self)

class LedScreenIterator(ls):
    pass

if __name__ == '__main__':
    screen = LedScreen()
    screen[0, 0] = (10, 10, 10)


    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

