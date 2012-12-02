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
import sys, os

sys.path.append(os.path.abspath(os.path.dirname(__file__) + '../'))
import abstractled

import pygame
pygame.init()

black = (0, 0, 0)

class VirtualLedScreen(abstractled.AbstractLed):
    def __init__(self, dimension=(12,10), ssize=(600, 500)):
        abstractled.AbstractLed.__init__(self, dimension)
        self.screen = pygame.display.set_mode(ssize,
                pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.screen.fill(black)
        self.sx, self.sy = float(ssize[0]) / dimension[0], \
            float(ssize[1]) / dimension[1]

    def draw_led(self, surf, x, y, w, h, color):
        hindcolor = tuple( int(((x/255.)**.6) * 20) for x in color )
        midcolor = tuple( int(((x/255.)**.6) * 127.5) for x in color )
        ledcolor = tuple( min(255, int(((x/255.)**.6) * 765)) for x in color )
        for dim, bcolor in (1, hindcolor), (.4, midcolor), (.2, ledcolor): 
            bx, by = int(x+w*(1-dim)/2), int(y+h*(1-dim)/2)
            bw, bh = int(w*dim), int(h*dim)
            pygame.draw.rect(surf, bcolor, pygame.Rect(bx, by, bw, bh))

    def draw(self):
        surf = pygame.display.get_surface()
        for x in xrange(self.w):
            for y in xrange(self. h):
                i = x + y * self.w
                self.draw_led(surf, x * self.sx, y * self.sy, self.sx, self.sy, self.buf[i])

    def check_events(self):
        for event in pygame.event.get():
            if event.type in (pygame.QUIT,):
                sys.exit(0)
            if event.type in (pygame.VIDEORESIZE,):
                self.screen = pygame.display.set_mode((event.w, event.h),
                        pygame.RESIZABLE | pygame.DOUBLEBUF)
                self.sx, self.sy = float(event.w) / self.w, \
                        float(event.h) / self.h



    def push(self):
        self.check_events()
        self.draw()
        pygame.display.flip()
        self.screen.fill(black)
