Arduino Code
============

This section covers the simple firmware for the arduino to control the leds.

Protocol
--------

Protocol is simple. Write bytes to the serial /dev/ttyACM0 file.
Each led is three bytes. Format is *Green* *Red* *Blue* (in that order).

To jump back to the start, write the byte 254. (This is not a problem since the
gamma correction will never return 254 for any colour component.

Code
----

.. literalinclude:: ../../src/firmware/ledwall.ino
    :language: c++
