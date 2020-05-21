#!/usr/bin/python3
#!/usr/bin/env python3
import os
import hashlib
from optparse import OptionParser
from utils import *


#  Flags
#---------------------------------------------
test = False
execute = True

#debug = True  # Dev Test
debug = False  # in Release !


# Ratings  chars sorted
#   used:  ` _ ^ - , ) ( ! 
#   all :  ` _ ^   ] [ @ = ;   . - , + ) (   ' & % # !
# bad sort:  } { ~ $ . 
# not on windows:  < > : " / \ | ? *

# prefixes for filename, with more duplicates
ratings = ['`','_','^','-',',','+',')','(','!','!!']  # 10


#  Options
#------------------------------------------------------------------------------------------
op = OptionParser(description='Find and delete duplicated files. '+
    'Rename with added rating from duplicates count.') #, usage='',epilog='')

def opt_bool(sh,long, dest,help, default):
    if default != 0:
        op.add_option(sh,long, dest=dest, help=help, action='store_false', default=True)
    else:
        op.add_option(sh,long, dest=dest, help=help, action='store_true', default=False)

opt_bool('-t', '--test',   'test',      'Test only and show stats', 0)
opt_bool('-o', '--opt',    'only',      'Only show options and quit', 0)
opt_bool('-l', '--list',   'list',      'List files, not just only stats', 0)
opt_bool('-x', '--exec',   'noexecute', 'Excecute (delete or rename)', 0)

opt_bool('-n', '--sub',    'recursive', 'Check subdirs', 1)
opt_bool('-a', '--across', 'across',    'Test duplicates across dirs', 1)  # 1
op.add_option('-d', '--dir', dest='dir', help='Path. If not set, uses current', default='')
op.add_option('-s', '--size', dest='h_size', type='int', default = -4096,
            help='Size to read, 1 full (slow), 0 none, default -4096, - from end, + from beginning')

opt_bool('-p', '--prefix', 'prefix',
            'Add prefix rating symbol, from duplicate count  ` _ ^ - , ) ( ! !!', 1)
opt_bool('-u', '--suffix', 'suffix',    'Add suffix ratings  _1 to _9', 0)
op.add_option('-i', '--offset', dest='offset',
            help='Offset value to add to rating count', type='int', default = 0)

(opt, args) = op.parse_args()

h_size = abs(opt.h_size)
if opt.noexecute:
    execute = False
if opt.test:
    test = True

if debug:
    opt.list = True
    #test = True  # force -t for testing only
    execute = False  # don't execute

print('Options:  test '+yn(test)+'  execute '+yn(execute)+'  list '+yn(opt.list))
print('  subdirs '+yn(opt.recursive)+'  across '+yn(opt.across)+'  size '+str(opt.h_size))
print('  prefix '+yn(opt.prefix)+'  suffix '+yn(opt.suffix))


#  Start dir
#---------------------------------------------
if opt.dir == '':
    start_dir = os.getcwd()

    if debug:  #  test only
        #start_dir += '/test-dirs/1simple'
        #start_dir += '/test-dirs/2same-name'
        #start_dir += '/test-dirs/3two-dir'
        start_dir += '/test-dirs/4clean-name'
else:
    start_dir = opt.dir

if opt.only:
    print('Path: ' + start_dir)
    exit(0)

if opt.list:
    print('---------------------------------------------')


#  Var
#---------------------------------------------
file_list  = list()  # all files
file_count = dict()  # same file properties count for unique

#  stats
class cStats:
    all_dirs = 0
    all_files = 0
    all_size = 0
    left_files = 0  # left after deleting duplicates
    left_size = 0

class cFile:
    def __init__(self, fpath, dir, fneu, fne, ext, size, hash):
        self.fpath = fpath  # full path with file
        self.dir = dir      # just dir path
        self.fneu = fneu    # filename, no ext, no ratings, for unique test
        self.fne = fne      # filename, no ext
        self.ext = ext      # file extension
        self.size = size    # file size B
        self.hash = hash    # hash from file contents, 0 if not used
        self.unique = True

    def unique_attrs(self, across):
        #  file properties needed to be different for file being unique
        #return (self.ext, self.size, self.hash))  # test .. different names but same content
        return ((self.fneu, self.ext, self.size, self.hash) if across
            else (self.dir, self.fneu, self.ext, self.size, self.hash))

stats = cStats()


#  Hash
#---------------------------------------------
def get_hash(file):
    hasher = hashlib.md5()
    #print(file+' '+str(opt.h_size))
    with open(file, "rb") as f:
        if opt.h_size < -1:  # from end
            try:  # fails: h_size > f.sizeof
                f.seek(opt.h_size, os.SEEK_END)
            except:
                pass
                #print('xx')
            buf = f.read()
        else:
            if h_size == 1:  # read full
                buf = f.read()
            else:  # from begin
                buf = f.read(h_size)
        #print(buf)
        hasher.update(buf)
    return hasher.hexdigest()


#  Process 1 file
#------------------------------------------------------------------------------------------
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

    #  find (n) in name  --
    #  this will ignore any suffix chars after (n) e.g. (n)ab^`
    l = fne.rfind('(')
    r = fne.rfind(')')
    fneu = fne

    if l+1 < r and l > 0 and r > 0:
        num = fne[l+1 : r]  # num (n)
        fnb = fne[ : l]  # fname no ()
        fneu = fnb
    #print('l '+str(l)+' r '+str(r))
    
    #  ignore rating prefixes, if already  --
    if opt.prefix:
        for r in ratings:
            while fneu.startswith(r):
                fneu = fneu[len(r) : ]
    
    #  get hash
    hash = get_hash(fpath) if  opt.h_size != 0  else 0

    #  cfile
    cf = cFile(fpath, dir, fneu, fne, ext, size, hash)
    unique_at = cf.unique_attrs(opt.across)
    in_count = file_count.get(unique_at, 0)
    file_count[unique_at] = in_count + 1  # inc count

    unique = True if  in_count == 0  else False
    if unique:
        stats.left_files += 1
        stats.left_size += size

    #  file  info
    if opt.list:
        u = ' # ' if  unique  else ' - '
        #  align size right, unique +, fname
        print('{:>12}'.format(str_size(size)) +
            ' ' + u + ' ' + fname)# + ' ' + hash)

    #  add
    cf.unique = unique
    file_list.append(cf)
    return


#  Main get loop
#------------------------------------------------------------------------------------------
if not opt.recursive:
    if opt.list:
        print(start_dir)
    files = os.listdir(start_dir)

    files.sort()
    for fname in files:
        process_file(start_dir, fname)
else:
    for dir, subdirs, files in os.walk(start_dir):
        if dir.find('/.') != -1:  # skip hidden
            continue

        if opt.list:
            print(dir)
        stats.all_dirs += 1

        #  each dir separate
        #  don't clear for across dirs
        if not opt.across:
            #file_list.clear
            file_count.clear

        files.sort()
        for fname in files:
            process_file(dir, fname)


print('----- Stats -----')
print(' Dirs:  ' + str(stats.all_dirs))
if stats.all_files > 0:
    print('Files:  {:.2f}'.format(100.0 * stats.left_files / stats.all_files) + '%  ' + str(stats.left_files) + '  /  ' + str(stats.all_files))
if stats.all_size > 0:
    print(' Size:  {:.2f}'.format(100.0 * stats.left_size / stats.all_size) + '%  ' + str_size(stats.left_size) + '  /  ' + str_size(stats.all_size) + ' B')
print(' Free:  ' + str_size(stats.all_size - stats.left_size) + ' B')


#  Delete, Rename files
tab = '   '
if not test:
    print('----- Executing')
    dir = ''
    
    for f in file_list:
        
        if dir != f.dir:
            dir = f.dir
            if opt.list:
                print(dir)
        
        unique_at = f.unique_attrs(opt.across)
        count = file_count.get(unique_at, 0) + opt.offset
        
        if not f.unique:  #  delete
            ch = '-'
            name = f.fpath[ len(dir)+1 : ]
            
            if execute:
                try:
                    os.remove(f.fpath)
                except Exception as ex:
                    print(tab + 'delete failed: ' + f.fne + ' ' + str(ex))
        else:
            if count < 2:
                continue
            
            #  rename with rating prefix
            pref = ''
            sufx = ''
            if opt.prefix:
                pref = ratings[min( max(0, count-2), len(ratings)-1 )]
            if opt.suffix:
                sufx = '_' + str(count)

            ch = '#'  #  dont rename to existing file(s)
            add = ''
            while True:
                new_file = pref + f.fne + sufx + add + f.ext
                new_fpath = os.path.join(f.dir, new_file)
                name = new_file
                
                if not os.path.exists(new_fpath):
                    break
                print(tab + 'exists: ' + new_file)
                add = 'a' if  add == ''  else chr(ord(add[0]) + 1)  # a,b,c..

            if execute:
                try:
                    os.rename(f.fpath, new_fpath)
                except Exception as ex:
                    print(tab + 'rename failed: ' + f.fne + ' ' + str(ex))

        if opt.list:
            print(tab + ch + '  ' + str(count) + '  ' + name)
