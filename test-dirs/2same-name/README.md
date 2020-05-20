### Test 2same-name

One already existing `` `e `` file.

e and e(1) are same, size 7 B  
e(1) gets deleted, e would be renamed to `` `e `` but this exeist so it becomes `` `ea ``

3 are same e(2), e(3), e(4), size 2 B  
(same name as e and e(1) had but other size), so e(3) and e(4) get deleted and e(2) renamed to _e(2)

e(5) has same size as above 3 files, but other content so hash is different, thus e(5) is unique and stays

f is unique, no changes

List format:  
`file size    # or - (unique or deleted)   file name`  
List format after Executing:  
`# or - (unique or deleted)   duplicates count   new file name`

Listing:
```
           5  #  `e
           7  #  e
           7  -  e(1)
           2  #  e(2)
           2  -  e(3)
           2  -  e(4)
           2  #  e(5)
           2  #  f
----- Stats -----
 Dirs:  1
Files:  66.67%  6  /  9
 Size:  98.57%  759  /  770 B
 Free:  11 B
----- Executing
./test-dirs/2same-name
   exists: `e
   #  2  `ea
   -  2  e(1)
   #  3  _e(2)
   -  3  e(3)
   -  3  e(4)
```

Note: sizes will be different because of this README.md file.
