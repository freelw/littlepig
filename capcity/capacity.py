#!/usr/bin/env python

import json
import clouds
import math

def readfile(fname):
    content = ''
    for line in open(fname):
        content += line
    return content

class Point:
    def __init__(self, item):
        self.x = item['x']
        self.y = item['y']
    def dis(self, p):
        return Math.sqrt((self.x-p.x)**2+(self.y-p.y)**2)

class vec:
    def __init__(self):
        pass
    def setpoint(self, p1, p2):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y
        return self
    def setxy(self, x, y):
        self.x = x
        self.y = y
        return self
    def cross(self, v):
        return self.x*v.x + self.y*v.y;
    def mutNum(self, n):
        return vec().setxy(n*self.x, n*self.y)
    def length(self):
        return math.sqrt(self.x**2+self.y**2)
    def minus(self, v):
        return vec().setxy(self.x-v.x, self.y-v.y)
        
class Edge:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def dis(self, p):
        p1p = vec().setpoint(self.p1, p)
        p1p2 = vec().setpoint(self.p1, self.p2)
        absp1p2 = p1p2.length()
        r = p1p.cross(p1p2)/(absp1p2**2)
        if r < 0:
            return p1p.length()
        elif r < 1:
            p1c = p1p2.mutNum(r)
            pc  = p1c.minus(p1p)
            return pc.length()
        else:
            p2p = vec().setpoint(self.p2, self.p1)
            return p2p.length()

class Edges:
    def __init__(self):
        self.edges = []

    def append(self, e):
        self.edges.append(e)

    def dis(self, cld):
        ret = 1e10
        p = Point(cld.x, cld.y)
        for e in self.edges:
            dis = e.dis(p) 
            if ret > dis:
                ret = dis
        return ret
        
def buildE(arr, sector):
    ret = Edges()
    for item in arr:
        p1 = Point(sector[item[0]-1])
        p2 = Point(sector[item[1]-1])
        e = Edge(p1, p2)
        ret.append(e)
    return ret

if '__main__' == __name__:
    conf = json.loads(readfile('../conf.txt'))
    sector = conf['sector']
    print sector

    top = [[1,2], [2,3]]
    bottom = [[6,5], [5,4]]

    topE = buildE(top, sector)
    bottomE = buildE(bottom, sector)

#    clds = clouds.get()
    
