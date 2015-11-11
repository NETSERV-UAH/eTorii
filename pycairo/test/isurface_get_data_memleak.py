#!/usr/bin/env python
"""test cairo.ImageSurface.get_data() for a memory leak
"""

import resource

import cairo


pagesize = resource.getpagesize()

if not (cairo.HAS_IMAGE_SURFACE and cairo.HAS_PNG_FUNCTIONS):
  raise SystemExit ('cairo was not compiled with ImageSurface and PNG support')

width, height = 32, 32

c = 1
while True:
  for i in range(100000):
    surface = cairo.ImageSurface(cairo.FORMAT_ARGB32, width, height)
    ctx = cairo.Context(surface)

    buf1 = surface.get_data()
    buf2 = memoryview(surface)
    buf3 = bytes(surface)

  print(c, resource.getrusage(resource.RUSAGE_SELF).ru_maxrss * pagesize)
  c += 1
