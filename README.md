## PDFCMD - Utility to Perform Commands on PDF Files
[![PyPi](https://img.shields.io/pypi/v/pdfcmd)](https://pypi.org/project/pdfcmd/)
[![AUR](https://img.shields.io/aur/version/pdfcmd)](https://aur.archlinux.org/packages/pdfcmd/)

This is a Linux command line utility to perform commands on PDF files.
It uses the [PyPDF2](https://github.com/mstamy2/PyPDF2) library. The
following commands are presently implemented, each as an independent
[plugin](pdfcmd/commands).

```
usage: pdfcmd [-h] {info,cat,pages} ...

Utility to perform commands on PDF files.

positional arguments:
  {info,cat,pages}  Available commands:
    info            Show PDF document information.
    cat             Concaternate selected pages of one or more PDF files into
                    a single file.
    pages           Output list of page labels/numbers, or total number of
                    pages.

optional arguments:
  -h, --help        show this help message and exit
```

#### `info` command
```
usage: pdfcmd info [-h] file

Show PDF document information.

positional arguments:
  file        PDF file

optional arguments:
  -h, --help  show this help message and exit
```

#### `cat` command
```
usage: pdfcmd cat [-h] [-o OUTFILE] [-H] ...

Concaternate selected pages of one or more PDF files into a single file.

positional arguments:
  fileranges            Sequence of alternating file names and page ranges
                        (see -H)

optional arguments:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file, default = stdout
  -H, --helppage        print help page describing page range/slice syntax
```

How to specify files and page ranges is described by typing `pdfcmd
cat -H`, which outputs the following:

```
Concaternate selected pages of one or more PDF files into a single file.
Arguments are specified as a sequence of alternating file names and page
ranges:

  file1 pagerange1 file2 pagerange2 ..

Page ranges refer to the previously specified file and are specified in
Python "slice" notation, assuming each page is like an element in a
sequence, starting at 0.

For example, concatenate all of head.pdf, all but page seven of
content.pdf, and the last page of tail.pdf, producing output.pdf:

  pdfcmd cat -o output.pdf head.pdf content.pdf :6 7: tail.pdf -1

A file not followed by a page range means all pages of that file, for
example:

  pdfcmd cat chapter*.pdf >book.pdf

You can also assign a single upper case "handle" to a file at first use
and then use that handle later as shorthand. For example, output the
first page from document1.pdf, the first page of document2.pdf, then
the remaining pages from document1.pdf and document2.pdf:

  pdfcmd cat -o output.pdf A=document1.pdf 0 B=document2.pdf 0 A 1: B 1:

Remember, page indices start with zero.
        Page range expression examples:
            :     all pages.                   -1    last page.
            22    just the 23rd page.          :-1   all but the last page.
            0:3   the first three pages.       -2    second-to-last page.
            :3    the first three pages.       -2:   last two pages.
            5:    from the sixth page onward.  -3:-1 third & second to last.
        The third, "stride" or "step" number is also recognized.
            ::2       0 2 4 ... to the end.    3:0:-1    3 2 1 but not 0.
            1:10:2    1 3 5 7 9                2::-1     2 1 0.
            ::-1      all pages in reverse order.
```

#### `pages` command
```
usage: pdfcmd pages [-h] [-c] file

Output list of page labels/numbers, or total number of pages.

positional arguments:
  file         PDF file

optional arguments:
  -h, --help   show this help message and exit
  -c, --count  just print the total count of pages
```

The latest documentation and code is available at
https://github.com/bulletmark/pdfcmd.

### INSTALLATION

Arch Linux users can install [pdfcmd from the
AUR](https://aur.archlinux.org/packages/pdfcmd).
Python 3.5 or later is required. Note [pdfcmd is on
PyPI](https://pypi.org/project/pdfcmd/) so just ensure that
`python3-pip` and `python3-wheel` are installed then type the following
to install (or upgrade):

```
$ sudo pip3 install -U pdfcmd
```

Alternatively, do the following to install from the source repository.
Note that the `python-pypdf2` package is required.

```sh
$ git clone http://github.com/bulletmark/pdfcmd
$ cd pdfcmd
$ sudo pip3 install -U .
```

### UPGRADE

```sh
$ cd pdfcmd  # Source dir, as above
$ git pull
$ sudo pip3 install -U .
```

### REMOVAL

```sh
$ sudo pip3 uninstall pdfcmd
```

### LICENSE

Copyright (C) 2021 Mark Blakeney. This program is distributed under the
terms of the GNU General Public License.
This program is free software: you can redistribute it and/or modify it
under the terms of the GNU General Public License as published by the
Free Software Foundation, either version 3 of the License, or any later
version.
This program is distributed in the hope that it will be useful, but
WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General
Public License at <http://www.gnu.org/licenses/> for more details.

<!-- vim: se ai syn=markdown: -->
