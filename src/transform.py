""" Module for the linear transform from 2D coordinate system to LED wall"""
__all__ = [ 'Transform' ]

class Transform(object):
    """
Transform class to transform a RGB led index to x and y plus the reverse
transform.

>>> t = Transform()
>>> print t.translate(10)
    """

    def __init__(self, w=12, h=10):
        self.w, self.h = w, h

    def translate(self, ind):
        """ Transform index to x, y. Top-left = (0, 0) """
        w, h = self.w, self.h

        x = w-1 - ind / h

        if x % 2 == 0:
            y = (h - 1) - (ind % h)
        else:
            y = ind % h

        return (w-x-1, (h - 1) -y)

    def inverse(self, (x, y)):
        """ Transform (x, y) to index """
        w, h = self.w, self.h

        if x % 2 == 0:
            ind = h*(x+1)-1 - y
        else:
            ind = h*x + y
        return ind

