LEd Wall Daemon (lewd)
======================

Initially written in Python, may port to go soon.
(API will not change, obviously)

TODO:
    - Мировое господство
    - Code:
        - Layer for even nicer led access?
        - Add higher-level APIs

    - Create multiplayer concept where frames are merged / managed.

    - TUI when serial/led communication is not available for testing.
      (Note to self: MINOS)

Experimental:
    - Documentation: done using sphinx: http://sphinx.pocoo.org
    - Tweak low-level networking code transform


Future ideas:
    - Music visualisation on the LEDs.
    - Middleware for more *noob friendly* API. (Pushing XML, JSON, etc)
    - Networking (WebSockets, etc)

Future future:
    - Maemo 5 application?
    - Web interface for switching animations (probably using websockets to
      communicate to middleware)
    - Web interface to actually control leds as well (websockets, perhaps
      something nice interactive can be done using canvas as well)

