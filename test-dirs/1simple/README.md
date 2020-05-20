### Test 1simple

3 unique files

a and a(1) are same, a(1) gets deleted, a is renamed to `a, lowest rating  
3 same b(2), b(2), b(3) so b(2) stays, rest deleted, b(2) renamed to _b(2) 2nd rating 3x  
c is unique, nothing changes

List format:  
`file size    # or - (unique or deleted)   file name`  
List format after Executing:  
`# or - (unique or deleted)   duplicates count   new file name`

Listing:
```
           7  #  a
           7  -  a(1)
           2  #  b(2)
           2  -  b(3)
           2  -  b(4)
           2  #  c
----- Stats -----
 Dirs:  1
Files:  57.14%  4  /  7
 Size:  95.44%  230  /  241 B
 Free:  11 B
----- Executing
./test-dirs/1simple
   #  2  `a
   -  2  a(1)
   #  3  _b(2)
   -  3  b(3)
   -  3  b(4)
```

Note: sizes will be different because of this README.md file.
