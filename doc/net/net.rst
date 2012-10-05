LED control over Network
========================

There (are|will be) several ways of controlling the LED screen.
This section (should|will) cover all of these methods.

Using a bytestream
------------------

See :ref:`ledremote` for the Python module that implements a :ref:`led` like
LedScreen class.

The protocol is trivial:

    * Open a connection

    * Repeat:
        -   Write width * height * 3 bytes, rgb order. (R, G, B values range from
            0 to 255)
            Pixels start (0, 0), which is the top-right corner of the led
            wall (and this the top-left corner when you are outside).

            Send like this:

            .. code-block:: python

                for y in range(0, h):
                    for x in range(0, w):
                        socket.write(pixels[x, y])



That's it. Right now the server doesn't drop the buffer when you're sending more
bytes than the arduino can handle, so don't do that. (Max should be 25fps)


Multiple instances sending frames
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Right now, if several clients are sending data to the server; it will simply
pass each frame (of each client) to the arduino. Which means the arduino will
simply not be able to manage to pipe all the data to the led wall. As stated
before, the server will eventually start dropping extraneous amounts of data
when required.

However, when you're writing a multiplayer game and have several clients
running, it is good practice to merge the frames (or have just one instance
actually draw the screen, etc) before pushing them to the low level api.
