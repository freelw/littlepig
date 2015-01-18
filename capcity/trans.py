
if '__main__' == __name__:
    xarr = []
    yarr = []
    for line in open('capacity3ddata.txt'):
        z, x, y = line.split()
        print x, ' ', y
        xarr.append(float(x))
        yarr.append(float(y))
    xarr.sort()
    yarr.sort()
    xarr = [str(item) for item in xarr]
    yarr = [str(item) for item in yarr]
    print len(xarr), ' ', len(yarr)
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
    draw = open('drawcapacity.m', 'w')
    msg += '\tfigure(1)\n'
    msg += '\tx = [%s]\n' % ', '.join(xarr)
    msg += '\ty = [%s]\n' % ', '.join(yarr)
    msg += '\tz = zeros(%s, %s)\n' % (len(xarr), len(yarr))
    for line in open('capacity3ddata.txt'):
        z, x, y = line.split()
        msg += '\tz(%s, %s) = %s\n' % (cntdx[x], cntdy[y], z)
    msg += '\t[xi, yi] = meshgrid(0:0.3:100, 0:0.3:100)\n'
    msg += "\tzi = griddata(x, y, z, xi, yi, 'linear')\n"
    
    msg += '\tmesh(xi, yi, zi)\n'
    msg += '\tfigure(2)\n'
    msg += '\t[C,h] = contour(xi, yi, zi)\n'
    msg += '\tclabel(C,h)\n'
    msg +='end'
    draw.write(msg)
    draw.close()
    
    
