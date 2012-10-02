import led
import sync
import sys
import time

sys.path.append('..')

if len(sys.argv) > 1 and sys.argv[1] == '-net':
    sys.path.append('net')
    import ledremote
    s = ledremote.RemoteLedScreen('nodejs', 8000)
else:
    import led
    s = led.LedScreen()

import animations
animations = [ x(12, 10) for x in animations.animations ]

fps = 25.

metronome = sync.Metronome(fps)
metronome.start()

start = time.time()
delay, blendtime = 20, 10

delay_frames, blend_frames = int(delay*fps), int(blendtime*fps)

def blend(frame1, frame2, d):
    return [ [ [ int(frame2[y][x][c]*d - frame1[y][x][c]*(d-1.))
                 for c in xrange(3)  ]
                 for x in xrange(12) ]
                 for y in range(10)  ]


current = 0

while True:
    for i in xrange(delay_frames):
        s.push_frame(animations[current].next())
        metronome.sync()

    last = current
    current += 1
    current %= len(animations)

    for i in xrange(blend_frames):
        s.push_frame(blend(animations[last].next(),
                           animations[current].next(),
                           float(i)/blend_frames))
        metronome.sync()
