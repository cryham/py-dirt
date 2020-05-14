#!/usr/bin/python3
#!/usr/bin/env python3
import os


#  start dir
#---------------------------------------------
start_dir = os.path.curdir
start_dir += '/test-dirs/1'
print('---------------------------------------------')
#print(dir1)

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

    file_set.clear

    for fname in files:
        fpath = os.path.join(root, fname)
        process_file(fpath, fname)

    print('-----')
    for file in file_set:
        print(file)
    