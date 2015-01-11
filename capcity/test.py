#!/usr/bin/env python

from capacity import *

if '__main__' == __name__:
    p1 = Point(0, 0)
    p2 = Point(1, 1)
    e = Edge(p1, p2)
    print e.length()
