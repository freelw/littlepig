import os

def getSpeed():
    speed_fr = 360
    speed_to = 504
    i = speed_fr
    while i < speed_to:
        yield i
        i += 5

def work(i, j):
    os.system('clean.bat')
    os.system('cleancache.bat')
    os.system('python complexity.py %s;%s' % (i, j))

if '__main__' == __name__:

    for i in getSpeed():
        for j in getSpeed():
            print i, ' ', j
            work(i, j)