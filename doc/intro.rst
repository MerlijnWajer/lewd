Introduction to LEWD
====================

LEd Wall Deamon (LEWD) is software written in Python for the RGB LED wall at the
Technologia Incognita Hackerspace located in Amsterdam.

Currently, the RGB LED Wall supports both local and remote access (over tcp
sockets) and can run at a maxiumum of approximately 150 frames per second.
Gamma correction is applied to all the frames and there exists some code to
allow for subpixel rendering.

The project is divided into several parts:

    * The :ref:`low` level code.
    * :ref:`Examples`!
    * The simple :ref:`net` and :ref:`sync` code.
    * Higher level APIs. (Which are yet to be written)
