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

