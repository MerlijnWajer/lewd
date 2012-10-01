import Image, os

imgfile = './imgs/test2.png'
#imgfile = './imgs/techinc-ad1.png'
#imgfile = './imgs/techinc-ad2.png'

def normalise(colour):
    r,g,b = colour
    return [r/255.,g/255.,b/255.]

class ScrollImage(object):

    def __init__(self, w, h):
        self.w, self.h = w, h
        self.i = 0
        image = Image.open(os.path.dirname(__file__)+'/'+imgfile)
        image = image.convert(mode='RGB')
        self.img_width, _ = image.size
        image = image.crop( (0, 0, self.img_width, h) )
        self.data = image.getdata()

    def next(self):

        frame = [ [ self.data[self.i+x+y*self.img_width] for x in xrange(self.w) ]
                                                         for y in xrange(self.h) ]
        self.i+=1
        self.i %= self.img_width-self.w

        return frame

animations = [ ScrollImage ]

