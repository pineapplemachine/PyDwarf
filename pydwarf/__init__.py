#!/usr/bin/env python
# coding: utf-8

__author__ = 'Sophie Kirschner'
__license__ = 'zlib/libpng'
__email__ = 'sophiek@pineapplemachine.com'
__version__ = '1.0.2'



'''

The pydwarf package acts as a layer of abstraction over the raws package, providing functionality for mod management and application.

pydwarf.log: A shared logging object.
pydwarf.version: Utilities pertinent to handling Dwarf Fortress versions.
pydwarf.response: PyDwarf expects plugins to return pydwarf.response objects.
pydwarf.urist: A combined decorator and global repository for PyDwarf plugins.
pydwarf.session: Ideally for use by a mod manager, abstracts the handling and execution of PyDwarf plugins.
pydwarf.config: Provides an object to simplify config loading and application.
pydwarf.helpers: Contains some miscellaneous utility functions.

'''



from log import log
from response import response, failure, success
from urist import urist
from session import session
from config import config
from helpers import rel, findfile
from version import *



def quick(raws, root=None, **kwargs):
    se = session()
    if root is not None: kwargs['root'] = root
    args = {
        'input': 'df',
        'paths': 'auto',
        'version': 'auto',
        'hackversion': 'auto',
        'output': 'output/',
        'backup': None,
        'packages': 'scripts',
        'verbose': True,
        'log': '',
    }
    args.update(kwargs)
    se.load(raws, args=args)
    return se

def df(*args, **kwargs):
    se = quick(*args, **kwargs)
    return se.df
