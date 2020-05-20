## About

Python command line tool for finding and deleting duplicated files.  
Also renaming with added rating symbols, from count of duplicates.  
Name comes from: Python Directory Tree.

### How it works / Features

Options (`-l -d` etc.) are listed below for features.  
This tool:
- **Lists** files (use `-l`) in current directory (or specified after `-d`).  
  By default recursively. Use -n to not check **subdirs**.
- Gets for each file: its name, extension, size, and reads part of file to get **hash** value.  
  By default size is 4kB from end (-4096). Use e.g. `-s 1024` for 1k from start. Or `-s 1` to read full files (slow).
- File properties needed to be different for files being **unique** are:  
  file name (without rating chars, e.g. added in previous run), extension, file size and hash value.  
  *See `def unique_attrs` in `d.py` for detail*
- By default it checks for unique files **across** subdirs (use `-a` not to, i.e. only in each dir).
- After that it writes **Stats**, showing Dirs and Files counts (left and all) and Size reduction.  
  E.g. `Files:  50%  1 / 2` would mean that of 2 all files 1 is left and that's 50%. Same for size.
- If used debug or test `-t` or no execute `-x` it will end now.
- If not it starts **Executing** (i.e. deleting duplicated files and renaming those left with rating).
- Rating can be added as prefix (default `-p` to disable) *at begin of filename*.  
  For rating prefix characters see `ratings =` in `d.py`, ` _ ^ - , + ) ( ! !!  
  Or as a numeric suffix *at end of filename*, from _1 to _9 and above (used with `-u`).
- Rating can be offset by a value with `-i offset`.

List format:  
`file size    # or - (unique or deleted)   file name`  
List format after Executing:  
`# or - (unique or deleted)   duplicates count   new file name`

## Testing

For testing included examples (in `test-dirs/`)  
just set `debug = True` in `d.py` (and comment out `#debug = False`) to test how the tool works.  
Those test examples have README.md files inside them explaining what happens.

## Usage

Start `./d.py -h` for help on options.  

Use `d -t` first, to test dir and show Stats (nothing executed). With also `-l` it will list files.  


Using `d -o` will only show final options (Yes/No).  

