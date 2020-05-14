#!/usr/bin/python3
#!/usr/bin/env python3
import os
from optparse import OptionParser


#  start dir
#---------------------------------------------
start_dir = os.path.curdir
#start_dir += '/test-dirs/1'
start_dir += '/test-dirs/2'
print('---------------------------------------------')
#print(dir1)


#  args
#---------------------------------------------
op = OptionParser()
op.add_option("-t", "--test", dest="test", help="Test only", action="store_true", default=False)
op.add_option("-s", "--size", dest="size", type="int", default=4096, help="Size to read, -1 full, 0 none")

(opts, args) = op.parse_args()

print("Args: test %r" % opts.test,end='')
print(", size %d" % opts.size)


#  var
file_set = set()


#  process 1 file
#---------------------------------------------
def process_file(fpath, fname):
    file_set.add(fpath)
    return


#  main loop
#---------------------------------------------
for root, subdirs, files in os.walk(start_dir):
    print(root)

    #  each dir separate
    #  todo: don't clear for across dirs
    file_set.clear

    for fname in files:
        fpath = os.path.join(root, fname)
        process_file(fpath, fname)

    print('-----')
    for file in file_set:
        print(file)
