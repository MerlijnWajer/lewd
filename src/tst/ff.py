# -*- encoding: utf-8
"""
ff.py is an implementation of a forest fire cellular automaton.
It features a rich command-line frontend, two backend implementations to choose
from and allows pretty much every factor to be customised through the command
line. It can also automagically find the critical density either by performing a
binary search or by creating density graphs.

Most of the code is not or hardly documented, mainly because the code is quite
simple, readable and should generally explain itself. Note that some features
were added incrementally and some old features (like draw status) might not
function properly in combination with other features. The different search
algorithms plus visualisation of these searches with matplotlib made the code a
bit more cluttered that we'd like, but there's no point in reworking everything
now; it just works.™

To use the (non default) numpy backend, you need both numpy and scipy. To
create graphs, you need matplotlib. To create PNGs, you need PIL.
"""

import random

import Image, ImageDraw
from optparse import OptionParser

# NOTE: In order for the NumPy version
# to work, these values must not be changed.
BARREN = 0
VEGGIE = 1
FIRE = 2
BURNT = 3

# Von Neumann
spread = \
 [[0, 1, 0],
  [1, 0, 1],
  [0, 1, 0]]

oparse = OptionParser()
oparse.add_option('-s', '--size', dest='grid_size',
        help='Grid size. Default is 30.',
        default=30, type=int)
oparse.add_option('-m', '--step-max', dest='max_steps',
        help='Max steps to simulate. Default is off.',
        default=0, type=int)
oparse.add_option('-d', '--density', dest='density',
        help='Density of vegetation. Default is 0.5.',
        default=0.5, type=float)
oparse.add_option('-p', '--print', dest='drawactions',
        help='Draw method. Valid is `png\', \'mpl\' and `term\'. '+
        'Default is off.', default=[], action='append', type=str)
oparse.add_option('--ppc', dest='ppc',
        help='Pixels per cell for print type `png\'. Default is 10.',
        default=10, type=int)
oparse.add_option('--spread-format', dest='spread',
        help='Spread format. Must be a NxN list with format: (0|1),...(0|1).'\
        ' Default is Von Neumann spread.',
        default='', type=str)
oparse.add_option('--sleep', dest='sleep',
        help='Sleep `sleep\' seconds each step. Default is 0.0.',
        default=0.0, type=float)
oparse.add_option('--status', dest='status',
        help='Draw status when doing binary search',
        action="store_true")
oparse.add_option('--numpy', dest='numpy',
        help='Accelerate automaton operations using NumPy',
        action="store_true")
oparse.add_option('-b', '--binary-search', dest='binary',
        help='Binary search to determine critical density. '
        'Due to randomness, repeat for BINARY amount of times and take the '
        'average. Default is off.',
        type=int)
oparse.add_option('-z', '--binary-search-steps', dest='binary_steps',
        help='Binary search steps. Default is 5.',
        default=5, type=int)
oparse.add_option('-e', '--binary-allowed-error', dest='binary_error',
        help='Binary search allowed error in percentage. Default is 0.5.',
        default=0.5, type=float)
oparse.add_option('-n', '--plot-density', dest='plot_density',
        help='Plot density, use step DENSITY going from 0.0 to 1.0',
        default=0.0, type=float)
oparse.add_option('-o', '--density-times', dest='density_times',
        help='Times to perform simulation per density step. Default is 100.',
        default=100, type=int)
oparse.add_option('-v', '--vary-grid-size', dest='vary_grid_size',
        help='Vary grid size from s to e with step z.\
        Example s,e,z => 10,20,5',
        default='', type=str)
oparse.add_option('-O', '--output-graph', dest='output_graph',
        help='Path to store image in. Used only by plot-density.',
        default=None, type=str)

p = oparse.parse_args()[0]

GRID_SIZE = p.grid_size
MAX_STEPS = p.max_steps
DENSITY = p.density
PPC = p.ppc
if hasattr(p, 'binary'):
    BINARY = p.binary
else:
    BINARY = 0
BINARY_STEPS = p.binary_steps
BINARY_ERROR = p.binary_error
DENSITY_STEP = p.plot_density
DENSITY_TIMES = p.density_times
OUTPUT_FILE = p.output_graph
VGS, VGE, VGSTEP = [int(x) for x in p.vary_grid_size.split(',')] if p.vary_grid_size else (0,0,0)

if p.spread:
    # I'm so sorry.
    _c = p.spread.split(',')
    _l = int(__import__('math').sqrt(len(_c)))
    __ = [[] for x in xrange(_l)]
    ___ = 0
    for _ in xrange(_l ** 2):
        __[___].append(int(_c[_]))
        if (_+1) % _l == 0 and _ != 0:
            ___ += 1

    spread = __

DOPNG = 'png' in p.drawactions
DOTERM = 'term' in p.drawactions
DOMPL = 'mpl' in p.drawactions
DRAWSTATUS = p.status

class Cell(object):
    """
    Cell

    self._state = Current Cell state
    self._next_state = Next automaton state
    """

    def __init__(self, state):
        self._state = state
        self._next_state = 0
        pass

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self._state == FIRE:
            return '\033[1;31m♥\033[0m'
        elif self._state == VEGGIE:
            return '\033[1;32mx\033[0m'
        elif self._state == BARREN:
            return '\033[1;33mx\033[0m'
        else:
            return '\033[1;34m.\033[0m'

    def col(self):
        if self._state == FIRE:
            return (255, 0, 0)
        elif self._state == VEGGIE:
            return (0, 255, 0)
        elif self._state == BARREN:
            return (255, 255, 0)
        else:
            return (30, 30, 30)


    def set_state(self, state):
        self._next_state = state

    def on_fire(self):
        return self._state == FIRE

class ForestBase(object):
    """
    Forest base class.
    """

    def __init__(self):
        self.setup_grid()
        self.setup_fire()

        # Enable rendering of images?
        if DOPNG:
            self.setup_images()

    def setup_fire(self):
        for x in xrange(GRID_SIZE):
            self.ignite(0, x)

    def setup_grid(self):
        """
        This needs to be implemented. It generates a random
        forest based on a specific density setting.
        """

    def setup_images(self):
        self._im_count = 0
        self._i = Image.new('RGB', (GRID_SIZE * PPC, GRID_SIZE * PPC), 0)
        self._d = ImageDraw.Draw(self._i)

        if DOPNG:
            self.draw_im()

    def draw_im(self):
        for x in xrange(GRID_SIZE):
            for y in xrange(GRID_SIZE):
                cell = self.get_cell(x, y)
                self._d.rectangle((y * PPC, x * PPC, (y + 1) * PPC, (x + 1) * PPC),
                        fill=cell.col())

        s = 'im-%0' + str(len(str(100000))) + 'd.png'
        self._i.save(s % self._im_count)
        self._im_count += 1

    def draw_term(self):
        print '\033[0;0H'
        for x in xrange(GRID_SIZE):
            for y in xrange(GRID_SIZE):
                cell = self.get_cell(x, y)
                print cell,

            print ''

    def other_side_reached(self):
        for y in xrange(GRID_SIZE):
            g = self.get_cell(GRID_SIZE - 1, y)

            if g.on_fire() or g._state == BURNT:
                return True

        return False


class ForestFire(ForestBase):
    """
    Standard Forest fire automaton.
    """

    def __init__(self):
        self.fires = []
        self.fires_new = []

        # barren count, tree count
        self.bc = 0
        self.tc = 0

        # To be forest grid
        self.grid = []

        # Execute standard initialisation procedure
        super(type(self), self).__init__()

    def setup_grid(self):
        """
        Intialise random forest grid based on Cell objects.
        """
    
        # Compute cells, trees and barren lands
        cc = GRID_SIZE ** 2
        self.tc = int(cc * DENSITY)
        self.bc = cc - self.tc

        # Generate random grid
        grid = [Cell(VEGGIE) if i < self.tc else Cell(BARREN)
            for i in xrange(GRID_SIZE ** 2)]

        random.shuffle(grid)
        self.grid = [grid[i:i+GRID_SIZE] for i in xrange(0, GRID_SIZE ** 2, GRID_SIZE)]

    def ignite(self, y, x):
        """
        Ignite cell at position (y, x)
        """
        g = self.grid[y][x]

        if g._state == VEGGIE:
            self.tc -= 1
        else:
            self.bc -= 1

        g._state = FIRE
        self.fires.append((y, x))

    def get_cell(self, y, x):
        return self.grid[y][x]

    def step(self):
        for f in self.fires:
            x, y = f
            g = self.grid[x][y]

            for iee in xrange(len(spread)):
                for jee in xrange(len(spread[iee])):
                    if spread[iee][jee] == 0:
                        continue

                    xx = max(0, x+iee - int(len(spread)/2))
                    yy = max(0, y+jee - int(len(spread)/2))
                    xx = min(GRID_SIZE - 1, xx);
                    yy = min(GRID_SIZE - 1, yy);


                    if x == xx and y == yy:
                        continue

                    g_ = self.grid[xx][yy]
                    if g_._state == VEGGIE:
                        if g_._next_state != FIRE:
                            self.tc -= 1
                        g_.set_state(FIRE)
                        if (xx, yy) not in self.fires_new:
                            self.fires_new.append((xx, yy))

            g.set_state(BURNT)

        for x in xrange(GRID_SIZE):
            for y in xrange(GRID_SIZE):
                cell = self.grid[x][y]
                cell._state = cell._next_state if cell._next_state else cell._state

        # For incremental drawing store old fires
        self.fires_old = self.fires

        # Update current fire state
        self.fires = self.fires_new
        self.fires_new = []

        if not self.fires:
            #print 'No more fire'
            return False

        if p.sleep:
            __import__('time').sleep(p.sleep)
        return True

    def draw_inc(self):
        for f in self.fires_old:
            x, y = f
            self._d.rectangle((y * PPC, x * PPC, (y + 1) * PPC, (x + 1) * PPC),
                    fill=((30, 30, 30)))

        for f in self.fires:
            x, y = f
            self._d.rectangle((y * PPC, x * PPC, (y + 1) * PPC, (x + 1) * PPC),
                    fill=(255, 0, 0))

        s = 'im-%0' + str(len(str(100000))) + 'd.png'
        self._i.save(s % self._im_count)
        self._im_count += 1


if p.numpy:
    from numpy import array, zeros, ones, hstack, maximum, minimum, sum
    from numpy.random import shuffle
    from scipy.ndimage import correlate

    class ForestFireNumPy(ForestBase):
        """
        NumPy forest fire automaton.
        """

        def __init__(self):
            """
            Initialise NumPy forest fire simulation.
            """

            # Mirror and flip spread to make the convolution filter work
            self.spread = array(spread)[::-1,::-1]

            # Run base initialisation
            super(type(self), self).__init__()

            # Allocate burn and next_burn maps.
            self.burn_map = zeros(self.grid.shape)
            self.next_burn_map = zeros(self.grid.shape)

        def setup_grid(self):
            """
            Initialise random NumPy forest array.
            """

            # Compute number of trees and cells
            cells = GRID_SIZE ** 2
            trees = int(cells * DENSITY)

            # Generate random grid
            self.grid = hstack([ones(trees), zeros(cells - trees)])
            shuffle(self.grid)
            self.grid.shape = (GRID_SIZE, GRID_SIZE)

        def ignite(self, y, x):
            """
            Ignite grid position (y, x)
            """

            self.grid[y, x] = FIRE

        def step(self):
            """
            Perform single automaton step.
            """

            gsum = sum(self.grid)

            # Compute burn touched cells
            maximum(1, self.grid, self.burn_map)
            self.burn_map -= 1

            # Correlate cells for next set of fires
            correlate(self.burn_map, self.spread, mode='constant', cval=0,
                output=self.next_burn_map)

            # And cutoff at 1 and multiply by grid to remove
            # barren cells.
            self.next_burn_map *= self.grid
            minimum(1, self.next_burn_map, self.next_burn_map)

            # Finally ignite next set of trees and top at barren
            self.grid += self.next_burn_map
            self.grid += self.burn_map
            minimum(3, self.grid, self.grid)

            if p.sleep:
                __import__('time').sleep(p.sleep)

            # No more fire?
            return gsum < sum(self.grid)

        def get_cell(self, y, x):
            """
            Return Cell object at grid position (y, x).
            """

            # NumPy doesn't actually use this class, so
            # we wrap a value in the grid in a cell instance.

            the_cell = Cell(self.grid[y, x])
            the_cell._next_state = the_cell._state
            return the_cell

        def print_debug(a):
            """
            Print content of array structure in an orderly fashion.
            """
            height, width = a.shape
            for y in xrange(height):
                for x in xrange(width):
                    print int(a[y, x]),
                print

done = False

if BINARY > 0 and DENSITY_STEP != 0.0:
    print "Cannot use both density step and binary search."
    __import__('sys').exit(1)

if BINARY > 0:
    den_lo = 0
    den_hi = 1
    DENSITY = 0.5
    avg_burnt = 0
    bins = []


if DOMPL:
    from pylab import show, plot, xlim, ylim, xlabel, ylabel, title, legend, \
        savefig

if DENSITY_STEP != 0.0:
    DENSITY = 0.0
    avg_burnt = 0
    dens = []

if VGSTEP:
    GRID_SIZE = VGS

bin_count = 0
binary_steps = 0

while True:
    if DOTERM or DRAWSTATUS:
        __import__('os').system('clear')

    while True:
        ff = ForestFireNumPy() if p.numpy else ForestFire()

        try:
            if DOTERM:
                # Hide cursor
                print '\033[?25l'
                ff.draw_term()

            if DOPNG:
                ff.draw_im()

            step = 0

            while step < MAX_STEPS or MAX_STEPS == 0:
                if not ff.step():
                    break
                if DOTERM:
                    ff.draw_term()

                if DOPNG:
                    if p.numpy:
                        ff.draw_im()
                    else:
                        ff.draw_inc()

                step += 1


            if DOTERM:
                ff.draw_term()

            if DOPNG:
                # NumPy does not support incrememntal drawing.
                if p.numpy:
                    ff.draw_im()
                else:
                    ff.draw_inc()

        finally:
            if DOTERM:
                # Restore (show) cursor
                print '\033[?25h'

        if DRAWSTATUS and not DOTERM:
            print '\033[0;0H'

        if BINARY > 0:
            #print 'Try:', bin_count
            avg_burnt += 1 if ff.other_side_reached() else 0
            #print 'Density: %f, avg_burnt: %d' % (DENSITY, avg_burnt)
            bin_count += 1
            if bin_count < BINARY:
                continue

        if DENSITY_STEP != 0.0:
            avg_burnt += 1 if ff.other_side_reached() else 0

            bin_count += 1
            if bin_count < DENSITY_TIMES:
                continue

        break


    if BINARY > 0:
        if avg_burnt > BINARY * BINARY_ERROR:
            den_hi = DENSITY
        else:
            den_lo = DENSITY

        print 'Result', DENSITY, 'Grid size:', GRID_SIZE

        t = binary_steps
        s = DENSITY
        bins.append((t, s))

        DENSITY = (den_lo + den_hi) / 2.0
        bin_count = 0
        avg_burnt = 0

        if binary_steps > BINARY_STEPS:
            t = [x[0] for x in bins]
            s = [x[1] for x in bins]

            plot(t, s, 'r', linewidth=1.0, label='foo')

            if VGSTEP:
                DENSITY = 0.5
                den_hi = 1.0
                den_lo = 0.
                bins = []
                binary_steps = 0
                GRID_SIZE += VGSTEP
                if GRID_SIZE > VGE:
                    break
                continue
            else:
                break
        else:
            binary_steps += 1

        continue

    if DENSITY_STEP != 0.0:
#        print 'Density: %f. Percentage burnt: %f' % (DENSITY, \
#                float(avg_burnt) / DENSITY_TIMES)
        dens.append((DENSITY, float(avg_burnt) / DENSITY_TIMES))

        bin_count = 0
        avg_burnt = 0

        if DENSITY > 1.0:
            DENSITY += DENSITY_STEP
            s = [x[1] for x in dens]
            t = []
            for x in range(len(s)):
                t.append(x * DENSITY_STEP)

            if VGSTEP:
                x = hex(255 - (int((GRID_SIZE - VGS) / float(VGE) * 255)))
                x = x[2:] + '0' if len(x) < 4 else x[2:]
                foo = tuple([x] * 3)
                col = '#%s%s%s' % foo
            else:
                col = 'r'

            if DOMPL:
                #plot(t, s, linewidth=1.0, label='density for size: %d' % GRID_SIZE)
                plot(t, s, col, linewidth=1.0, label='density for size: %d' % GRID_SIZE)
            #plot(t, s, col, linewidth=1.0, label='percent reached for size: %d' % GRID_SIZE)

            dens = []

            if VGSTEP:
                DENSITY = 0.0
                GRID_SIZE += VGSTEP
                if GRID_SIZE > VGE:
                    break

                continue
        else:
            DENSITY += DENSITY_STEP
            continue

    break

if DOMPL:
    if DENSITY_STEP != 0.0:
        xlabel('density (%)')
        ylabel('reached the other side (%)')
        legend(loc='upper left')
        title('')
    elif BINARY > 0:
        xlim(0.0, 16)
        ylim(0.0, 1.0)
        xlabel('density (%)')
        ylabel('reached the other side (%)')
        title('')

    if OUTPUT_FILE:
        print 'Saving to', OUTPUT_FILE
        savefig(OUTPUT_FILE)
    else:
        show()
