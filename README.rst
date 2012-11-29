LEd Wall Daemon (lewd)
======================

Written in Python, supports the following features:
- Three interfaces: LedScreen (local access), RemoteLedScreen (networked /
  remote) and VirtualLedScreen, for local prototyping without the wall.
- Features a nice and simple API, the network protocol is also very simple.
- Some nice animations
- Tools to display images, with sub-pixel rendering
- Automatic gamma correction
- High FPS possible (>100fps)
- Some documentation is in place

TODO:
- Implement some kind of ``game api``.
- Possibly speed up the code a bit with numpy
- Wrote more documentation
- Write a frontend that makes it easy to set up the ledwall

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

