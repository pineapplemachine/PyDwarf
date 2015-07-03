# Imports all scripts in this directory

import sys
sys.path.append('../')

import os
import imp
import pydwarf

__all__ = []

for root, dirs, files in os.walk(os.path.dirname(os.path.realpath(__file__))):
    for filename in files:
        path = os.path.join(root, filename)
        modulename = '.'.join(os.path.basename(filename).split('.')[1:-1])
        if filename.endswith('.py') and filename.startswith('pydwarf.'):
            try:
                with open(path, 'U') as modulefile:
                    module = imp.load_module(modulename, modulefile, path, ('.py', 'U', imp.PY_SOURCE))
                    globals()[modulename] = module
                    __all__.append(modulename)
            except:
                pydwarf.log.exception('Failed to load script from %s' % path)
