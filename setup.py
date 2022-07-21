#!/usr/bin/python3
# Setup script to install this package.
# M.Blakeney, Mar 2018.

from pathlib import Path
from setuptools import setup

name = 'pdfcmd'
module = name.replace('-', '_')
here = Path(__file__).resolve().parent

setup(
    name=name,
    version='1.2',
    description='Utility to perform commands on PDF files',
    long_description=here.joinpath('README.md').read_text(),
    long_description_content_type='text/markdown',
    url=f'https://github.com/bulletmark/{name}',
    author='Mark Blakeney',
    author_email='mark.blakeney@bullet-systems.net',
    keywords='PDF',
    license='GPLv3',
    packages=[module] + [str(d) for d in Path(module).iterdir() if d.is_dir()
                and not d.name.startswith('_')],
    python_requires='>=3.5',
    install_requires=['pypdf2>=2.0.0'],
    classifiers=[
        'Programming Language :: Python :: 3',
    ],
    data_files=[
        (f'share/{name}', ['README.md']),
    ],
    entry_points={
        'console_scripts': [f'{name}={module}:{module}.main'],
    }
)
