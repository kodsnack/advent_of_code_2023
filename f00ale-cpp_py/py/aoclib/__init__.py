import os
import os.path
import sys

def readdata():
    name = os.path.basename(sys.argv[0]).split('.')[0]
    with open(f'{os.path.dirname(os.path.abspath(__file__))}/../../data/{name}.txt') as fp:
        return fp.readlines()

def readans():
    name = os.path.basename(sys.argv[0]).split('.')[0]
    name = name.replace('p','a')
    ret = None
    try:
        with open(f'{os.path.dirname(os.path.abspath(__file__))}/../../data/{name}.txt') as fp:
            lines = fp.readlines()
            ret = lines[0].strip(), lines[1].strip()
    except:
        pass
    return ret

def checkans(a1, a2):
    corr = readans()
    ok1 = 'Unknown'
    ok2 = 'Unknown'
    if corr:
        ok1 = 'OK' if str(a1) == corr[0] else f'Expected <{corr[0]}>'
        ok2 = 'OK' if str(a2) == corr[1] else f'Expected <{corr[1]}>'
    print(f'{a1} {ok1}')
    print(f'{a2} {ok2}')
