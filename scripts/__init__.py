# Imports all scripts in this directory

import sys
sys.path.append('../')

import pydwarf

__all__ = []

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    try:
        pydwarf.log.debug('Loading script %s...' % name)
        module = loader.find_module(name).load_module(name)
        globals()[name] = module
        __all__.append(name)
        # for name, value in inspect.getmembers(module):
        #     if not name.startswith('__'): __all__.append(name)
    except:
        pydwarf.log.exception('Failed to load script %s' % name)
