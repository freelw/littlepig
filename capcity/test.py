#!/usr/bin/env python

from capacity import *

def builditem(x, y):
    return {'x':x, 'y':y}
if '__main__' == __name__:
    
    p1 = Point(builditem(0, 0))
    p2 = Point(builditem(1, 1))
    p = Point(builditem(0, 1))
    e = Edge(p1, p2)
    print e.dis(p)

    p1 = Point(builditem(0, 0))
    p2 = Point(builditem(1, 1))
    p = Point(builditem(-1, 0))
    e = Edge(p1, p2)
    print e.dis(p)

    p1 = Point(builditem(0, 0))
    p2 = Point(builditem(1, 1))
    p = Point(builditem(2, 2))
    e = Edge(p1, p2)
    print e.dis(p)
