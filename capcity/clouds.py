#!/usr/bin/env python

import json
import random

class cloud:
    def __init__(self, x, y, R):
        self.x = x
        self.y = y
        self.R = R

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

def get(min_variance, max_variance):
    conf = json.loads(readfile('../conf.txt'))
    sector = conf['sector']
    rtop = 80.
    while True:
        ret = []
        for i in xrange(10):
            while True:
                x = random.randint(-100, 100)
                y = random.randint(-100, 100)
                R = random.randint(0, rtop)
                cld = cloud(x, y, R)
                #print 'building cloud %s' % i
                if isInSector(cld, sector):
                    break
            ret.append(cld)
        vr = variance([item.R for item in ret])
        if min_variance <= vr <= max_variance:
            print 'variance %s ok.' % vr
            break
        else:
            if vr > max_variance:
                print 'variance %s is bigger then %s rtop=%s, retry.' % (vr, max_variance, rtop)
                rtop /= 2
            elif vr < min_variance:
                rtop *= 2
                print 'variance %s is smaller then %s rtop=%s, retry.' % (vr, min_variance, rtop)
                
            
    return ret

def variance(arr):
    s = reduce(lambda x, y : x+y, arr)
    ave = s*1./len(arr)
    arr1 = map(lambda x : (x-ave)**2, arr)
    s = reduce(lambda x, y : x+y, arr1)
    return s*1./len(arr1)
    
if '__main__' == __name__:
    arr = [1, 2, 3]
    print variance(arr)
