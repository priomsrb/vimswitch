import zipfile
import glob
import os
import stat


def pack(sources, output):
    """
    Creates a single file python executable containing the given sources.

    `sources` is a list of filenames or globs. One of the entries must be a
    __main__.py file.

    `output` is the filename that will be given to the executable.

    For example:
        pack(['__main__.py', 'myproject/*.py'], 'myproject'])
    This will create an executable called 'myproject'. This executable can be
    run using:
        ./myproject
    or
        python myproject
    """
    files = _expandGlobs(sources)
    _zipFiles(files, output)
    _addShebang(output)
    _makeExecutable(output)
    fileSize = int(_getFileSize(output) / 1024)
    print('Executable created: %s (%skb)' % (output, fileSize))


def _expandGlobs(globs):
    expandedGlobs = []
    for g in globs:
        expandedGlobs += glob.glob(g)
    return expandedGlobs


def _zipFiles(filenames, output):
    print("Zipping files: ")
    with zipfile.ZipFile(output, 'w', compression=zipfile.ZIP_DEFLATED) as outputZip:
        for filename in filenames:
            print('\t%s' % filename)
            outputZip.write(filename)


def _addShebang(filename):
    """
    Since python 2.6, python is able to execute a zip file if they contain a
    __main__.py file inside it. By adding the python shebang at the top of
    the zip file, python will attempt to execute this file.

    Conveniently, zip files can be prepended with data and still be valid. So
    what we end up with is a self-executing zip file.
    """
    shebang = b'#!/usr/bin/env python'
    print('Adding shebang: %s' % shebang.decode('utf-8'))
    with open(filename, 'rb+') as f:
        previousContent = f.read()
        f.seek(0)
        f.write(shebang)
        f.write(b'\n')
        f.write(previousContent)


def _getFileSize(filename):
    return os.path.getsize(filename)


def _makeExecutable(filename):
    print('Setting executable flag')
    st = os.stat(filename)
    os.chmod(filename, st.st_mode | stat.S_IXUSR | stat.S_IXGRP | stat.S_IXOTH)
