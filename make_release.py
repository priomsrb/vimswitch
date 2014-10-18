#!/usr/bin/env python

from scripts.pack import pack

if __name__ == '__main__':
    # Create the `vimswitch` executable inside the `release` folder.
    # The executable will only contain the vimswitch application code i.e. the
    # test code will not be included.

    sources = [
        '__main__.py',
        'vimswitch/*.py'
    ]

    pack(sources, 'release/vimswitch')
