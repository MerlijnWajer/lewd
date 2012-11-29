import sys, os
import socket
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
import abstractled

class RemoteLedScreen(abstractled.AbstractLed):
    def __init__(self, host, port, dim=(12,10)):
        """
Set Host and Port to where the net.py server is running.

Usage:

>>> screen = RemoteLedScreen('wallserver', 8000)
        """
        if type(dim) not in (tuple, list) or len(dim) != 2:
            raise ValueError("Invalid dimension. Format is tuple(x,y)")
        self.w, self.h = dim

        #self.sock = socket.create_connection((host, port))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

    def push(self):
        """
Push the current frame contents to the screen.

>>> screen.push()
        """
        self.sock.send(''.join([chr(x) for x in self.buf[::]]))

if __name__ == '__main__':
    screen = RemoteLedScreen('nosejs', 8000)

    for x in range(12):
        for y in range(10):
            screen[(x,y)] = 25, 25, 25

    screen.push()
