import time

class Metronome(object):
    """
Metronome class for limiting frames per second.

>>> m = Metronome
>>> m.start()
>>> while True:
        print 'Hi'
        m.sync()
    """
    def __init__(self, fps):
        """
Initialise a Metronome object. **fps** defines the amount of frames per second.

        """
        self.delay = 1./fps

    def start(self):
        """
Start the metronome
        """
        self.last = time.time()

    def sync(self):
        """
Wait if required.
        """
        now = time.time()
        if self.delay > now-self.last:
            time.sleep(self.delay - (now-self.last))
        self.last = max(now, self.last+self.delay)

