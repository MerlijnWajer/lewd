import sys,os
sys.path.insert(0, os.path.dirname(__file__))

__all__ = [ "fire", "scrollimage", "gameoflife", "spaceinvader", "munch", "wobbleinvader", "wobble", "lsdwall", "lsdwall2", "plasma" ]

animations = []

for mod in __all__:
    globals()[mod] = __import__(mod)
    if hasattr(globals()[mod], 'animations'):
        animations += globals()[mod].animations

