import sys,os
sys.path.insert(0, os.path.dirname(__file__))

__all__ = [ "fire", "gameoflife", "spaceinvader", "scrollimage", "munch", "wobbleinvader", "wobble" ]

animations = []

for mod in __all__:
    globals()[mod] = __import__(mod)
    if hasattr(globals()[mod], 'animations'):
        animations += globals()[mod].animations

