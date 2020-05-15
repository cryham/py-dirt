#!/usr/bin/python3
#!/usr/bin/env python3
import os
import math
import random
from utils import *
from optparse import OptionParser


#  Options
#---------------------------------------------
op = OptionParser(description='Find duplicate files and delete. '+
    'Rename with added rating from duplicates count.') #, usage='',epilog='')
op.add_option('-t', '--test', dest='test',
                    help='Test only and show stats', action='store_true', default=False)
op.add_option('-l', '--nolist', dest='print_files',
                    help='Don\'t list files only stats', action='store_false', default=True)

op.add_option('-d', '--dir', dest='dir',
                    help='Path. If not set, uses current', default='')
op.add_option('-n', '--nosub', dest='recursive',
                    help='Don\'t check subdirs', action='store_false', default=True)
op.add_option('-a', '--across', dest='across',
                    help='Test duplicates across dirs', action='store_true', default=False)
op.add_option('-s', '--size', dest='size', type='int', default = -4096,
                    help='Size to read, -1 full (slow), 0 none, default -4096, - from end, + from beginning')

(opts, args) = op.parse_args()

print('Options:  test '+yn(opts.test)+'  list '+yn(opts.print_files))
print('  subdirs '+yn(opts.recursive)+'  across '+yn(opts.across)+'  size '+str(opts.size))


#  Start dir
if opts.dir == '':
    start_dir = os.getcwd()
    #  test only, comment out
    #start_dir += '/test-dirs/1'
    start_dir += '/test-dirs/2'
    #start_dir += '/../dirtest/fmt'
    #start_dir += '/../dirtest/zc'
    #start_dir += '/../dirtest/zc2'
    #start_dir += '/../dirtest/zi'
else:
    start_dir = opts.dir

#print('Path: ' + start_dir + 'recursive '+str(opts.recursive))
print('---------------------------------------------')


#  Var
file_list = list()   # all files
file_count = dict()  # same file properties count for unique

#  stats
class cstats:
    all_dirs = 0
    all_files = 0
    left_files = 0  # left after deleting duplicates
    all_size = 0
    left_size = 0

class cfile:
    fpath = ''  # full path with file
    dir = ''  # just dir
    fne = ''
    ext = ''
    unique = True
    #same_count = 0

stats = cstats()


#  Process 1 file
#---------------------------------------------
def process_file(dir, fname):
    #print(fpath)
    fpath = os.path.join(dir, fname)
    if not os.path.isfile(fpath):
        return

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
    cf.fpath = fpath
    cf.dir = dir
    cf.fne = fne
    cf.ext = ext
    cf.size = size
    cf.unique = unique
    
    #  file  info
    #  align size right, unique +, fname
    if opts.print_files:
        #print(fne+'  s '+str(size)+' '+str(unique))
        #print(fname+'  '+cf.fne+cf.ext+'  {:12d}'.format(cf.size)+'  u: '+str(unique))
        if unique:
            u = ' + '
        else:
            u = ' - '
        print('{:>12}'.format(str_size(size)) +
            ' ' + u + ' ' + fname)

    #  add
    file_list.append(cf)
    return


#  Main get loop
#---------------------------------------------
if not opts.recursive:
    print(start_dir)
    files = os.listdir(start_dir)

    files.sort()
    for fname in files:
        process_file(start_dir, fname)
else:
    for dir, subdirs, files in os.walk(start_dir):
        print(dir)
        stats.all_dirs += 1

        #  each dir separate
        #  don't clear for across dirs
        if not opts.across:
            file_list.clear
            file_count.clear

        files.sort()
        for fname in files:
            process_file(dir, fname)


print('----- stats -----')
print(' dirs:  ' + str(stats.all_dirs))
if stats.all_files > 0:
    print('files:  {:.2f}'.format(100.0 * stats.left_files / stats.all_files) + '%  ' + str(stats.left_files) + ' / ' + str(stats.all_files))
if stats.all_size > 0:
    print(' size:  {:.2f}'.format(100.0 * stats.left_size / stats.all_size) + '%  ' + str_size(stats.left_size) + ' / ' + str_size(stats.all_size) + ' B')
print(' free:  ' + str_size(stats.all_size - stats.left_size) + ' B')


#  delete, rename files
if not opts.test:
    print('----- deleting')
    
    for f in file_list:
        unique_file = (f.fne, f.ext, f.size)  #, f.hash)
        count = file_count.get(unique_file, 0)
        if not f.unique:  # delete
            if opts.print_files:
                print(str(count)+' '+f.fpath)
            #os.remove(f.path)
        else:  # rename
            os.path.split(f.fpath)
            # dont rename to existing file
            #os.rename(f.path, '`'+f.)
