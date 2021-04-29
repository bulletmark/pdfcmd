#!/usr/bin/python3
'Show PDF document information.'
# Author: Mark Blakeney, Dec 2019.
import argparse
import PyPDF2

def init(parser):
    'Called to add arguments to parser at init'
    parser.add_argument('file', help='PDF file', type=argparse.FileType('rb'))

def main(parser, args):
    'Called to action this command'
    inf = PyPDF2.PdfFileReader(args.file).getDocumentInfo()
    for key, val in inf.items():
        if key.startswith('/'):
            key = key[1:]
        print('{}: {}'.format(key, val))
