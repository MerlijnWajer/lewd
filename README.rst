LEd Wall Daemon (lewd)
======================

Initially written in Python, may port to go soon.
(API will not change, obviously)

TODO:
    - Мировое господство
    - Code:
        - Make it run standalone (that is, without requiring the nodejs to
        - set up some initial stuff)
        - Add (optional!) buffering to just send an entire frame at once,
        - seeing led frames are mostly accessed using __setitem__
        - Add __iter__ support
        - Add (low-level!) networking support
        - Layer for even nicer led access?

    - Document API(s)
    - TUI when serial/led communication is not available for testing.
      (Note to self: MINOS)


Future ideas:
    - Music visualisation on the LEDs.
    - Middleware for more *noob friendly* API. (Pushing XML, JSON, etc)
    - Networking (WebSockets, etc)
    - Authentication API? (Including logging)
    - Think about nice ways to make writing animations easy (brainsmoke did
      something nice in python, probably port his code)

Future future:
    - Maemo 5 application?
    - Web interface for switching animations (probably using websockets to
      communicate to middleware)
    - Web interface to actually control leds as well (websockets, perhaps
      something nice interactive can be done using canvas as well)

