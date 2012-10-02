import sys, os
import socket
from transform import Transform
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))

class RemoteLedScreen(object):
    def __init__(self, host, port, dim=(12,10)):
        """
Set Host and Port to where the net.py server is running.

Usage:

>>> screen = RemoteLedScreen('wallserver', 8000)
        """
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        self.w, self.h = dim
        self.buf = [(0, 0, 0)] * self.w * self.h
        self.transform = Transform(*dim)

        # We could cache a possible exception but let's leave it for now
        #print "ohai"
        #self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
        #print "dat sock"
        self.sock = socket.create_connection((host, port))

    def __setitem__(self, tup, val):
        """
Allows for easy frame access.
Use like:

>>> screen[(x, y)] = r, g, b
        """
        if type(tup) not in (tuple, list) or len(tup) != 2:
            raise ValueError("tup should be a tuple of length 2")

        if type(val) not in (tuple, list) or len(val) != 3:
            raise ValueError("val should be a tuple of length 3")

        if tup[0] not in range(0, self.w) or tup[1] not in range(0, self.h):
            raise ValueError("tup should be inside the grid:", (self.w, self.h))

        self.buf[self.transform.inverse(tup)] = val

    def push(self):
        """
Push the current frame contents to the screen.

>>> screen.push()
        """
        self.sock.send(''.join(chr(r)+chr(g)+chr(b) for r,g,b in self.buf))

    def load_data(self, data):
        socket.send(data)

    def load_frame(self, frame):
        """
Load internal frame from *frame*. Does not send anything yet.
Frame is a two dimensional array.
        """
        for y in xrange(max(len(frame), self.h)):
            for x in xrange(max(len(frame[y]), self.w)):
                self[ (x, y) ] = frame[y][x]

    def push_frame(self, frame):
        """
Push a frame to the screen
        """
        self.load_frame(frame)
        self.push()

if __name__ == '__main__':
    screen = RemoteLedScreen('nosejs', 8000)

    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()
