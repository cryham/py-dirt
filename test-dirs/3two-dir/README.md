## Test 3two-dir

a.txt and a(1).txt are same, size 39 B,  
so a.txt is deleted, a(1).txt would be renamed to `` `a(1).txt``,  
**but** subdir `bb/` has also: a.txt and a(1).txt, same 39 B as before,  
so these are deleted (e.g. a(2).txt would be too or just a.txt).  
This is with `across Yes`, with `-a`it won't happen.

c.c, c(2).c and c(4).c are same, size 0 B,  
so c(2).c is renamed to _c(2).c and rest deleted

c(3).c, c(5).c, c(6).c and c(8).c are same, size 2B,  
so c(3).c is renamed to ^c(3).c and rest deleted

Rest of files are already rather obvious (`d*, b*.txt`).

## Listing:
List format:  
`file size  |  # or - (unique or deleted)  |  file name`  
List format after Executing:  
`# or - (unique or deleted)  |  duplicates count  |  new file name`

Note: sizes and Stats will be slightly different because of this README.md file.

```
         742  #  README.md
          39  #  a(1).txt
          39  -  a.txt
           0  #  c(2).c
           2  #  c(3).c
           0  -  c(4).c
           2  -  c(5).c
           2  -  c(6).c
           2  -  c(8).c
           0  -  c.c
           7  #  d
           7  -  d(1)
           2  #  d(2)
           2  -  d(3)
./test-dirs/3two-dir/bb
          39  -  a(1).txt
          39  -  a.txt
          39  #  b(1).txt
          39  -  b(2).txt
           3  #  b(3).txt
----- Stats -----
 Dirs:  2
Files:  42.11%  8  /  19
 Size:  82.99%  834  /  1k 005 B
 Free:  171 B
----- Executing
./test-dirs/3two-dir
   #  4  ^a(1).txt
   -  4  a.txt
   #  3  _c(2).c
   #  4  ^c(3).c
   -  3  c(4).c
   -  4  c(5).c
   -  4  c(6).c
   -  4  c(8).c
   -  3  c.c
   #  2  `d
   -  2  d(1)
   #  2  `d(2)
   -  2  d(3)
./test-dirs/3two-dir/bb
   -  4  a(1).txt
   -  4  a.txt
   #  2  `b(1).txt
   -  2  b(2).txt
```
