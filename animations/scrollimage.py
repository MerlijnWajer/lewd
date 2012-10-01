import Image, os

imgdir = os.path.dirname(__file__)+'/imgs/'
imgfiles = [ imgdir + name for name in os.listdir(imgdir) if name.endswith('.png') ]

def normalise(colour):
    r,g,b = colour
    return [r/255.,g/255.,b/255.]

def scrollimage_class(imgfile):

    class ScrollImage(object):

        def __init__(self, w, h):
            self.w, self.h = w, h
            self.i = 0
            image = Image.open(os.path.dirname(__file__)+'/'+imgfile)
            image = image.convert(mode='RGB')
            self.img_width, _ = image.size
            image = image.crop( (0, 0, self.img_width, h) )
            self.data = image.getdata()
            self.b = False

        def next(self):
            frame = [ [ self.data[self.i+x+y*self.img_width] for x in xrange(self.w) ]
                                                             for y in xrange(self.h) ]

            self.b = not self.b

            if self.b:
                self.i+=1
                if self.img_width-self.w > 0:
                    self.i %= self.img_width-self.w
                else:
                    self.i = 0

            return frame

    return ScrollImage

animations = [ scrollimage_class(name) for name in imgfiles ]

