## Test 4clean-name

All files have same size and content.

Names are treated the same after cleaning from:
- rating prefixes `` ` _ ! `` etc.
- and any chars after (number).

This way 5 files `f`, `f(2)`, ````f(2)``, `!f(3)` and `f(2)abc` are all `f` named.  
Since `!f(3)` was  found first it will stay, with added `-` prefix (rating 5), and other files are deleted.

The files `f(2)(2)` and `fa(2)` are unique (not `f` named) and not changed.

## Listing:
List format:  
`file size  |  # or - (unique or deleted)  |  file name`  
List format after Executing:  
`# or - (unique or deleted)  |  duplicates count  |  new file name`

Note: sizes and Stats will be slightly different because of this README.md file.

```
           2  #  !f(3)
      1k 216  #  README.md
           2  -  ``f(2)
           2  -  f
           2  -  f(2)
           2  #  f(2)(2)
           2  -  f(2)abc
           2  #  fa(2)
----- Stats -----
 Dirs:  1
Files:  50.00%  4  /  8
 Size:  99.35%  1k 222  /  1k 230 B
 Free:  8 B
----- Executing
./test-dirs/4clean-name
   #  5  -!f(3)
   -  5  ``f(2)
   -  5  f
   -  5  f(2)
   -  5  f(2)abc
```
