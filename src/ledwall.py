import sync
import curses
import sys

import ext

keyevents = ext.input.CursesInput()

sys.path.append('..')

import animations
animations = [ x(12, 10) for x in animations.animations ]

if len(sys.argv) > 1 and sys.argv[1] == '-net':
    sys.path.append('net')
    import ledremote
    s = ledremote.RemoteLedScreen('nodejs', 8000)
else:
    import led
    s = led.LedScreen()

fps = 25.
metronome = sync.Metronome(fps)
metronome.start()

def blend(frame1, frame2, d):
    return [ [ [ int(frame2[y][x][c]*d - frame1[y][x][c]*(d-1.))
                 for c in xrange(3)  ]
                 for x in xrange(12) ]
                 for y in range(10)  ]

current = 0
c = 0;

wait_time, blend_time, shift_time = 30, 3, .5
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

