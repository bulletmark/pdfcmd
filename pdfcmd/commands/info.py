#!/usr/bin/python3
'Show PDF document information.'
# Author: Mark Blakeney, Dec 2019.
from __future__ import annotations

from argparse import ArgumentParser, FileType, Namespace

import pypdf

def init(parser: ArgumentParser) -> None:
    'Called to add arguments to parser at init'
    parser.add_argument('file', help='PDF file', type=FileType('rb'))

def main(args: Namespace) -> str | None:
    'Called to action this command'
    if inf := pypdf.PdfReader(args.file).metadata:
        for key, val in inf.items():
            if key.startswith('/'):
                key = key[1:]
            print(f'{key}: {val}')
