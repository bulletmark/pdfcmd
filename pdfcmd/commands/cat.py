#!/usr/bin/python3
'Concaternate selected pages of one or more PDF files into a single file.'
# Author: Mark Blakeney, Dec 2019.
from __future__ import annotations

import os
import re
import string
import sys
from argparse import REMAINDER, ArgumentParser, Namespace
from pathlib import Path

import pypdf

# flake8: noqa: E122
HELP = string.Template(\
'''
Arguments are specified as a sequence of alternating file names and page
ranges:

  file1 pagerange1 file2 pagerange2 ..

Page ranges refer to the previously specified file and are specified in
Python "slice" notation, assuming each page is like an element in a
sequence, starting at 0.

For example, concatenate all of head.pdf, all but page seven of
content.pdf, and the last page of tail.pdf, producing output.pdf:

  $prog cat -o output.pdf head.pdf content.pdf :6 7: tail.pdf -1

A file not followed by a page range means all pages of that file, for
example:

  $prog cat chapter*.pdf >book.pdf

You can also assign a single "alias" character to a file at first use
and then use that alias later as shorthand. For example, output the
first page from document1.pdf, the first page of document2.pdf, then the
remaining pages from document1.pdf and document2.pdf:

  $prog cat -o output.pdf a=document1.pdf 0 b=document2.pdf 0 a 1: b 1:

The alias can be any single lower or upper case letter.

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
''')

def init(parser: ArgumentParser) -> None:
    'Called to add arguments to parser at init'
    parser.add_argument('-o', '--outfile', default='-',
            help='output file, default = stdout')
    parser.add_argument('-a', '--no-aliases', action='store_true',
            help='do not use aliases')
    # Need to parse remaining args ourself because of ranges starting with '-'
    parser.add_argument('fileranges', nargs=REMAINDER,
            help='Sequence of alternating file names and page ranges')

    parser.epilog = HELP.safe_substitute(prog=Path(sys.argv[0]).stem)

def main(args: Namespace) -> str | None:
    'Called to action this command'
    if not args.fileranges:
        args.parser.error('Must specify at least one input file')

    aliases = {}
    merger = pypdf.PdfWriter()
    for fname, pages in pypdf.parse_filename_page_ranges(args.fileranges):
        if re.search('^[A-Za-z]=.', fname) and not args.no_aliases:
            alias = fname[0]
            fname = fname[2:]
            aliases[alias] = fname
        else:
            fname = aliases.get(fname, fname)

        if not Path(fname).exists():
            sys.exit(f'File "{fname}" does not exist.')

        merger.append(fname, pages=pages)

    merger.write(os.fdopen(sys.stdout.fileno(), 'wb') if args.outfile ==
            '-' else args.outfile)
