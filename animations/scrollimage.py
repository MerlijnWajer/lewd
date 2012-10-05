import Image, os

LEFT, RIGHT = -1, 1

imgfiles = [
    ("imgs/nyancat.png"              , LEFT  , 3),
    ("imgs/technologiaincognita.png" , RIGHT , 3),
    ("imgs/techinc-ad2.png"          , RIGHT , 3),
    ("imgs/techinc.png"              , RIGHT , 3),
#    ("imgs/test3.png"                , RIGHT , 3),
]

def normalise(colour):
    r,g,b = colour
    return [r/255.,g/255.,b/255.]

def scrollimage_class(filename, scrolldir, subpix):

    class ScrollImage(object):

        def __init__(self, w, h):
            self.w, self.h = w, h
            self.i = 0
            image = Image.open(os.path.dirname(__file__)+'/'+filename)
            image = image.convert(mode='RGB')
            iw, ih = image.size
            iw, ih = int(subpix*iw*h/float(ih)), h
            image = image.resize( (iw, ih), Image.ANTIALIAS )
            self.data = image.getdata()
            self.iw, self.ih = iw, ih

        def next(self):
            frame = [ [ self.data[(self.i+x*subpix)%self.iw + y*self.iw]
                        for x in xrange(self.w) ]
                        for y in xrange(self.h) ]

            self.i+=scrolldir
            self.i %= self.iw

            return frame

    return ScrollImage

animations = [ scrollimage_class(name, scrolldir, subpix) for name, scrolldir, subpix in imgfiles ]

