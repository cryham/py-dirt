#!/usr/bin/python3
#!/usr/bin/env python3
import os
import math
import random


#  utils
#---------------------------------------------

#  get file ext by content. only few, images
def get_file_ext(fpath) -> str:
    with open(fpath, "rb") as f:
        #if f.size < 16:  # checked before
        #    return '?'
        buf = f.read(16)
        if buf[8:12] == b'WEBP':
            return 'webp'
        if buf[0:3] == b'GIF':
            return 'gif'
        if buf[1:4] == b'PNG':
            return 'png'
        if buf[0:4] == b'\xff\xd8\xff\xe0' or buf[6:10] == b'Exif':  #'ÿØÿà'
            return 'jpg'  # same for: jpg jpeg jpe
        if buf[1:4] == b'PDF':
            return 'pdf'
        if buf[0:2] == b'BM':
            return 'bmp'
    return '?'  # unknown


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


#  test  str_size
if 1==2:
    for i in range(10):
        x = math.pow(10,i)
        d = int(round(x))
        #print(d)
        e = random.randint(0,d) + d
        print(e)
        print(str_size(e,kmg=True))
    exit(1)
