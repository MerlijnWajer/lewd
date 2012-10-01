""" Module for the linear transform from 2D coordinate system to LED wall"""
__all__ = ['transform_led', 'reverse_led', 'set_transform']

w, h = 0, 0

def set_transform(ww, hh):
    w = ww
    h = hh

def transform_led(ind):
    """ Transform index to x, y. Top-left = (0, 0) """
    x = ind / h

    if x % 2 == 0:
        y = (h - 1) - (ind % h)
    else:
        y = ind % h

    return (x, y)

def reverse_led((x, y)):
    """ Transform (x, y) to index """
    if x % 2 == 0:
        ind = y + x*h
    else:
        ind = ((h - 1) - y) + x*h
    return ind

