from filters import rawstokenfilter as tokenfilter
from filters import rawsboolfilter as boolfilter
from queryable import rawsqueryable as queryable
from queryable import rawstokenlist as tokenlist
from token import rawstoken as token
from file import rawsfile as file
from dir import rawsdir as dir
from dir import copytree
import color

filter = tokenfilter

parse = token.parse
parseone = token.parseone

__version__ = '1.0.1'
