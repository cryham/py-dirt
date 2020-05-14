#!/usr/bin/python3
#!/usr/bin/env python3
import os
from optparse import OptionParser


#  start dir
#---------------------------------------------
start_dir = os.path.curdir
start_dir += '/test-dirs/1'
#start_dir += '/test-dirs/2'
print('---------------------------------------------')
#print(dir1)


#  args
#---------------------------------------------
op = OptionParser()
op.add_option("-t", "--test", dest="test", help="Test only", action="store_true", default=False)
op.add_option("-s", "--size", dest="size", type="int", default=4096, help="Size to read, -1 full, 0 none, default 4kB")

(opts, args) = op.parse_args()

print("Args: test %r" % opts.test,end='')
print(", size %d" % opts.size)


#  var
file_set = set()
file_dict = dict()


#  process 1 file
#---------------------------------------------
def process_file(fpath, fname):
    #print(fname)

    fspl = os.path.splitext(fname)
    fne = fspl[0]  # fname no ext
    ext = fspl[1]
    
    size = os.path.getsize(fpath)
    
    #print(fname + '  ' + str(size) + '  ' + fne + ' ' + ext)

    #  find (n) in name
    l = fne.rfind('(')
    r = fne.rfind(')')
    #print("lr " +str(l)+' '+str(r))

    if l+1 < r and l != -1 and r != -1:
        #print(str(l)+' '+str(r))
        n = fne[l+1:r]  # num (n)
        fnb = fne[:l]  # fname no ()
        
        file_set.add((fnb, str(size)))
        file_dict[fnb] = file_dict.get(fnb,0) + 1

        print(fnb+' '+n+'  m '+str(file_dict.get(fnb,0)))

    else:  # no ()
        #print('no ' + fne +' '+ str(size) +' '+ str(l)+' '+str(r))
        file_set.add((fne, str(size)))
        file_dict[fne] = file_dict.get(fne,0) + 1 

        print(fne+'  m '+str(file_dict.get(fne,0)))

    return


#  main loop
#---------------------------------------------
for root, subdirs, files in os.walk(start_dir):
    print(root)

    #  each dir separate
    #  todo: don't clear for across dirs
    file_set.clear
    file_dict.clear

    for fname in files:
        fpath = os.path.join(root, fname)
        process_file(fpath, fname)

    print('-----')
    for file in file_set:
        print(file)
