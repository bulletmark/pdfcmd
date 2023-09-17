#!/usr/bin/python3
'Utility to perform commands on PDF files.'
# Author: Mark Blakeney, Dec 2019.

import sys
import argparse
import importlib
from pathlib import Path

def main():
    'Main code'
    mainparser = argparse.ArgumentParser(description=__doc__)
    subparser = mainparser.add_subparsers(title='Commands',
            dest='func')

    # Iterate over the commands to set up their parsers
    prog = Path(__file__)
    for modfile in sorted((prog.parent / 'commands').glob('[!_]*.py')):
        name = modfile.stem
        mod = importlib.import_module(f'{prog.stem}.commands.{name}')
        docstr = mod.__doc__.strip().split('\n\n')[0] if mod.__doc__ else None
        parser = subparser.add_parser(name, description=mod.__doc__,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                help=docstr)

        # Add reference to mainparser in case subcommand needs it
        parser._mainparser = mainparser

        if hasattr(mod, 'init'):
            mod.init(parser)
        if not hasattr(mod, 'main'):
            mainparser.error(f'"{name}" command must define a main()')

        parser.set_defaults(func=mod.main, parser=parser)

    args = mainparser.parse_args()

    if not args.func:
        mainparser.print_help()
        return

    # Run the command that the user specified
    return args.func(args)

if __name__ == '__main__':
    sys.exit(main())
