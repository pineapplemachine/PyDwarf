import itertools
from queryable import rawsqueryable
from filters import rawstokenfilter

class rawstoken(rawsqueryable):
    
    auto_arg_docstring = '''
        auto: When the first argument is specified the intended assignment will be
            detected automatically. If a rawstoken is specified it will be treated
            as a token argument. If a string, pretty. If anything else, tokens.'''
    
    @staticmethod
    def auto(auto, pretty, token, tokens):
        # Convenience function for handling method arguments
        if auto is not None:
            if isinstance(auto, basestring): pretty = auto
            elif isinstance(auto, rawstoken): token = auto
            elif isinstance(auto, rawsqueryable): tokens = auto.tokens()
            else: tokens = auto
        return pretty, token, tokens
        
    def __init__(self, auto=None, pretty=None, token=None, value=None, args=None, prefix=None, suffix=None, prev=None, next=None, file=None):
        '''Constructs a token object.
        
        %s (However, a tokens argument is illegal here and attempting to create
        a rawstoken using one will cause an exception.)
        pretty: Parses the token's text from a string. A string without opening
            and closing braces is considered to have them implicitly.
        token: Copies this token's attributes from another.
        value: The leftmost string between a token's brackets, where strings are
            delimited by colons.
        args: All except the leftmost string between a token's brackets.
        prefix: Comment or formatting text preceding a token.
        suffix: Comment or formatting text following a token.
        prev: The previous token.
        next: The following token.
        ''' % rawstoken.auto_arg_docstring
        
        pretty, token, tokens = rawstoken.auto(auto, pretty, token, None)
        if tokens is not None: raise ValueError
        if pretty:
            token = rawstoken.parseone(pretty, implicit_braces=True)
        if token:
            value = token.value
            args = list(token.args) if token.args else []
            prefix = token.prefix
            suffix = token.suffix
        # tokens look like this: [value:arg1:arg2:...:argn]
        self.prev = prev            # previous token sequentially
        self.next = next            # next token sequentially
        self.value = value          # value for the token
        self.args = args            # arguments for the token
        self.prefix = prefix        # non-token text between the preceding token and this one
        self.suffix = suffix        # between this token and the next/eof (should typically apply to eof)
        self.removed = False        # keeps track of whether this token has been removed yet
        self.file = None            # parent rawsfile object
        if not self.args: self.args = []
    
    def nargs(self, count=None):
        '''When count is None, returns the number of arguments the token has. (Length of
        arguments list.) Otherwise, returns True if the number of arguments is equal to the
        given count and False if not.'''
        return len(self.args) if (count is None) else (len(self.args) == count)
    def getarg(self, index):
        '''Gets argument at index, returns None if the index is out of bounds.'''
        return self.args[index] if index >= 0 and index < len(self.args) else None
    def setarg(self, index, value):
        '''Sets argument at index, also verifies that the input contains no illegal characters.'''
        if any([char in str(value) for char in '[]:\'']): raise ValueError
        self.args[index] = value
    def argsstr(self):
        '''Return arguments joined by ':'.'''
        return ':'.join([str(a) for a in self.args])
        
    def arg(self):
        '''When a token is expected to have only one argument, this method can be used
        to access it. It there's one argument it will be returned, otherwise an
        exception will be raised.'''
        if len(self.args) == 1:
            return self.args[0]
        else:
            raise ValueError
        
    def __hash__(self): # Not that this class is immutable, just means you'll need to be careful about when you're using token hashes
        return hash('%s:%s' % (self.value, self.argsstr()) if self.nargs() else self.value)
    
    def __str__(self):
        return '[%s%s]' %(self.value, (':%s' % self.argsstr()) if self.args and len(self.args) else '')
    def __repr__(self):
        return '%s%s%s' % (self.prefix if self.prefix else '', str(self), self.suffix if self.suffix else '')
    def __eq__(self, other):
        return self.equals(other)
    def __ne__(self, other):
        return not self.equals(other)
        
    def equals(self, other):
        '''Returns True if two tokens have identical values and arguments, False otherwise.'''
        return other is not None and self.value == other.value and self.nargs() == other.nargs() and all([str(self.args[i]) == str(other.args[i]) for i in xrange(0, self.nargs())])
        
    @staticmethod
    def tokensequal(atokens, btokens):
        '''Determine whether two iterables containing tokens contain equivalent tokens.'''
        for atoken, btoken in itertools.izip(atokens, btokens):
            if not atoken.equals(btoken): return False
        return True
    
    @staticmethod
    def copy(auto=None, token=None, tokens=None):
        '''Copies some token or iterable collection of tokens.'''
        pretty, token, tokens = rawstoken.auto(auto, None, token, tokens)
        if token:
            return rawstoken(token=token)
        elif tokens:
            copied = []
            prevtoken = None
            for token in tokens:
                newtoken = rawstoken(token=token)
                copied.append(newtoken)
                newtoken.prev = prevtoken
                if prevtoken: prevtoken.next = newtoken
                prevtoken = newtoken
            return copied
        else:
            raise ValueError
        
    def tokens(self, range=None, include_self=False, reverse=False, until_token=None):
        count = 0
        itertoken = self if include_self else (self.prev if reverse else self.next)
        while itertoken and (range is None or range > count) and (itertoken != until_token):
            yield itertoken
            itertoken = itertoken.prev if reverse else itertoken.next
            count += 1
            
    @staticmethod   
    def iter(root, tail):
        '''Iterate through tokens starting with root and ending at tail.'''
        itertoken = root
        while itertoken is not None and itertoken != tail:
            yield itertoken
            itertoken = itertoken.next
            
    def match(self, pretty=None, **kwargs):
        '''Returns True if this method matches some rawstokenfilter, false otherwise.'''
        return rawstokenfilter(pretty=pretty, **kwargs).match(self)
        
    def add(self, auto=None, pretty=None, token=None, tokens=None, reverse=False):
        '''Adds a token or tokens nearby this one. If reverse is False the token 
        or tokens are added immediately after. If it's True, they are added before.
        
        %s
        pretty: Parses the string and adds the tokens within it.
        token: Adds this one token.
        tokens: Adds all of these tokens.
        ''' % rawstoken.auto_arg_docstring
        pretty, token, tokens = rawstoken.auto(auto, pretty, token, tokens)
        if pretty:
            return self.addall(rawstoken.parse(pretty), reverse)
        elif tokens:
            return self.addall(tokens, reverse)
        elif token:
            return self.addone(token, reverse)
        else:
            raise ValueError
            
    def addprop(self, auto=None, **kwargs):
        '''When this token is an object token like CREATURE:X or INORGANIC:X, a
        new token is usually added immediately afterwards. However, if a token like
        COPY_TAGS_FROM or USE_MATERIAL_TEMPLATE exists underneath the object, then
        the specified tag is only added after that.'''
        
        addafter = self.getlastprop(value_in=('COPY_TAGS_FROM', 'USE_MATERIAL_TEMPLATE'))
        if not addafter: addafter = self
        addafter.add(auto=auto, **kwargs)
    
    @staticmethod
    def firstandlast(tokens):
        # Utility method for getting the first and last items of some iterable
        try:
            return tokens[0], tokens[-1]
        except:
            first, last = None, None
            for token in tokens:
                if first is not None: first = token
                last = token
            return first, last            
        
    def addone(self, token, reverse=False):
        # Utility method called by add when adding a single token
        if reverse:
            token.next = self
            token.prev = self.prev
            if self.prev: self.prev.next = token
            self.prev = token
        else:
            token.prev = self
            token.next = self.next
            if self.next: self.next.prev = token
            self.next = token
        return token
    def addall(self, tokens, reverse=False):
        # Utility method called by add when adding multiple tokens
        first, last = rawstoken.firstandlast(tokens)
        if reverse:
            last.next = self
            first.prev = self.prev
            if self.prev: self.prev.next = first
            self.prev = last
        else:
            first.prev = self
            last.next = self.next
            if self.next: self.next.prev = tokens[-1]
            self.next = first
        return tokens
    
    def remove(self, count=0, reverse=False):
        '''Removes this token and the next count tokens in the direction indicated by reverse.'''
        if not self.removed:
            left = self.prev
            right = self.next
            if count:
                token = self.prev if reverse else self.next
                while count and token:
                    count -= 1
                    token.removed = True
                    token = token.prev if reverse else token.next
                if reverse:
                    left = token
                else:
                    right = token
            if left: left.next = right
            if right: right.prev = left
            self.removed = True
        return self
    
    @staticmethod
    def parse(data, implicit_braces=True, **kwargs):
        '''Parses a string, turns it into a list of tokens.

        data: The string to be parsed.
        implicit_braces: Determines behavior when there are no opening or closing braces.
            If True, then the input is assumed to be the contents of a token, e.g. [input].
            If False, an exception is raised.
        **kwargs: Extra named arguments are passed to the constructor each time a new
            rawstoken is distinguished and created.
        '''

        tokens = [] # maintain a sequential list of tokens
        pos = 0     # byte position in data
        if data.find('[') == -1 and data.find(']') == -1:
            if implicit_braces:
                tokenparts = data.split(':')
                token = rawstoken(
                    value=tokenparts[0],
                    args=tokenparts[1:],
                    **kwargs
                )
                return [token]
            else:
                raise ValueError
        else:
            while pos < len(data):
                token = None
                open = data.find('[', pos)
                if open >= 0 and open < len(data):
                    close = data.find(']', pos)
                    if close >= 0 and close < len(data):
                        prefix = data[pos:open]
                        tokentext = data[open+1:close]
                        tokenparts = tokentext.split(':')
                        token = rawstoken(
                            value=tokenparts[0],
                            args=tokenparts[1:],
                            prefix=prefix,
                            prev=tokens[-1] if len(tokens) else None,
                            **kwargs
                        )
                        pos = close+1
                if token:
                    if len(tokens): tokens[-1].next = token
                    tokens.append(token)
                else:
                    break
            if len(tokens) and pos<len(data):
                tokens[-1].suffix = data[pos:]
            return tokens
            
    @staticmethod
    def parseone(*args, **kwargs):
        tokens = rawstoken.parse(*args, **kwargs)
        if len(tokens) != 1: raise ValueError
        return tokens[0]
