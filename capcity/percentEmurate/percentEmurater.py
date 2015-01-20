#!/usr/bin/env python

import json
import random
import math

class cloud:
    def __init__(self, x, y, R):
        self.x = x
        self.y = y
        self.R = R

    def isIn(self, x, y):
        return self.dis(x, y) <= self.R

    def dis(self, x, y):
        return math.sqrt((x-self.x)**2 + (y-self.y)**2)

def readfile(fname):
    content = ''
    for line in open(fname):
        content += line
    return content

def printclouds(clds, percent, cnt):
    fname = 'clouds%s' % cnt
    f = open(fname, 'w')
    f.write('%s\n' % percent)
    for cld in clds:
        msg = '%s %s %s' % (cld.x, cld.y, cld.R)
        f.write(msg + '\n')
    f.close()

def get():
    conf = json.loads(readfile('../../conf.txt'))
    sector = conf['sector']
    ret = []
    cnt = 0
    while True:
        while True:
            x = random.randint(-100, 100)
            y = random.randint(-100, 100)
            R = random.randint(10, 15)
            cld = cloud(x, y, R)
            if isInSector(cld, sector):
                break
        ret.append(cld)
        area_percent = getAreaPercent(sector, ret)
        if area_percent > 85:
            return
        print area_percent
        printclouds(ret, area_percent, cnt)
        cnt += 1

def getAreaPercent(sector, clds):
    N = 10000
    cnt = 0
    cnt1 = 0
    def getrand():
        return 1.*random.randint(-10000, 10000)/100
    while cnt < N:
        x = getrand()
        y = getrand()
        if isInSector(cloud(x, y, 0), sector):
            cnt += 1
            for cld in clds:
                if cld.isIn(x, y):
                    cnt1 += 1
                    break
    return 1.*cnt1/cnt*100
def getAreaPercent(sector, clds):
    N = 10000
    cnt = 0
    cnt1 = 0
    def getrand():
        return 1.*random.randint(-10000, 10000)/100
    while cnt < N:
        x = getrand()
        y = getrand()
        if isInSector(cloud(x, y, 0), sector):
            cnt += 1
            for cld in clds:
                if cld.isIn(x, y):
                    cnt1 += 1
                    break
    return 1.*cnt1/cnt*100

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

if '__main__' == __name__:
    get()
