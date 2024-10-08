#!/usr/bin/python3
'Output list of page labels/numbers, or total number of pages.'
# Author: Mark Blakeney, Dec 2019.
from __future__ import annotations

import sys
from argparse import ArgumentParser, FileType, Namespace
from typing import Any

import pypdf

def init(parser: ArgumentParser) -> None:
    'Called to add arguments to parser at init'
    parser.add_argument('file', help='PDF file', type=FileType('rb'))
    parser.add_argument('-c', '--count', action='store_true',
            help='just print the total count of pages')

def int_to_page_alpha(pageno: int, base: str) -> str:
    (div, mod) = divmod(pageno - 1, 26)
    c = chr(mod + ord(base))
    return c * (div + 1)

def int_to_roman(input: int) -> str:
    if not isinstance(input, int):
        raise TypeError(f'expected integer, got {type(input)}')
    if not 0 < input < 4000:
        raise ValueError('Argument must be between 1 and 3999')
    ints = (1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1)
    nums = ('M', 'CM', 'D', 'CD', 'C', 'XC', 'L', 'XL', 'X', 'IX', 'V',
            'IV', 'I')
    result = []
    for i in range(len(ints)):
        count = int(input / ints[i])
        result.append(nums[i] * count)
        input -= ints[i] * count
    return ''.join(result)

def getpages(pdf: Any) -> Any:
    'Generate a list of page labels'
    try:
        nums = pdf.trailer['/Root']['/PageLabels']['/Nums']
    except Exception:
        return range(1, len(pdf.pages) + 1)

    # At this point we have either the object or the list.
    # Make it a list.
    if not isinstance(nums, list):
        nums = [nums]

    labels = []
    style = None
    # default
    style = '/D'
    prefix = ''
    next_pageno = 1
    for i in range(0, pdf.getNumPages()):
        if len(nums) > 0 and i >= nums[0]:
            nums.pop(0)  # discard index
            pnle = nums.pop(0)
            style = pnle.get('/S', '/D')
            prefix = pnle.get('/P', '')
            next_pageno = pnle.get('/St', 1)
        if style == '/D':
            pageno_str = str(next_pageno)
        elif style == '/A':
            pageno_str = int_to_page_alpha(next_pageno, 'A')
        elif style == '/a':
            pageno_str = int_to_page_alpha(next_pageno, 'a')
        elif style == '/R':
            pageno_str = int_to_roman(next_pageno)
        elif style == '/r':
            pageno_str = int_to_roman(next_pageno).lower()
        else:
            raise Exception('Malformed PDF: unkown page numbering style '
                            + style)
        labels.append(prefix or pageno_str)
        next_pageno += 1

    return labels

def main(args: Namespace) -> str | None:
    'Called to action this command'
    pdf = pypdf.PdfReader(args.file)
    if args.count:
        print(len(pdf.pages))
        sys.exit()
    for page in getpages(pdf):
        print(page)
