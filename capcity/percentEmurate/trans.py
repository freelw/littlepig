#!/usr/bin/env python

import json

def readfile(fname):
    content = ''
    for line in open(fname):
        content += line
    return content

def trans():
    conf = json.loads(readfile('../../conf.txt'))
    sector = conf['sector']
    xarr = [item['x'] for item in sector]
    yarr = [item['y'] for item in sector]
    print sector
    print xarr
    print yarr
    for i in xrange(9):
        name = 'clouds%s' % i
        for line in open(name):
            line = line.strip()
            x, y, r = line.split()
            print 'circle(%s, %s, %s, "%s");' % (x, y, r, name)

if '__main__' == __name__:
    trans()
