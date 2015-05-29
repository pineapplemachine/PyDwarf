from queryable import rawsqueryable
from token import rawstoken

class rawsfile(rawsqueryable):
    '''Represents a single file within a raws directory.'''
    
    def __init__(self, header=None, data=None, path=None, tokens=None, rfile=None, dir=None):
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
        if self.data:
            tokens = rawstoken.parse(self.data, implicit_braces=False)
        if tokens:
            self.settokens(tokens)
            
    def settokens(self, tokens):
        self.roottoken, self.tailtoken = rawstoken.firstandlast(tokens)
        
    def copy(self):
        rfile = rawsfile(header=self.header, path=self.path, dir=self.dir)
        rfile.settokens(rawstoken.copy(self.tokens()))
        return rfile
        
    def __str__(self):
        return '%s\n%s' %(self.header, ''.join([str(o) for o in self.tokens()]))
    def __repr__(self):
        return '%s\n%s' %(self.header, ''.join([repr(o) for o in self.tokens()]))
        
    def root(self):
        '''Gets the first token in the file.'''
        while self.roottoken and self.roottoken.prev: self.roottoken = self.roottoken.prev
        return self.roottoken
    def tail(self):
        '''Gets the last token in the file.'''
        while self.tailtoken and self.tailtoken.next: self.tailtoken = self.tailtoken.next
        return self.tailtoken
        
    def tokens(self, range=None, include_self=False, reverse=False):
        '''Iterate through all tokens.'''
        if include_self: raise ValueError
        count = 0
        itrtoken = self.tail() if reverse else self.root()
        while itrtoken and (range is None or range > count):
            yield itrtoken
            itrtoken = itrtoken.prev if reverse else itrtoken.next
            count += 1
            
    def read(self, rfile):
        self.header, self.data = rfile.readline().strip(), rfile.read()
    def write(self, rfile):
        rfile.write(self.__repr__())
    
    def add(self, auto=None, pretty=None, token=None, tokens=None, **kwargs):
        tail = self.tail()
        if tail:
            return tail.add(auto=auto, pretty=pretty, token=token, tokens=tokens, **kwargs)
        else:
            pretty, token, tokens = rawstoken.auto(auto, pretty, token, tokens)
            if pretty:
                tokens = rawstoken.parse(pretty)
                if len(tokens) == 1: token = tokens[0]
            if token:
                self.roottoken = token
                self.tailtoken = token
                return token
            elif tokens:
                self.settokens(tokens)
                return tokens
                
    def remove(self):
        self.dir.removefile(rfile=self)
