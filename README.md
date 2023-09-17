## PDFCMD - Utility to Perform Commands on PDF Files
[![PyPi](https://img.shields.io/pypi/v/pdfcmd)](https://pypi.org/project/pdfcmd/)
[![AUR](https://img.shields.io/aur/version/pdfcmd)](https://aur.archlinux.org/packages/pdfcmd/)

This is a Linux command line utility to perform commands on PDF files.
It uses the [pypdf](https://github.com/py-pdf/pypdf) library. The
following commands are presently implemented, each as an independent
[plugin](pdfcmd/commands).

The latest documentation and code is available at
https://github.com/bulletmark/pdfcmd.

## Usage

Type `pdfcmd` or `pdfcmd -h` to view the usage summary:

```
usage: pdfcmd [-h] {cat,help,info,pages} ...

Utility to perform commands on PDF files.

options:
  -h, --help            show this help message and exit

Commands:
  {cat,help,info,pages}
    cat                 Concaternate selected pages of one or more PDF files
                        into a single file.
    help                Show help/usage for this utility.
    info                Show PDF document information.
    pages               Output list of page labels/numbers, or total number of
                        pages.
```

Type `pdfcmd <command> -h` to see specific help/usage for any
individual command:

### Command `cat`

```
usage: pdfcmd cat [-h] [-o OUTFILE] [-a] ...

Concaternate selected pages of one or more PDF files into a single file.

positional arguments:
  fileranges            Sequence of alternating file names and page ranges

options:
  -h, --help            show this help message and exit
  -o OUTFILE, --outfile OUTFILE
                        output file, default = stdout
  -a, --no-aliases      do not use aliases

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

You can also assign a single upper case "alias" name to a file at first
use and then use that alias later as shorthand. For example, output the
first page from document1.pdf, the first page of document2.pdf, then the
remaining pages from document1.pdf and document2.pdf:

  pdfcmd cat -o output.pdf A=document1.pdf 0 B=document2.pdf 0 A 1: B 1:

Page range expression examples (remember, page indices start with zero):
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

### Command `info`

```
usage: pdfcmd info [-h] file

Show PDF document information.

positional arguments:
  file        PDF file

options:
  -h, --help  show this help message and exit
```

### Command `pages`

```
usage: pdfcmd pages [-h] [-c] file

Output list of page labels/numbers, or total number of pages.

positional arguments:
  file         PDF file

options:
  -h, --help   show this help message and exit
  -c, --count  just print the total count of pages
```

### Command `help`

```
usage: pdfcmd help [-h]

Show help/usage for this utility.

options:
  -h, --help  show this help message and exit
```

## INSTALLATION

Arch Linux users can install [pdfcmd from the
AUR](https://aur.archlinux.org/packages/pdfcmd). Python 3.6 or later is
required. Note [pdfcmd is on PyPI](https://pypi.org/project/pdfcmd/) so
just ensure that [`pipx`](https://pypa.github.io/pipx/) is installed
then type the following:

```
$ pipx install pdfcmd
```

To upgrade:

```
$ pipx upgrade pdfcmd
```

## LICENSE

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
