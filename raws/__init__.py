#!/usr/bin/env python

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
raws.parse: A convenience alias for raws.token.parse, which accepts an input string and parses it into a tokenlist.
raws.parseone: A convenience alias for raws.token.parseone, which acts like raws.token.parse but expects a single token instead of a list of them.

'''



# TODO: rename classes internally to reflect what they're exported as here e.g. binfile -> binfile
from filters import rawstokenfilter as tokenfilter
from filters import rawsboolfilter as boolfilter
from queryable import rawsqueryable as queryable
from queryableobj import rawsqueryableobj as queryableobj
from tokenlist import tokenlist
from token import token
from filefactory import filefactory
from basefile import basefile
from reffile import reffile
from binfile import binfile
from rawfile import rawfile
from dir import rawsdir as dir
from copytree import copytree
import objects
import color
import docs

filter = tokenfilter
parse = token.parse
parseone = token.parseone
