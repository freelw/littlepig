import random
import dataLoader

def judge(arr, separation, clearance):
    def transkm(s):#nm 2 km
        return s*1.852
    for i in xrange(len(arr)-1):
        timehour = (arr[i+1]['time'] - arr[i]['time'])*1./3600
        timemin = (arr[i+1]['time'] - arr[i]['time'])*1./60
        if separation > timehour * arr[i]['v']:
            return False
        if clearance > timehour * arr[i]['v']:
            return False
            
        def feql(a, b):
            return abs(a-b) < 1e-7
        #if feql(arr[i]['v'], arr[i+1]['v']) and timemin < 10:
        #    return False
        #if transkm(arr[i]['v']) - 40 > transkm(arr[i+1]['v']) and timemin < 5:
        #    return False
        #if transkm(arr[i]['v']) - 80 > transkm(arr[i+1]['v']) and timemin < 3:
        #    return False
    return True
    
def buildstream():
    
    obj = getfsObj()
    tf = obj['time']['f']
    tt = obj['time']['t']
    flighttypes = obj['flighttypes']
    typesnum = len(flighttypes)
    flightnum = obj['flightnum']
    retry = obj['retry']
    separation = obj['separation']
    clearance = obj['clearance']
    bBindClearance = obj['bBindClearance']
    bVsame = obj['bVsame']
    #print '%d %d %d' % (f, t, flightnum)  
    type = getrd(0, typesnum)
    vf = flighttypes[type]['vf']
    vt = flighttypes[type]['vt']
    v = getrd(vf, vt)
    baseTime = tf + getrd(0, clearance/v)
    
    for i in xrange(retry):
        arr = []
        for j in xrange(flightnum):
            if bBindClearance:
                arr.append({'time':baseTime + j*(clearance+1)/v*3600, 'v':v, 'type':type})
            else:
                if not bVsame:
                    v = getrd(vf, vt)
                arr.append({'time':getrd(tf, tt), 'v':v, 'type':type})
        def func(a):
            return a['time']
        arr.sort(key=func)
        for j in xrange(len(arr)):
            arr[j]['index'] = j
        if judge(arr, separation, clearance):
            print 'buildstream ok'
            return arr
        print 'retry ', i+1, ' time'
    else:
        print 'buildstream failed'
        return []
    
def getfsObj():
    obj = dataLoader.readinput()
    return obj['flightstream']

def getrd(f, t):
    len = t - f
    return int(random.random() * len) + f
    
if '__main__' == __name__:
    print 'flightstream'
    print buildstream()