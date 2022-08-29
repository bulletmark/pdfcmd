#!/usr/bin/python3
'Utility to perform commands on PDF files.'
# Author: Mark Blakeney, Dec 2019.

import sys
import argparse
import importlib
from pathlib import Path

def import_path(path):
    'Import given module path'
    modname = path.stem.replace('-', '_')
    spec = importlib.util.spec_from_loader(modname,
            importlib.machinery.SourceFileLoader(modname, str(path)))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def main():
    'Main code'
    mainparser = argparse.ArgumentParser(description=__doc__)
    subparser = mainparser.add_subparsers(title='Commands',
            dest='func')

    # Iterate over the commands to set up their parsers
    for modfile in (Path(__file__).parent / 'commands').glob('[!_]*.py'):
        mod = import_path(modfile)
        docstr = mod.__doc__.strip() if mod.__doc__ else None
        parser = subparser.add_parser(modfile.stem, description=docstr,
                formatter_class=argparse.RawDescriptionHelpFormatter,
                help=docstr)

        # Add reference to mainparser in case subcommand needs it
        parser._mainparser = mainparser

        if hasattr(mod, 'init'):
            mod.init(parser)
        if not hasattr(mod, 'main'):
            mainparser.error(f'"{modfile.stem}" command must define a main()')

        parser.set_defaults(func=mod.main, parser=parser)

    args = mainparser.parse_args()

    if not args.func:
        mainparser.print_help()
        return

    # Run the command that the user specified
    args.func(args)

if __name__ == '__main__':
    sys.exit(main())
