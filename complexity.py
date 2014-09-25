import dataLoader
import flightstream
import json
import math
import copy
import os
import sys

class point:
    def __init__(x, y):
        self.x = x
        self.y = y

class route:
    def __init__(begin, end):
        self.begin = begin
        self.end = end

def write_func(func, arr):
    fx = open(func+'.m', 'w')
    content = 'function ret='+func+'\n'
    content += '\tret=['
    for item in arr:
        content += str(item) + ','
    content = content[:-1] + ']\n'
    content += 'end\n'
    fx.write(content)
    fx.close()

def init_m(sector_info):
    def init_sector(info):
        x = []
        y = []
        for item in info:
            x.append(item['x'])
            y.append(item['y'])
        write_func('getsectorx', x)
        write_func('getsectory', y)
    def init_lines(info):
        begin = info['begin']
        end = info['end']
        write_func('getroutebegin', begin)
        write_func('getrouteend', end)
    def init_cloud(info):
        arr = [info['cloudx'], info['cloudy'], info['cloudR'], info['speedx'], info['speedy']]
        write_func('getcloudinfo', arr)
    def init_circle(info):
        arr = [info['circlex'], info['circley'], info['circleR']]
        write_func('getcircleinfo', arr)
        
    init_sector(sector_info['sector'])
    init_lines(sector_info['lines'])
    #init_cloud(sector_info['cloud'])
    init_circle(sector_info['circle'])
    
def drawMap(sector_info):
    print 'complexity.py begin...'
    if sector_info is None:
        pass
    else:
        init_m(sector_info)

def drawFlightsInfo(sector_info, varr):

    def getCache():
        try:
            fc = open('flightinfocache')
            ret = ''
            for line in fc:
                ret += line
            fc.close()
            
            fflightsinfo = open('flightsinfo')
            flightsinfo = ''
            for line in fflightsinfo:
                flightsinfo += line
                
            flightsinfo = json.loads(flightsinfo)
            fflightsinfo.close()
            
            return ret, flightsinfo
        except:
            return None, None
    def saveCache(s,  flightsinfo):
        fc = open('flightinfocache', 'w')
        fc.write(s)
        fc.close()
        
        fflightsinfo = open('flightsinfo', 'w')
        fflightsinfo.write(json.dumps(flightsinfo))
        fflightsinfo.close()
    def getDrawCmd(varr):
        ret, flightsinfo = getCache()
        if ret is not None:
            return ret, flightsinfo
        ret = ''
        linenum = len(sector_info['lines']['begin'])
        colors = ['b', 'm', 'c', 'r', 'g', 'y', 'w', 'k']
        colornum = len(colors)
        flightsinfo = []
        print varr
        for i in xrange(linenum):
            arr = flightstream.buildstream(varr[i])
            flightsinfo.append(arr)
            x = [str(item['time']) for item in arr]
            y = [str(item['v']) for item in arr]
            print x
            xs = '\tx = [' + ', '.join(x) + ']\n'
            ys = '\ty = [' + ', '.join(y) + ']\n'
            ret += xs
            ret += ys
            colorstr = "'%s'" % colors[i%colornum]
            ret += "\tplot(x, y, %s)\n" % colorstr
        saveCache(ret, flightsinfo)
        return ret, flightsinfo
            
    funcname = 'showlinestinfo'
    content = 'function %s\n' % funcname
    drawCmd, flightsinfo = getDrawCmd(varr)
    content += drawCmd
    content += 'end\n'
    
    f = open(funcname+'.m', 'w')
    f.write(content)
    f.close()   
    return flightsinfo
    
class plane:
    def __init__(self, x, y, vx, vy, type = None, line = None, index = None, time = None):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.type = type
        self.line = line
        self.index = index
        self.time = time

def getlineunitv(cnt, sector_info):
    begin = sector_info['lines']['begin'][cnt] - 1
    end = sector_info['lines']['end'][cnt] - 1
    pbegin = sector_info['sector'][begin]
    pend = sector_info['sector'][end]
    vx = pend['x'] - pbegin['x']
    vy = pend['y'] - pbegin['y']
    len = math.sqrt(vx**2 + vy**2)
    return fdiv(vx, len), fdiv(vy, len)

def getbeginpoint(cnt, sector_info):
    begin = sector_info['lines']['begin'][cnt] - 1
    pbegin = sector_info['sector'][begin]
    return pbegin['x'], pbegin['y']

def scanComing(i, sector_info, flightsinfo, pool):
    whichline = 0
    for arr in flightsinfo:
        uvx, uvy = getlineunitv(whichline, sector_info)
        x, y = getbeginpoint(whichline, sector_info)
        if len(arr) > 0:
            item = arr[0]
            if item['time'] <= i:
                type = item['type']
                index = item['index']
                time = item['time']
                v = item['v']
                vx = v*uvx
                vy = v*uvy
                newplane = plane(x, y, vx, vy, type, whichline, index, time)
                pool.append(newplane)
                print 'coming'
                arr.pop(0)
        whichline += 1

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

def scanLeaving(sector_info, pool, leaveTime):
    ret = []
    retleave = []
    sector = sector_info['sector']
    for item in pool:
        if isInSector(item, sector):
            ret.append(item)
        else:
            item.leaveTime = leaveTime
            retleave.append(item)
            
    if len(pool) != len(ret):
        print 'leave!'
    return ret, retleave
    
def move(pool):
    for item in pool:
        item.x += item.vx *1./ 3600
        item.y += item.vy *1./ 3600
def feql(a, b):
    return abs(a-b) < 1e-10

def fdiv(a, b):
    if feql(b, 0):
        b = 1e-10
    return a * 1. / b

def simulate(flightsinfo, sector_info):
    print flightsinfo
    print sector_info
    fr = sector_info['flightstream']['time']['f']
    to = sector_info['flightstream']['time']['simulate_end_time']
    
    pool = []
    
    def dis(pl1, pl2):
        return math.sqrt((pl1.x - pl2.x)**2 + (pl1.y - pl2.y)**2)
    def towards(p1, p2):
        pl1 = copy.deepcopy(p1)
        pl2 = copy.deepcopy(p2)
        dis1 = dis(pl1, pl2)
        tpool = [pl1, pl2]
        move(tpool)
        dis2 = dis(pl1, pl2)
        return dis2 < dis1
    def conflict(pl1, pl2, separation):
        vrx = pl2.vx - pl1.vx
        vry = pl2.vy - pl1.vy
        tmp = fdiv(vry, vrx)
        thit = math.atan(tmp)
        if thit < 0:
            thit += math.pi
                
        line12x = pl2.x - pl1.x
        line12y = pl2.y - pl1.y
        tmp = fdiv(line12y, line12x)
        gama = math.atan(tmp)
        if gama < 0:
            gama += math.pi

        dis12 =  dis(pl1, pl2)
        tmp = fdiv(separation, dis12)
           
        def asin(tmp):
            if tmp > 1:
                tmp = 1
            elif tmp < -1:
                tmp = -1
            return math.asin(tmp)
            #confirm abs(tmp) <= 1
        tmp = asin(tmp)
        alpha = gama + tmp
        beta = gama - tmp
        return beta < thit < alpha, thit, alpha, beta
        
    def changev(pl2, pl1, beta, thit):
        D = fdiv(pl2.vy, pl2.vx)
        vx = fdiv((pl1.vy - math.tan(beta)*pl1.vx), (D - math.tan(beta)))
        vy = D*vx
        return vx, vy

    def can_not_changev(vx, vy, pl, sector_info):
        type = pl.type
        vf = sector_info['flightstream']['flighttypes'][type]['vf']
        vt = sector_info['flightstream']['flighttypes'][type]['vt']
        v = math.sqrt(vx**2 + vy**2)
        return v < vf or v > vt

    def cost(vx, vy, pl, sector_info):
        #if can_not_changev(vx, vy, pl, sector_info):
        #    return 1e11
        v = math.sqrt(vx**2 + vy**2)
        curv = math.sqrt(pl.vx**2 + pl.vy**2)
        return curv - v
        
    def samdir(pl1, pl2):
        def unit_v(x, y):
            sz = math.sqrt(x**2+y**2)
            return fdiv(x, sz), fdiv(y, sz)
        u1x, u1y = unit_v(pl1.vx, pl1.vy)
        u2x, u2y = unit_v(pl2.vx, pl2.vy)
        return feql(u1x, u2x) and feql(u1y, u2y)
    
    def cantSolveConflict(time_point, plj, plk = None):
        f = open('cantSolveConflict.txt', 'a')
        if plk is None:
            msg = 'at %s plane %s_%s can\'t avoid cloud' % (time_point, plj.line, plj.index)
        else:
            msg = 'at %s plane %s_%s can\'t avoid plane %s_%s' % (time_point, plj.line, plj.index, plk.line, plk.index)
        f.write(msg+'\n')
        f.close()
    
    
    global flightnumarr
    global leaveinfo
    def jkisConflict(plj, plk, conflictTime, value, samedir = "can't change"):
        def jisConflict(plj, conflictTime):
            global conflictMap
            index = '%s_%s' % (plj.line, plj.index)
            for item in conflictMap:
                if item['index'] == index:
                    item['arr'][conflictTime] = 1
                    #print 'plane : %s is conflict at %s' %(index, conflictTime)
                    break
            else:
                print 'jisConflict warning index : %s %s' % index
        jisConflict(plj, conflictTime)
        jisConflict(plk, conflictTime)
        conflictmsg = open('conflictmsg.txt', 'a')
        msg = '%s_%s %s_%s conflict at %s %s_%s change %s samedir %s\n' % (plj.line, plj.index, plk.line, plk.index, conflictTime, plj.line, plj.index, value, samedir)
        conflictmsg.write(msg)
        conflictmsg.close()
        
    cldconf = sector_info['cloud']
    cloud = plane(cldconf['cloudx'], cldconf['cloudy'], cldconf['speedx'], cldconf['speedy'])
    for i in xrange(fr, to):
        flightnumarr.append({'t':i, 'num':len(pool)})
        scanComing(i, sector_info, flightsinfo, pool)
        pool, leave = scanLeaving(sector_info, pool, i)
        leaveinfo.append(leave)
        cost_sum = 0
        def getminind(c):
            ind = 0
            cnt = 0
            for item in c:
                if item < c[ind]:
                    ind = cnt
                cnt += 1
            return ind
        #for cloud
        for j in xrange(len(pool)):
            if dis(pool[j], cloud) <= cldconf['cloudR']*6:
                if towards(pool[j], cloud):
                    bconflict, thit, alpha, beta = conflict(pool[j], cloud, cldconf['cloudR'])
                    if bconflict:
                        vjx1, vjy1 = changev(pool[j], cloud, alpha, thit)
                        vjx2, vjy2 = changev(pool[j], cloud, beta, thit)
                        cost_inputs = [
                            [vjx1, vjy1, pool[j], sector_info],
                            [vjx2, vjy2, pool[j], sector_info]
                        ]
                        c = []
                        for item in cost_inputs:
                            c.append(abs(cost(item[0], item[1], item[2], item[3])))
                        ind = getminind(c)
                        item = cost_inputs[ind]
                        cost_sum += abs(cost(item[0], item[1], item[2], item[3]))
                        if not can_not_changev(item[0], item[1], item[2], item[3]):
                            if 0 == ind or 1 == ind:
                                pool[j].vx = item[0]
                                pool[j].vy = item[1]
                        else:
                            cantSolveConflict(i, pool[j])
        #for cloud end
        
        
        for j in xrange(len(pool)):
            for k in xrange(len(pool)):
                if k > j:
                    if dis(pool[j], pool[k]) <= 6*sector_info['flightstream']['separation']:
                        if towards(pool[j], pool[k]):
                            
                            if samdir(pool[j], pool[k]):
                                c = []
                                cost_inputs = [[pool[j].vx, pool[j].vy, pool[k], sector_info],
                                    [pool[k].vx, pool[k].vy, pool[j], sector_info]
                                ]
                                for item in cost_inputs:
                                    c.append(abs(cost(item[0], item[1], item[2], item[3])))
                                ind = getminind(c)
                                item = cost_inputs[ind]
                                value = cost(item[0], item[1], item[2], item[3])
                                cost_sum += abs(value)
                                if not can_not_changev(item[0], item[1], item[2], item[3]):
                                    if 0 == ind:
                                        pool[k].vx = item[0]
                                        pool[k].vy = item[1]
                                        jkisConflict(pool[k], pool[j], i, value, 'samedir')
                                    elif 1 == ind:
                                        pool[j].vx = item[0]
                                        pool[j].vy = item[1]
                                        jkisConflict(pool[j], pool[k], i, value, 'samedir')
                                else:
                                    jkisConflict(pool[j], pool[k], i, None)
                                    cantSolveConflict(i, pool[j], pool[k])
                            else:
                                bconflict, thit, alpha, beta = conflict(pool[j], pool[k], sector_info['flightstream']['separation'])
                                if bconflict: 
                                    
                                    vjx1, vjy1 = changev(pool[j], pool[k], alpha, thit)
                                    vjx2, vjy2 = changev(pool[j], pool[k], beta, thit)
                                    bconflict, thit, alpha, beta = conflict(pool[k], pool[j], sector_info['flightstream']['separation'])
                                    vkx1, vky1 = changev(pool[k], pool[j], alpha, thit)
                                    vkx2, vky2 = changev(pool[k], pool[j], beta, thit)
                                    c = []
                                    cost_inputs = [[vjx1, vjy1, pool[j], sector_info],
                                        [vjx2, vjy2, pool[j], sector_info],
                                        [vkx1, vky1, pool[k], sector_info],
                                        [vkx2, vky2, pool[k], sector_info]
                                    ]
                                    for item in cost_inputs:
                                        c.append(abs(cost(item[0], item[1], item[2], item[3])))
                                    ind = getminind(c)
                                    item = cost_inputs[ind]
                                    
                                    value = cost(item[0], item[1], item[2], item[3])
                                    cost_sum += abs(value)
                                    if not can_not_changev(item[0], item[1], item[2], item[3]):
                                        if 0 == ind or 1 == ind:
                                            pool[j].vx = item[0]
                                            pool[j].vy = item[1]
                                            jkisConflict(pool[j], pool[k], i, value, 'diffdir')
                                        elif 2 == ind or 3 == ind:
                                            pool[k].vx = item[0]
                                            pool[k].vy = item[1]
                                            jkisConflict(pool[k], pool[j], i, value, 'diffdir')
                                    else:
                                        jkisConflict(pool[k], pool[j], i, None)
                                        cantSolveConflict(i, pool[j], pool[k])
        global cost_arr
        cost_arr.append(cost_sum)
        move(pool)

def showcost(fr, to, cost_arr):
    if to-fr != len(cost_arr):
        print 'fr %d to %d lencost %d' % (fr, to, len(cost_arr))
        print 'length can\'t match'
    x = range(fr, to)
    x = ['%s' % item for item in x]
    y = ['%s' % item for item in cost_arr]
    funcname = 'showcost'
    content = 'function %s\n' % funcname
    content += '\tx = [' + ', '.join(x) + ']\n'
    content += '\ty = [' + ', '.join(y) + ']\n'
    content += '\tplot(x, y)\n'
    content += 'end\n'
    f = open(funcname+'.m', 'w')
    f.write(content)
    f.close()   
    

def showflightnumarr(arr):
    x = ['%s' % item['t'] for item in arr]
    y = ['%s' % item['num'] for item in arr]
    funcname = 'showflightnumarr'
    content = 'function %s\n' % funcname
    content += '\tx = [' + ', '.join(x) + ']\n'
    content += '\ty = [' + ', '.join(y) + ']\n'
    content += '\tplot(x, y)\n'
    content += 'end\n'
    f = open(funcname+'.m', 'w')
    f.write(content)
    f.close() 
    
def initConflictMap(map, flightsinfo, fr, to):
    whichline = 0
    for arr in flightsinfo:
        for item in arr:
            map.append({'index':'%s_%s'%(whichline, item['index']), 'arr':[0 for i in xrange(fr, to)]})
        whichline += 1

if '__main__' == __name__:
    cost_arr = []
    flightnumarr = []
    leaveinfo = []
    conflictMap = []
    sector_info = dataLoader.readinput()
    if len(sys.argv) >= 2:
        varr = [int(x) for x in sys.argv[1].split(';')]
        bIsBat = True
    else:
        varr = [None for i in xrange(len(sector_info['lines']['begin']))]
        bIsBat = False
    drawMap(sector_info)
    flightsinfo = drawFlightsInfo(sector_info, varr)
    initConflictMap(conflictMap, flightsinfo, sector_info['flightstream']['time']['f'], sector_info['flightstream']['time']['simulate_end_time'])
    simulate(flightsinfo, sector_info)
    showcost(sector_info['flightstream']['time']['f'], sector_info['flightstream']['time']['simulate_end_time'], cost_arr)
    showflightnumarr(flightnumarr)
    
    for item in conflictMap:
        print item['index'], ' ', len(item['arr'])

    sum = {'all':0}
    cnt = {'all':0}
    print 'line|time|leavetime'
    for item in leaveinfo:
        for pl in item:
            print '%s|%s|%s' % (pl.line, pl.time, pl.leaveTime)
            dert = pl.leaveTime - pl.time
            sum['all'] += dert
            cnt['all'] += 1
            if sum.get(pl.line, None) is None:
                sum[pl.line] = dert
                cnt[pl.line] = 1
            else:
                sum[pl.line] += dert
                cnt[pl.line] += 1
    print 'line|planeCnt|aveTime'
    aveTime = open('aveTime.txt', 'w')
    for key in sum:
        msg = '%s|%s|%s' % (key, cnt[key], sum[key]*1./cnt[key])
        print msg
        aveTime.write(msg + '\n')
    aveTime.close()
    
    total_cost_sum = reduce(lambda a, b : a+b, cost_arr)
    print 'total_cost_sum : %s' % total_cost_sum
    fr = sector_info['flightstream']['time']['f']
    to = sector_info['flightstream']['time']['simulate_end_time']
    ave_cost = total_cost_sum / (to - fr)
    print 'ave_cost : %s' % ave_cost
    
    if bIsBat:
        vstr = ' '.join(['%s' % item for item in varr])
        msg = '%s %s\n' % (vstr, ave_cost)
        batOutput = open('./output/batOutput.txt', 'a')
        batOutput.write(msg)
        batOutput.close()