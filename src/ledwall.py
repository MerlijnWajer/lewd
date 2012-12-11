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
import sync
import curses
import sys

import ext

keyevents = ext.input.CursesInput()

sys.path.append('..')

all_animations = True
use_socket = False
use_vled = False
use_spi = False

for arg in sys.argv[1:]:
    if arg == '-net':
        use_socket = True
    if arg == '-select':
        all_animations = False
    if arg == '-local':
        use_vled = True
    if arg == '-spi':
        use_spi = True

import animations

if all_animations:
    animations = [ x(12, 10) for x in animations.animations ]
else:
    animations = [
        animations.wobble.Wobble(12, 10),
        animations.drops.Drops(12, 10),
        animations.fire.Fire(12, 10),
        animations.plasma.Plasma(12, 10),
        animations.fire.Fire(12, 10),
        animations.lsdwall.Wobble(12, 10),
        animations.drops.Drops(12, 10),
    ]

if use_socket:
    sys.path.append('net')
    import ledremote
    s = ledremote.RemoteLedScreen('ledwall', 8000)
elif use_vled:
    sys.path.append('virtual')
    import vled
    s = vled.VirtualLedScreen(ssize=(600, 500))
elif use_spi:
    import ledspi
    s = ledspi.LedSPI()
else:
    import led
    s = led.LedScreen()

fps = 50.
metronome = sync.Metronome(fps)
metronome.start()

def blend(frame1, frame2, d):
    return [ [ [ int(frame2[y][x][c]*d - frame1[y][x][c]*(d-1.))
                 for c in xrange(3)  ]
                 for x in xrange(12) ]
                 for y in range(10)  ]

current = 0
c = 0;

wait_time, blend_time, shift_time = 20, 5, .5
wait_frames = int(wait_time*fps)
blend_frames = int(blend_time*fps)
shift_frames = int(shift_time*fps)

def animate_blend(s, ani1, ani2, numframes):
    for i in xrange(numframes):
        s.push_frame(blend(ani1.next(), ani2.next(), i/float(numframes)))
        metronome.sync()

locked = False

try:
    while True:
        if not locked:
            c+=1

        f = keyevents.poll()

        if f == 'q':
            break

        elif f == ',':
            last = current
            current -=1;
            current %= len(animations)
            c=0
            animate_blend(s, animations[last], animations[current], shift_frames)
        elif f == '.':
            last = current
            current +=1;
            current %= len(animations)
            animate_blend(s, animations[last], animations[current], shift_frames)
            c=0

        elif c == wait_frames:
            last = current
            current +=1;
            current %= len(animations)
            animate_blend(s, animations[last], animations[current], blend_frames)
            c=0

        elif f == 'l':
            locked = not locked

        s.push_frame(animations[current].next())

        metronome.sync()

finally:
    pass
    curses.reset_shell_mode()

