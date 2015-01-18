#!/usr/bin/env python

import json
import clouds
import math

def readfile(fname):
    content = ''
    for line in open(fname):
        content += line
    return content

def builditem(x, y):
    return {'x':x, 'y':y}

class Point:
    def __init__(self, item):
        self.x = item['x']
        self.y = item['y']
    def dis(self, p):
        return math.sqrt((self.x-p.x)**2+(self.y-p.y)**2)

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
        item = builditem(cld.x, cld.y)
        p = Point(item)
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

def printways(ways):
    N = len(ways)-1
    print '--------------ways---------------'
    for i in xrange(N+1):
        for j in xrange(N+1):
            print '%s %s %s' % (i, j, ways[i][j])
    print '/-------------ways--------------/'

def floyed(ways):
    N = len(ways)-1
    for k in xrange(N+1):
        for i in xrange(N+1):
            for j in xrange(N+1):
                if i != j and ways[i][j] > ways[i][k] + ways[k][j]:
                    ways[i][j] = ways[i][k] + ways[k][j]

def printclouds(clds):
    print '-------------clouds-------------'
    for index, cld in enumerate(clds):
        print 'index : %s x : %s y %s R : %s' % (index, cld.x, cld.y, cld.R)
    print '/------------clouds------------/'

if '__main__' == __name__:
    conf = json.loads(readfile('../conf.txt'))
    sector = conf['sector']

    top = [[1,2], [2,3]]
    bottom = [[6,5], [5,4]]

    topE = buildE(top, sector)
    bottomE = buildE(bottom, sector)

    per_range = [(0, 10), (10, 20)]
    vr_range = [(0, 100)]
    
    def writeout(msg):
        fout = open('capacity3ddata.txt', 'wa')
        fout.write(msg+'\n')
        fout.close()
        
    retrytimes = 10
    for i in xrange(retrytimes):
        for peri in per_range:
            for vri in vr_range:
                #clds, area_percent, vr = clouds.get(0, 10, 0, 10)
                clds, area_percent, vr = clouds.get(peri[0], peri[1] , vri[0], vri[1])
                N = len(clds)+1
                ways = [[1e10 for i in xrange(N+1)] for j in xrange(N+1)]
                for index, cld in enumerate(clds):
                    tpd = topE.dis(cld) - cld.R
                    btd = bottomE.dis(cld) - cld.R
                    ways[0][index+1] = tpd
                    ways[index+1][0] = tpd
                    ways[N][index+1] = btd
                    ways[index+1][N] = btd
                for i, cldi in enumerate(clds):
                    for j, cldj in enumerate(clds):
                        if i != j:
                            pi = Point(builditem(cldi.x, cldi.y))
                            pj = Point(builditem(cldj.x, cldj.y))
                            dis = max(pi.dis(pj), 0)
                            ways[i+1][j+1] = dis
                            ways[j+1][i+1] = dis
                #printways(ways)
                floyed(ways)
                #printways(ways)
                printclouds(clds)
                msg = 'capacity : %s, coverage : %s, variance : %s' % (ways[0][N], area_percent, vr)
                print msg
                writeout(msg + '\n')
