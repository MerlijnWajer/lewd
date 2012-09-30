""" Module for the linear transform from 2D coordinate system to LED wall"""
__all__ = ['transform_led', 'reverse_led']

def transform_led(ind):
    """ Transform index to x, y. Top-left = (0, 0) """
    x = ind / 10
    #y = ind % 10

    if x % 2 == 0:
        y = 9 - (ind % 10)
    else:
        y = ind % 10

    return (x, y)

def reverse_led((x, y)):
    """ Transform (x, y) to index """
    if x % 2 == 0:
        ind = y + x*10
    else:
        ind = (9 - y) + x*10
    return ind

