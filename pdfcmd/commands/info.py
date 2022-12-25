#!/usr/bin/python3
'Show PDF document information.'
# Author: Mark Blakeney, Dec 2019.
import argparse
import pypdf

def init(parser):
    'Called to add arguments to parser at init'
    parser.add_argument('file', help='PDF file', type=argparse.FileType('rb'))

def main(args):
    'Called to action this command'
    inf = pypdf.PdfReader(args.file).metadata
    for key, val in inf.items():
        if key.startswith('/'):
            key = key[1:]
        print(f'{key}: {val}')
