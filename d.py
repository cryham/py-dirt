#!/usr/bin/python3
#!/usr/bin/env python3
import os
import math
import random
from utils import *
from optparse import OptionParser


#  args
#---------------------------------------------
op = OptionParser(description='Find duplicate files and delete. '+
    'Rename with added rating from duplicates count.') #, usage='',epilog='')
op.add_option('-d', '--dir', dest='dir',
                    help='Path. If not set, uses current', default='')
op.add_option('-t', '--test', dest='test',
                    help='Test only and show stats', action='store_true', default=False)
op.add_option('-n', '--nosub', dest='recursive',
                    help='Don\'t check subdirs', action='store_false', default=True)
op.add_option('-s', '--size', dest='size', type='int', default = -4096,
                    help='Size to read, -1 full, 0 none, default -4096, - from end, + from beginning')
op.add_option('-a', '--across', dest='across',
                    help='Test duplicates across dirs', action='store_true', default=False)

(opts, args) = op.parse_args()

print('Args: test '+yn(opts.test)+', subdirs '+yn(opts.recursive)+
      ', across '+yn(opts.across)+', size '+str(opts.size))


#  start dir
if opts.dir == '':
    start_dir = os.getcwd()
    #start_dir += '/test-dirs/1'  # test
    start_dir += '/test-dirs/2'  # test
else:
    start_dir = opts.dir

#print('Path: ' + start_dir + 'recursive '+str(opts.recursive))
print('---------------------------------------------')


#  var
file_list = list()  # all files
file_count = dict()  # same file properties count for unique

#  stats
class cstats:
    all_dirs = 0
    all_files = 0
    left_files = 0  # left after deleting duplicates
    all_size = 0
    left_size = 0

class cfile:
    path = ''
    fne = ''
    ext = ''
    unique = True
    #same_count = 0

stats = cstats()


#  process 1 file
#---------------------------------------------
def process_file(fpath, fname):
    #print(fpath)

    fspl = os.path.splitext(fname)
    fne = fspl[0]  # fname no ext
    ext = fspl[1]
    
    size = os.path.getsize(fpath)
    stats.all_files += 1
    stats.all_size += size
    #print(fname + '  ' + str(size) + '  ' + fne + ' ' + ext)

    #  find (n) in name
    l = fne.rfind('(')
    r = fne.rfind(')')

    if l+1 < r and l > 0 and r > 0:
        n = fne[l+1:r]  # num (n)
        fnb = fne[:l]  # fname no ()
        fne = fnb
    #print('l '+str(l)+' r '+str(r))
    

    #  file properties needed to be different for being unique
    unique_file = (fne, ext, size)  #, hash)
    in_count = file_count.get(unique_file, 0)
    file_count[unique_file] = in_count + 1  # inc count

    if in_count == 0:
        unique = True
        stats.left_files += 1
        stats.left_size += size
    else:
        unique = False

    #  cfile
    cf = cfile()
    cf.path = fpath
    cf.fne = fne
    cf.ext = ext
    cf.size = size
    cf.unique = unique
    
    #  file  info
    #print(fne+'  s '+str(size)+' '+str(unique))
    #print(fname+'  '+cf.fne+cf.ext+'  {:12d}'.format(cf.size)+'  u: '+str(unique))
    if unique:
        u = ' + '
    else:
        u = ' - '
    print('{:9d}'.format(cf.size)+' '+u+fname)

    #  add
    file_list.append(cf)
    return


#  main get loop
#---------------------------------------------
if not opts.recursive:
    print(start_dir)  #+'/  ----')
    files = os.listdir(start_dir)
    for fname in files:
        process_file(fpath, fname)
        print(fname, start_dir)
else:
    for root, subdirs, files in os.walk(start_dir):
        print(root)  #+'/  ----')
        stats.all_dirs += 1

        #  each dir separate
        #  don't clear for across dirs
        if not opts.across:
            file_list.clear
            file_count.clear

        for fname in files:
            fpath = os.path.join(root, fname)
            process_file(fpath, fname)


print('----- stats -----')
print(' dirs:  ' + str(stats.all_dirs))
print('files:  {:.2f}'.format(100.0 * stats.left_files / stats.all_files) + '%  ' + str(stats.left_files) + ' / ' + str(stats.all_files))
print(' size:  {:.2f}'.format(100.0 * stats.left_size / stats.all_size) + '%  ' + str_size(stats.left_size) + ' / ' + str(stats.all_size) + ' B')
print(' free:  '+str_size(stats.all_size - stats.left_size) + ' B')


#  delete, rename files
if not opts.test:
    print('----- deleting')
    
    for f in file_list:
        unique_file = (f.fne, f.ext, f.size)  #, f.hash)
        count = file_count.get(unique_file, 0)
        print(f.path)
        #if not file.unique:
        #  delete
        pass
