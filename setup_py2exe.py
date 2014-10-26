from distutils.core import setup
import py2exe

setup(
    console=[{
        'script': '__main__.py',
        'dest_base': 'vimswitch'
    }],
    zipfile=None,
    options={"py2exe" : {
       "includes": ["urllib.request"],
       "excludes": ["doctest", "pdb", "unittest", "difflib", "inspect"],
       "bundle_files": 1,
       "compressed": True,
       "optimize": 2,
       #"dll_excludes": ["MSVCP90.dll"]
    }}
)