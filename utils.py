#!/usr/bin/python3
import os
import math
import random


#  utils
#---------------------------------------------
def yn(b):
    if b:
        return 'Yes'
    else:
        return 'No'

#  format size string
#  e.g.  sep: 1'234,  kmg: 1k 234
def str_size(num, kmg=True, sep=False):
    s = ''
    i = 0
    d = int(num)
    while True:
        if kmg:
            if i==3:
                s = 'k ' + s
            if i==6:
                s = 'm ' + s
            if i==9:
                s = 'g ' + s
        else:
            if sep and i%3==0 and i>0:
                s = "'" + s
        i += 1
        s = str(d % 10) + s
        d //= 10
        if d == 0:
            break
    return s

if 1==2:  # test str_size
    for i in range(10):
        x = math.pow(10,i)
        d = int(round(x))
        #print(d)
        e = random.randint(0,d) + d
        print(e)
        print(str_size(e,kmg=True))
    exit(1)
