"""
  This file is part of the LEd Wall Daemon (lewd) project
  Copyright (c) 2009-2012 by ``brainsmoke'' and Merlijn Wajer (``Wizzup'')

    lewd is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    lewd is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with lewd.  If not, see <http://www.gnu.org/licenses/>.

  See the file COPYING, included in this distribution,
  for details about the copyright.
"""
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

