import itertools
from queryable import rawsqueryable, rawstokenlist
from filters import rawstokenfilter

class rawstoken(rawsqueryable):
    
    auto_arg_docstring = '''
        auto: When the first argument is specified the intended assignment will be
            detected automatically. If a rawstoken is specified it will be treated
            as a token argument. If a string, pretty. If anything else, tokens.'''
    
    # Don't allow these characters in values or arguments
    illegal_internal_chars = '[]:'
    
    # Don't allow these characters in a token's prefix or suffix
    illegal_external_chars = '['
    
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
        
        Example usage:
            >>> token_a = raws.token('DISPLAY_COLOR:6:0:1')
            >>> print token_a
            [DISPLAY_COLOR:6:0:1]
            >>> token_b = token = raws.token(value='DISPLAY_COLOR', args=['6', '0', '1'])
            >>> print token_b
            [DISPLAY_COLOR:6:0:1]
            >>> print token_a == token_b
            True
            >>> print token_a is token_b
            False
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
        given count and False if not.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:0:1:2:3:4')
            >>> print 'Token has %d arguments.' % token.nargs()
            Token has 5 arguments.
            >>> print token.nargs(2)
            False
            >>> print token.nargs(5)
            True
        '''
        return len(self.args) if (count is None) else (len(self.args) == count)
        
    def getarg(self, index=0):
        '''Gets argument at index, returns None if the index is out of bounds.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:argument 0:argument 1')
            >>> print token.getarg(0)
            argument 0
            >>> print token.getarg(1)
            argument 1
            >>> print token.getarg(2)
            None
            >>> print token.getarg(-1)
            argument 1
            >>> print token.getarg(-2)
            argument 0
            >>> print token.getarg(-3)
            None
        '''
        return self.args[index] if index >= -len(self.args) and index < len(self.args) else None
    def setarg(self, index, value=None):
        '''Sets argument at index, also verifies that the input contains no illegal characters.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> print token
            [EXAMPLE:a:b:c]
            >>> token.setarg(2, 500)
            >>> print token
            [EXAMPLE:a:b:500]
            >>> token.setarg('hi!')
            >>> print token
            [EXAMPLE:hi!:b:500]'''
        if value is None and index is not None: value = index; index = 0
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_internal_chars]): raise ValueError
        self.args[index] = valuestr
    def addarg(self, value):
        '''Appends an argument to the end of the argument list.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token
            [EXAMPLE]
            >>> token.addarg('hi!')
            >>> print token
            [EXAMPLE:hi!]
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_internal_chars]): raise ValueError
        self.args.append(valuestr)
    def argsstr(self):
        '''Return arguments joined by ':'.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> print token.argsstr()
            a:b:c
        '''
        return ':'.join([str(a) for a in self.args])
        
    def getvalue(self):
        '''Get the token's value.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> print token.getvalue()
            EXAMPLE
        '''
        return self.value
    def setvalue(self, value):
        '''Set the token's value.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> token.setvalue('JUST KIDDING')
            >>> print token
            [JUST KIDDING:a:b:c]
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_internal_chars]): raise ValueError
        self.value = value
        
    def getprefix(self):
        '''Get the comment text preceding a token.
        
        Example usage:
            >>> token = raws.token('This is a comment [EXAMPLE] so is this')
            >>> print token
            [EXAMPLE]
            >>> print token.getprefix()
            This is a comment
            >>> print token.getsuffix()
             so is this
        '''
        return self.prefix
    def setprefix(self, value):
        '''Set the comment text preceding a token.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token
            [EXAMPLE]
            >>> token.setprefix('hello ')
            >>> print repr(token)
            hello [EXAMPLE]
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_external_chars]): raise ValueError
        self.prefix = value
        
    def getsuffix(self):
        '''Get the comment text following a token.
        
        Example usage:
            >>> token = raws.token('This is a comment [EXAMPLE] so is this')
            >>> print token
            [EXAMPLE]
            >>> print token.getsuffix()
             so is this
            >>> print token.getprefix()
            This is a comment
        '''
        return self.suffix
    def setsuffix(self, value):
        '''Set the comment text following a token.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token
            [EXAMPLE]
            >>> token.setsuffix(' world')
            >>> print repr(token)
            [EXAMPLE] world
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_external_chars]): raise ValueError
        self.suffix = value
        
    def arg(self):
        '''When a token is expected to have only one argument, this method can be used
        to access it. It there's one argument it will be returned, otherwise an
        exception will be raised.
        
        Example usage:
            >>> token_a = raws.token('EXAMPLE:x')
            >>> token_b = raws.token('EXAMPLE:x:y:z')
            >>> print token_a.arg()
            x
            >>> try:
            ...     print token_b.arg()
            ... except:
            ...     print 'token_b doesn\'t have the correct number of arguments!'
            ...
            token_b doesn't have the correct number of arguments!'''
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
        '''Returns True if two tokens have identical values and arguments, False otherwise.
        
        Example usage:
            >>> token_a = raws.token('EXAMPLE:hi!')
            >>> token_b = raws.token('EXAMPLE:hello there')
            >>> token_c = raws.token('EXAMPLE:hi!')
            >>> print token_a, token_b, token_c
            [EXAMPLE:hi!] [EXAMPLE:hello there] [EXAMPLE:hi!]
            >>> print token_a == token_b
            False
            >>> print token_b == token_c
            False
            >>> print token_c == token_a
            True
            >>> print token_c is token_a
            False'''
        return other is not None and self.value == other.value and self.nargs() == other.nargs() and all([str(self.args[i]) == str(other.args[i]) for i in xrange(0, self.nargs())])
        
    @staticmethod
    def tokensequal(atokens, btokens):
        '''Determine whether two iterables containing tokens contain equivalent tokens.'''
        for atoken, btoken in itertools.izip(atokens, btokens):
            if not atoken.equals(btoken): return False
        return True
    
    @staticmethod
    def copy(auto=None, token=None, tokens=None):
        '''Copies some token or iterable collection of tokens.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> print token
            [EXAMPLE:a:b:c]
            >>> copied_token = raws.token.copy(token)
            >>> print copied_token
            [EXAMPLE:a:b:c]
            >>> print token is copied_token
            False
            >>> tokens = raws.token.parse('[HELLO][WORLD]')
            >>> print tokens
            [HELLO][WORLD]
            >>> print tokens[0]
            [HELLO]
            >>> print tokens[1]
            [WORLD]
            >>> copied_tokens = raws.token.copy(tokens)
            >>> print copied_tokens
            [HELLO][WORLD]
            >>> print tokens == copied_tokens
            True
            >>> print tokens is copied_tokens
            False
        '''
        pretty, token, tokens = rawstoken.auto(auto, None, token, tokens)
        if token:
            return rawstoken(token=token)
        elif tokens:
            copied = rawstokenlist()
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
        '''Iterate through successive tokens starting with this one.
        
        range: If defined as an integer, then iteration stops when this many tokens
            have been iterated over.
        include_self: If True, iteration includes this token. Otherwise, iteration
            starts with the immediately following or preceding token.
        reverse: If False, iteration goes forward through the sequence of tokens. If
            True, it goes backwards.
        until_token: Iteration stops if/when the current token matches this exact
            object.
            
        Example usage:
            >>> tokens = raws.token.parse('[HI][HOW][ARE][YOU][?]')
            >>> first_token = tokens[0]
            >>> last_token = tokens[-1]
            >>> print first_token
            [HI]
            >>> print last_token
            [?]
            >>> print raws.tokenlist(first_token.tokens()) # Construct a raws.tokenlist object using the generator returned by the tokens method
            [HOW][ARE][YOU][?]
            >>> print raws.tokenlist(first_token.tokens(include_self=True))
            [HI][HOW][ARE][YOU][?]
            >>> print raws.tokenlist(first_token.tokens(range=1))
            [HOW]
            >>> print raws.tokenlist(first_token.tokens(until_token=tokens[3]))
            [HOW][ARE]
            >>> print raws.tokenlist(last_token.tokens(reverse=True))
            [YOU][ARE][HOW][HI]
        '''
        count = 0
        itertoken = self if include_self else (self.prev if reverse else self.next)
        while itertoken and (range is None or range > count) and (itertoken is not until_token):
            yield itertoken
            itertoken = itertoken.prev if reverse else itertoken.next
            count += 1
            
    @staticmethod   
    def iter(root, tail):
        '''Iterate through tokens starting with root and ending at tail.
        
        Example usage:
            >>> tokens = raws.token.parse('[HI][HOW][ARE][YOU][?]')
            >>> print raws.tokenlist(raws.token.iter(tokens[1], tokens[3]))
            [HOW][ARE][YOU]
        '''
        itertoken = root
        while itertoken is not None and itertoken.next is not tail:
            yield itertoken
            itertoken = itertoken.next
            
    def match(self, filter=None, **kwargs):
        '''Returns True if this method matches some rawstokenfilter, false otherwise.
        
        Example usage:
            >>> filter = raws.tokenfilter(exact_value='EXAMPLE')
            >>> token_a = raws.token('HELLO:THERE')
            >>> token_b = raws.token('EXAMPLE')
            >>> token_c = raws.token('EXAMPLE:NUMBER:TWO')
            >>> print token_a.match(filter)
            False
            >>> print token_b.match(filter)
            True
            >>> print token_c.match(filter)
            True
            >>> print token_a.match(exact_value='HELLO')
            True
        '''
        return (filter if filter else rawstokenfilter(**kwargs)).match(self)
        
    def add(self, auto=None, pretty=None, token=None, tokens=None, reverse=False):
        '''Adds a token or tokens nearby this one. If reverse is False the token 
        or tokens are added immediately after. If it's True, they are added before.
        
        %s
        pretty: Parses the string and adds the tokens within it.
        token: Adds this one token.
        tokens: Adds all of these tokens.
        reverse: If True, the tokens are added before instead of after.
        
        Example usage:
            >>> two = raws.token('TWO')
            >>> two.add('THREE')
            [THREE]
            >>> print two.tokenlist(include_self=True)
            [TWO][THREE]
            >>> three = two.next
            >>> three.add('[TWO AND A HALF][TWO AND THREE QUARTERS]', reverse=True)
            [[TWO AND A HALF], [TWO AND THREE QUARTERS]]
            >>> print two.tokenlist(include_self=True)
            [TWO][TWO AND A HALF][TWO AND THREE QUARTERS][THREE]
        ''' % rawstoken.auto_arg_docstring
        pretty, token, tokens = rawstoken.auto(auto, pretty, token, tokens)
        if pretty:
            tokens = rawstoken.parse(pretty)
            if len(tokens) == 1: token = tokens[0]
        if token:
            return self.addone(token, reverse)
        elif tokens:
            return self.addall(tokens, reverse)
        else:
            raise ValueError
            
    def addprop(self, auto=None, **kwargs):
        '''When this token is an object token like CREATURE:X or INORGANIC:X, a
        new token is usually added immediately afterwards. However, if a token like
        COPY_TAGS_FROM or USE_MATERIAL_TEMPLATE exists underneath the object, then
        the specified tag is only added after that. **kwargs are passed on to the
        add method.
        
        Example usage:
            >>> panda = df.getobj('CREATURE:PANDA, GIGANTIC')
            >>> print panda.tokens(range=4, include_self=True)
            <generator object tokens at 0x10c28f3c0>
            >>> print panda.tokenlist(range=4, include_self=True)
            [CREATURE:PANDA, GIGANTIC]
                [COPY_TAGS_FROM:PANDA]
                [APPLY_CREATURE_VARIATION:GIANT]
                [CV_REMOVE_TAG:CHANGE_BODY_SIZE_PERC]
            >>> panda.addprop('FLIER')
            >>> print panda.tokenlist(range=5, include_self=True)
            [CREATURE:PANDA, GIGANTIC]
                [COPY_TAGS_FROM:PANDA][FLIER]
                [APPLY_CREATURE_VARIATION:GIANT]
                [CV_REMOVE_TAG:CHANGE_BODY_SIZE_PERC]
        '''
        
        if self.value == 'INORGANIC':
            aftervalues = ('COPY_TAGS_FROM', 'USE_MATERIAL_TEMPLATE')
        else:
            aftervalues = ('COPY_TAGS_FROM',)
        addafter = self.getlastprop(value_in=aftervalues)
        if not addafter: addafter = self
        addafter.add(auto=auto, **kwargs)
    
    @staticmethod
    def firstandlast(tokens):
        '''Utility method for getting the first and last items of some iterable
        
        Example usage:
            >>> tokens = raws.token.parse('[ONE][TWO][THREE][FOUR]')
            >>> print raws.token.firstandlast(tokens)
            ([ONE], [FOUR])
        '''
        try:
            return tokens[0], tokens[-1]
        except:
            first, last = None, None
            for token in tokens:
                if first is None: first = token
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
        '''Removes this token and the next count tokens in the direction indicated by reverse.
        
        Example usage:
            >>> forest = df.getobj('ENTITY:FOREST')
            >>> print forest.tokenlist(range=5, include_self=True)
            [ENTITY:FOREST]
                [CREATURE:ELF]
                [TRANSLATION:ELF]
                [WEAPON:ITEM_WEAPON_SWORD_SHORT]
                [WEAPON:ITEM_WEAPON_SPEAR]
            >>> sword = forest.get('WEAPON:ITEM_WEAPON_SWORD_SHORT')
            >>> sword.remove()
            >>> print forest.tokenlist(range=5, include_self=True)
            [ENTITY:FOREST]
                [CREATURE:ELF]
                [TRANSLATION:ELF]
                [WEAPON:ITEM_WEAPON_SPEAR]
                [WEAPON:ITEM_WEAPON_BOW]
        '''
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
    
    @staticmethod
    def parse(data, implicit_braces=True, **kwargs):
        '''Parses a string, turns it into a list of tokens.

        data: The string to be parsed.
        implicit_braces: Determines behavior when there are no opening or closing braces.
            If True, then the input is assumed to be the contents of a token, e.g. [input].
            If False, an exception is raised.
        **kwargs: Extra named arguments are passed to the constructor each time a new
            rawstoken is distinguished and created.
            
        Example usage:
           >>> token = raws.token.parse('HELLO:THERE')
            >>> print token
            [HELLO:THERE]
            >>> tokens = raws.token.parse('[WHAT] a [BEAUTIFUL][DAY]')
            >>> print tokens
            [WHAT] a [BEAUTIFUL][DAY]
            >>> print tokens[0]
            [WHAT]
            >>> print tokens[1]
            [BEAUTIFUL] 
        '''

        tokens = rawstokenlist()    # maintain a sequential list of tokens
        pos = 0                     # byte position in data
        if data.find('[') == -1 and data.find(']') == -1:
            if implicit_braces:
                tokenparts = data.split(':')
                token = rawstoken(
                    value=tokenparts[0],
                    args=tokenparts[1:],
                    **kwargs
                )
                tokens.append(token)
                return tokens
            else:
                raise ValueError
        else:
            while pos < len(data):
                token = None
                open = data.find('[', pos)
                if open >= 0 and open < len(data):
                    close = data.find(']', open)
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
        '''Parses a string containing exactly one token. **kwargs are passed on to the parse static method.
        
        Example usage:
            >>> raws.token.parseone('[EXAMPLE]')
            [EXAMPLE]
            >>> try:
            ...     raws.token.parseone('[MORE][THAN][ONE][TOKEN]')
            ... except:
            ...     print 'There was more than one token!'
            ...
            There was more than one token!
        '''
        tokens = rawstoken.parse(*args, **kwargs)
        if len(tokens) != 1: raise ValueError
        return tokens[0]
