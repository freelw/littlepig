#!/usr/bin/env python

import json
import random

class cloud:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.R = 5

def readfile(fname):
    content = ''
    for line in open(fname):
        content += line
    return content

def isInSector(item, sector):
    def vcp(x0, y0, x1, y1):
        return x0*y1 - x1*y0
    x = item.x
    y = item.y
    def getSum(x, y, sector, bAbs=False):
        sum = 0
        for i in xrange(len(sector)-1):
            x0 = sector[i]['x'] - x
            y0 = sector[i]['y'] - y
            x1 = sector[i+1]['x'] - x
            y1 = sector[i+1]['y'] - y 
            tmp = vcp(x0, y0, x1, y1)
            if bAbs:
                tmp = abs(tmp)
            sum += tmp
        x0 = sector[len(sector)-1]['x'] - x
        y0 = sector[len(sector)-1]['y'] - y
        x1 = sector[0]['x'] - x
        y1 = sector[0]['y'] - y
        tmp = vcp(x0, y0, x1, y1)
        if bAbs:
            tmp = abs(tmp)
        sum += tmp
        return sum
    sum0 = getSum(x, y, sector)
    sum1 = getSum(x, y, sector, True)
    return abs(abs(sum0) - abs(sum1)) < 1e-7

def get():
    conf = json.loads(readfile('../conf.txt'))
    sector = conf['sector']
    ret = []
    for i in xrange(10):
        while True:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            cld = cloud(x, y)
            print 'building cloud %s' % i
            if isInSector(cld, sector):
                break
            ret.append(cld)
    return ret
