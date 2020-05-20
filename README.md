## About

Python command line tool for finding and deleting duplicated files.  
Also renaming with added rating symbols, from count of duplicates.  
Name comes from: Python Directory Tree.

## How it works and Features

Options (`-l -d` etc.) are listed below for features.  
This tool:
- **Lists** files (use `-l` to show) in current directory (or specified after `-d`).  
  By default recursively. Use -n to not check **subdirs**.
- Gets for each file: its name, extension, size, and reads part of file to get **hash** value.  
  By default size is 4kB from end (-4096).  
  Use e.g. `-s 1024` for 1k from start. Or `-s 1` to read full files (slow).
- Files are **unique** when at least one of their properties are:  
  file name (without rating chars, e.g. added in previous run), extension, file size or hash value.  
  *In `d.py` after `def unique_attrs`*
- By default it checks for unique files **across** subdirs (use `-a` not to, i.e. only in each dir).
- After that it writes **Stats**, showing Dirs and Files counts (left and all) and Size reduction.  
  E.g. `Files:  33%  1 / 3` would mean that of all 3 files 1 is left and that's 33%.  
  Same goes for `Size:`. It's in Bytes and sepearated with `g m k` (giga mega kilo, 1000 multipliers).
- If used debug or test `-t` it will end now.
- If not, it starts **Executing**, i.e. deleting duplicated files and renaming those left with rating.
- If no execute `-x` is used it will show same output but won't execute.
- Rating can be added as prefix (default, use `-p` to disable) *at begin of filename*,  
  increasing with duplicated files count `` ` _ ^ - , + ) ( ! !! ``  
  *In `d.py` after `ratings =`*  
  Or as a numeric suffix *at end of filename*, from _1 to _9 and above (use with `-u`).
- Rating can be offset by a value with `-i value`.
- If new filename already exists, a suffix letter (`a` to `z`) will be added to filename.

List format (header):  
`file size | # or - (unique or deleted) | file name`  
List format after Executing:  
`# or - (unique or deleted) | duplicates count | new file name`

## Testing and Examples

For testing included examples (in `test-dirs/`)  
set `debug = True` in `d.py` (and comment out `#debug = False`) to test how the tool works.  
Uncomment (no #) just one of lines with `start_dir +=` for a test.

Those test **examples** have README.md files inside subdirs, explaining what happens with tool output:  
[1simple](https://github.com/cryham/py-dirt/tree/master/test-dirs/1simple), 
[2same-name](https://github.com/cryham/py-dirt/tree/master/test-dirs/2same-name), 
[3two-dir](https://github.com/cryham/py-dirt/tree/master/test-dirs/3two-dir)

## Usage

Start `./d.py -h` for **help** on options.  

Use `./d.py -t` first to test dir and show Stats (nothing executed). With `-l` it will also list files.  

Using `-o` will only show final options (Yes/No).  

All options also have longer names e.g. `--list`.  
To change any option's default value change last 0 or 1 to opposite at end of line e.g. with `opt_bool('-t',`  
