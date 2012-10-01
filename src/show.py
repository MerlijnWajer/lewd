import led
import sync
import sys
import time

sys.path.append('..')

import animations
animations = [ x(12, 10) for x in animations.animations ]

s = led.LedScreen()

metronome = sync.Metronome(fps=25.)
metronome.start()
current = 0

start = time.time()
delay = 120.

while True:
    current = int((time.time()-start)/delay) % len(animations)
    s.push_frame(animations[current].next())
    metronome.sync()

