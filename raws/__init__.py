#!/usr/bin/env python
# coding: utf-8

__author__ = 'Sophie Kirschner'
__license__ = 'zlib/libpng'
__email__ = 'sophiek@pineapplemachine.com'
__version__ = '1.0.2'



'''

The raws package provides querying and modification functionality for Dwarf Fortress raws.

raws.dir: An entire directory of raws files, stored as a dictionary of files.
raws.token: A single token within a raws file, for example [CREATURE:DWARF] or [INORGANIC:IRON].
raws.tokenlist: Extends Python's inbuilt list class with additional, specialized functionality.
raws.queryable: Many raws classes extend this class, which provides token querying functionality.
raws.queryableobj: An extension of the queryable class which adds methods optimized for finding object tokens, like the [CREATURE:DWARF] token which is underneath [OBJECT:CREATURE] in the creature_standard file.
raws.tokenfilter: Used by queryable objects' query method to find tokens meeting specific conditions.
raws.boolfilter: Can be used in place of a tokenfilter for operations like Filter A OR Filter B.
raws.color: Contains a convenience class and objects for dealing with colors in the DF raws.
raws.copytree: A general utility method for copying an entire directory and its contents from one location to another.
raws.objecs: Contains information and helper functions for knowing which object types belong to which headers, such as how [BUILDING_WORKSHOP:ID] belongs to [OBJECT:BUILDING].

raws.rawfile: A single raws file, stored as a linked list.
raws.reffile: A file stored as a reference to a source file.
raws.binfile: A file stored in a string, as its binary content.
raws.basefile: A base class which other file types inherit from.

raws.filter: A convenience alias for raws.tokenfilter.
raws.parse: A convenience alias for raws.token.parse, which accepts an input string and parses it into a token or tokenlist.

'''



import queryable, queryableobj, queryableadd
import token
import basefile, reffile, binfile, rawfile
import filefactory
import tokenlist
import tokenparse
import dir
import filters

import copytree
import objects
import color

basefilter = filters.basefilter
tokenfilter = filters.tokenfilter
boolfilter = filters.boolfilter
queryable = queryable.queryable
queryableobj = queryableobj.queryableobj
queryableadd = queryableadd.queryableadd
tokenlist = tokenlist.tokenlist
token = token.token
filefactory = filefactory.filefactory
basefile = basefile.basefile
reffile = reffile.reffile
binfile = binfile.binfile
rawfile = rawfile.rawfile
dir = dir.dir
copytree = copytree.copytree
parseplural = tokenparse.parseplural
parsesingular = tokenparse.parsesingular
parsevariable = tokenparse.parsevariable

filter = tokenfilter
parse = parsevariable
