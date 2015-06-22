from queryable import rawsqueryableobj, rawstokenlist
from token import rawstoken

class rawsfile(rawsqueryableobj):
    '''Represents a single file within a raws directory.'''
    
    def __init__(self, header=None, data=None, path=None, tokens=None, rfile=None, dir=None):
        '''Constructs a new raws file object.
        
        header: The header string to appear at the top of the file. Also used to determine filename.
        data: A string to be parsed into token data.
        path: A path to the file from which this object is being parsed, if any exists.
        tokens: An iterable of tokens from which to construct the object; these tokens will be its initial contents.
        rfile: A file-like object from which to automatically read the header and data attributes.
        dir: Which raws.dir object this file belongs to.
        '''
        if rfile:
            self.read(rfile)
            if header is not None: self.header = header
            if data is not None: self.data = data
        else:
            self.header = header
            self.data = data
        self.path = path
        self.roottoken = None
        self.tailtoken = None
        self.dir = dir
        if self.data is not None:
            tokens = rawstoken.parse(self.data, implicit_braces=False, file=self)
            self.settokens(tokens, setfile=False)
        elif tokens is not None:
            self.settokens(tokens, setfile=True)
    
    def index(self, index):
        itrtoken = self.root() if index >= 0 else self.tail()
        index += (index < 0)
        for i in xrange(0, abs(index)):
            itrtoken = itrtoken.next if index > 0 else itrtoken.prev
            if itrtoken is None: return None
        return itrtoken
        
    def getpath(self):
        return self.path
    def setpath(self, path):
        self.path = path
        
    def getheader(self):
        '''Get the file header.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> creature_standard = dwarf.file
            >>> print creature_standard.getheader()
            creature_standard
            >>> creature_standard.setheader('example_header')
            >>> print creature_standard.getheader()
            example_header
        '''
        return self.header
    def setheader(self, header):
        '''Set the file header.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> creature_standard = dwarf.file
            >>> print creature_standard.getheader()
            creature_standard
            >>> creature_standard.setheader('example_header')
            >>> print creature_standard.getheader()
            example_header
        '''
        self.header = header
            
    def settokens(self, tokens, setfile=True):
        '''Internal: Utility method for setting the root and tail tokens given an iterable.'''
        self.roottoken, self.tailtoken = rawstoken.firstandlast(tokens, self if setfile else None)
    
    def copy(self):
        '''Makes a copy of a file and its contents.
        
        Example usage:
            >>> item_food = df.getfile('item_food')
            >>> food_copy = item_food.copy()
            >>> print item_food is food_copy
            False
            >>> print item_food == food_copy
            True
            >>> food_copy.add('EXAMPLE:TOKEN')
            [EXAMPLE:TOKEN]
            >>> print food_copy.list()
            [OBJECT:ITEM]
            [ITEM_FOOD:ITEM_FOOD_BISCUITS]
            [NAME:biscuits]
            [LEVEL:2]
            [ITEM_FOOD:ITEM_FOOD_STEW]
            [NAME:stew]
            [LEVEL:3]
            [ITEM_FOOD:ITEM_FOOD_ROAST]
            [NAME:roast]
            [LEVEL:4][EXAMPLE:TOKEN]
            >>> print item_food == food_copy
            False
        '''
        rfile = rawsfile(header=self.header, path=self.path, dir=self.dir)
        rfile.settokens(rawstoken.copy(self.tokens()))
        return rfile
        
    def equals(self, other):
        return rawstoken.tokensequal(self.tokens(), other.tokens())
        
    def __eq__(self, other):
        return self.equals(other)
    def __ne__(self, other):
        return not self.equals(other)
        
    def __len__(self):
        return self.length()
        
    def __str__(self):
        return self.header
    def __repr__(self):
        return '%s\n%s' %(self.header, ''.join([repr(o) for o in self.tokens()]))
        
    def root(self):
        '''Gets the first token in the file.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> print creature_standard.root()
            [OBJECT:CREATURE]
        '''
        while self.roottoken is not None and self.roottoken.prev is not None: self.roottoken = self.roottoken.prev
        return self.roottoken
    def tail(self):
        '''Gets the last token in the file.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> print creature_standard.tail()
            [MULTIPLY_VALUE:15]
        '''
        while self.tailtoken is not None and self.tailtoken.next is not None: self.tailtoken = self.tailtoken.next
        return self.tailtoken
        
    def tokens(self, reverse=False, **kwargs):
        '''Iterate through all tokens.
        
        reverse: If False, starts from the first token and iterates forwards. If True,
            starts from the last token and iterates backwards. Defaults to False.
        **kwargs: Other named arguments are passed on to the raws.token.tokens method.
        '''
        if reverse:
            tail = self.tail()
            if tail is None: return
            generator = tail.tokens(include_self=True, reverse=True, **kwargs)
        else:
            root = self.root()
            if root is None: return
            generator = root.tokens(include_self=True, **kwargs)
        for token in generator:
            yield token
            
    def read(self, rfile):
        '''Internal: Given a file-like object, reads header and data from it.'''
        self.header, self.data = rfile.readline().strip(), rfile.read()
    def write(self, rfile):
        '''Internal: Given a file-like object, writes the file's contents to that file.'''
        rfile.write(self.__repr__())
    
    def add(self, auto=None, pretty=None, token=None, tokens=None, **kwargs):
        '''Adds tokens to the end of a file.
        
        Example usage:
            >>> item_food = df.getfile('item_food')
            >>> print item_food.list()
            [OBJECT:ITEM]
            [ITEM_FOOD:ITEM_FOOD_BISCUITS]
            [NAME:biscuits]
            [LEVEL:2]
            [ITEM_FOOD:ITEM_FOOD_STEW]
            [NAME:stew]
            [LEVEL:3]
            [ITEM_FOOD:ITEM_FOOD_ROAST]
            [NAME:roast]
            [LEVEL:4]
            >>> tokens = item_food.add('\nhi! [THIS][IS][AN][EXAMPLE]')
            >>> print tokens
            hi! [THIS][IS][AN][EXAMPLE]
            >>> print item_food.list()
            [OBJECT:ITEM]
            [ITEM_FOOD:ITEM_FOOD_BISCUITS]
            [NAME:biscuits]
            [LEVEL:2]
            [ITEM_FOOD:ITEM_FOOD_STEW]
            [NAME:stew]
            [LEVEL:3]
            [ITEM_FOOD:ITEM_FOOD_ROAST]
            [NAME:roast]
            [LEVEL:4]
            hi! [THIS][IS][AN][EXAMPLE]
        '''
        tail = self.tail()
        if tail:
            return tail.add(auto=auto, pretty=pretty, token=token, tokens=tokens, **kwargs)
        else:
            pretty, token, tokens = rawstoken.auto(auto, pretty, token, tokens)
            if pretty is not None:
                tokens = rawstoken.parse(pretty)
                if len(tokens) == 1: token = tokens[0]
            if token is not None:
                self.roottoken = token
                self.tailtoken = token
                token.file = self
                return token
            elif tokens is not None:
                self.settokens(tokens)
                return tokens
                
    def remove(self):
        '''Remove this file from the raws.dir object to which it belongs.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> print dwarf
            [CREATURE:DWARF]
            >>> print dwarf.file
            creature_standard
            >>> dwarf.file.remove()
            >>> print df.getobj('CREATURE:DWARF')
            None
            >>> print df.getfile('creature_standard')
            None
        '''
        self.dir.removefile(rfile=self)
        
    def length(self):
        '''Get the number of tokens in this file.
        
        Example usage:
            >>> print df.getfile('creature_standard').length()
            5516
            >>> print df.getfile('inorganic_metal').length()
            1022
            >>> print df.getfile('item_pants').length()
            109
        '''
        count = 0
        for token in self.tokens(): count += 1
        return count
        
    def clear(self):
        '''Remove all tokens from this file.
        
        Example usage:
            >>> item_pants = df.getfile('item_pants')
            >>> print item_pants.length()
            109
            >>> item_pants.clear()
            >>> print item_pants.length()
            0
        '''
        for token in self.tokens():
            token.file = None
        self.roottoken = None
        self.tailtoken = None
        
    def getobjheaders(self, type):
        root = self.root()
        if root is not None and root.value == 'OBJECT' and root.nargs() == 1 and root.args[0] in match_types:
            return (root,)
        return tuple()
