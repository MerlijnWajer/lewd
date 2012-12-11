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
""" Simple ``move'' animation. Use w,a,s,d to move, q to stop"""
#import led
import sync
from ext import CursesInput
__import__('sys').path.append('./net')
import ledremote

#s = led.LedScreen()
s = ledremote.RemoteLedScreen('ledwall', 8000)

ci = CursesInput()

pos = (0, 0)

lastch = -1

metronome = sync.Metronome(fps=25.)
metronome.start()

try:
    while True:
        for x in range(12):
            for y in range(10):
                s[(x, y)] = 25, 25, 25

        # Set our pos
        s[(pos[0], pos[1])] = 255, 0, 0

        f = ci.poll()

        if f != None:
            lastch = f

        if f == 'q':
            break

        if lastch == 'w':
            if pos[0]+1>11:
                pos = (0, pos[1])
            else:
                pos = (pos[0]+1,pos[1])
        elif lastch == 's':
            if pos[0] - 1 < 0:
                pos = (11, pos[1])
            else:
                pos = (pos[0]-1, pos[1])
        elif lastch == 'a':
            if pos[1]+1 > 9:
                pos = (pos[0], 0)
            else:
                pos = (pos[0], pos[1]+1)
        elif lastch == 'd':
            if pos[1]-1 < 0:
                pos = (pos[0], 9)
            else:
                pos = (pos[0],pos[1]-1)

        s.push()

        metronome.sync()

finally:
    del ci

