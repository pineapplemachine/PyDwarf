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



import logger
import response
import helpers
import quick
import urist
import uristscript
import registrar
import session
import config
from version import * # TODO: do this better



timestamp = logger.timestamp
datetimeformat = logger.datetimeformat
stdouthandler = logger.stdouthandler
logfilehandler = logger.logfilehandler
log = logger.log

success = response.success
failure = response.failure
response = response.response

df = quick.df
quick = quick.quick

rel = helpers.rel
findfile = helpers.findfile

urist = urist.urist
uristscript = uristscript.uristscript
registrar = registrar.registrar
session = session.session
config = config.config



script = uristscript

scripts = urist.registrar
