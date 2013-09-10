import fileinput
import os


def dir_of(path):
    d, f = os.path.split(path)
    return d

for line in fileinput.input():
    try:
        weight,left,right = line.split()
        nodes = left,right
        dleft,dright = dir_of(left),dir_of(right)
        if dleft == dright:
            continue
        print weight, dleft, dright
    except:
        print "cannot process", line

    
