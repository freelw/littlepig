
if '__main__' == __name__:
    xd = {}
    yd = {}
    for line in open('batOutput.txt'):
        x, y, z = line.split()
        xd[x] = True
        yd[y] = True
    xarr = [int(item) for item in xd.keys()]
    yarr = [int(item) for item in yd.keys()]
    xarr.sort()
    yarr.sort()
    xarr = [str(item) for item in xarr]
    yarr = [str(item) for item in yarr]
    cnt = 0
    cntdx = {}
    for item in xarr:
        cnt += 1
        cntdx[item] = cnt
    cnt = 0
    cntdy = {}
    for item in yarr:
        cnt += 1
        cntdy[item] = cnt
    
    msg = 'function drawplane\n'
    draw = open('drawplane.m', 'w')
    msg += '\tx = [%s]\n' % ', '.join(xarr)
    msg += '\ty = [%s]\n' % ', '.join(yarr)
    msg += '\tz = zeros(%s, %s)\n' % (len(xarr), len(yarr))
    for line in open('batOutput.txt'):
        x, y, z = line.split()
        msg += '\tz(%s, %s) = %s\n' % (cntdx[x], cntdy[y], z)
    msg += '\tmesh(x, y, z)\n'

    msg +='end'
    draw.write(msg)
    draw.close()
    
    