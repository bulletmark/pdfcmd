#!/usr/bin/python3
'Concaternate selected pages of one or more PDF files into a single file.'
# Author: Mark Blakeney, Dec 2019.
import os
import re
import sys
import string
import argparse
import PyPDF2
from pathlib import Path

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

You can also assign a single upper case "handle" to a file at first use
and then use that handle later as shorthand. For example, output the
first page from document1.pdf, the first page of document2.pdf, then
the remaining pages from document1.pdf and document2.pdf:

  $prog cat -o output.pdf A=document1.pdf 0 B=document2.pdf 0 A 1: B 1:

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

def init(parser):
    'Called to add arguments to parser at init'
    parser.add_argument('-o', '--outfile', default='-',
            help='output file, default = stdout')
    parser.add_argument('-H', '--helppage', action='store_true',
            help='print help page describing page range/slice syntax')
    # Need to parse remaining args ourself because of ranges starting with '-'
    parser.add_argument('fileranges', nargs=argparse.REMAINDER,
            help='Sequence of alternating file names and page ranges (see -H)')

def main(parser, args):
    'Called to action this command'
    if args.helppage:
        prog = Path(sys.argv[0]).stem
        print(__doc__ + HELP.safe_substitute(prog=prog))
        sys.exit()

    if not args.fileranges:
        parser.error('Must specify at least one input file')

    handles = {}
    merger = PyPDF2.PdfFileMerger()
    for fname, pages in PyPDF2.parse_filename_page_ranges(args.fileranges):
        if re.search('^[A-Z]=.', fname):
            handle = fname[0]
            fname = fname[2:]
            handles[handle] = fname
        else:
            fname = handles.get(fname, fname)

        if not Path(fname).exists():
            sys.exit('File "{}" does not exist.'.format(fname))

        merger.append(fname, pages=pages)

    merger.write(os.fdopen(sys.stdout.fileno(), 'wb') if args.outfile ==
            '-' else args.outfile)
