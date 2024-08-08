#!/usr/bin/python3
'Show help/usage for this utility.'
from __future__ import annotations

from argparse import Namespace

def main(args: Namespace) -> str | None:
    args.parser._mainparser.print_help()
