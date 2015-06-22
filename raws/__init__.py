'''

The raws package provides querying and modification functionality for Dwarf Fortress raws.

raws.dir: An entire directory of raws files, stored as a dictionary of files.
raws.dfhack: Possessed by dir objects as a hack attribute, the class exposes methods for interacting with DFHack files.
raws.file: A single raws file, stored as a linked list.
raws.token: A single token within a raws file, for example [CREATURE:DWARF] or [INORGANIC:IRON].
raws.tokenlist: Extends Python's inbuilt list class with additional, specialized functionality.
raws.queryable: Many raws classes extend this class, which provides token querying functionality.
raws.queryableobj: An extension of the queryable class which adds methods optimized for finding object tokens, like the [CREATURE:DWARF] token which is underneath [OBJECT:CREATURE] in the creature_standard file.
raws.tokenfilter: Used by queryable objects' query method to find tokens meeting specific conditions.
raws.boolfilter: Can be used in place of a tokenfilter for operations like Filter A OR Filter B.
raws.color: Contains a convenience class and objects for dealing with colors in the DF raws.
raws.copytree: A general utility method for copying an entire directory and its contents from one location to another.

raws.filter: A convenience alias for raws.tokenfilter.
raws.parse: A convenience alias for raws.token.parse, which accepts an input string and parses it into a tokenlist.
raws.parseone: A convenience alias for raws.token.parseone, which acts like raws.token.parse but expects a single token instead of a list of them.

'''

from filters import rawstokenfilter as tokenfilter
from filters import rawsboolfilter as boolfilter
from queryable import rawsqueryable as queryable
from queryable import rawsqueryableobj as queryableobj
from queryable import rawstokenlist as tokenlist
from token import rawstoken as token
from file import rawsfile as file
from dir import rawsdir as dir
from dfhack import dfhack
from copytree import copytree
import color

filter = tokenfilter

parse = token.parse
parseone = token.parseone

__version__ = '1.0.1'
