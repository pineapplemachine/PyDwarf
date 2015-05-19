# Imports all scripts in this directory

__all__ = []
loaded = {}

import pkgutil
import inspect

for loader, name, is_pkg in pkgutil.walk_packages(__path__):
    module = loader.find_module(name).load_module(name)

    for name, value in inspect.getmembers(module):
        if not name.startswith('__'):
            loaded[name] = value
            __all__.append(name)
