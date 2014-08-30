import json

def readinput():
    try:
        input = open('conf.txt')
        content = ''
        for line in input:
            content += line
        obj = json.loads(content)
    except Exception, e:
        print 'readinput error %s' % e
        return None
    return obj
    
if '__main__' == __name__:
    print readinput()