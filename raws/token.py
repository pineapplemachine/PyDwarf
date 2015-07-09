import itertools
import inspect

from tokenargs import tokenargs
from queryable import rawsqueryable, rawstokenlist

class rawstoken(rawsqueryable):
    
    '''Internal: Recurring piece of docstrings.'''
    auto_arg_docstring = '''
        auto: When the first argument is specified the intended assignment will be
            detected automatically. If a rawstoken is specified it will be treated
            as a token argument. If a string, pretty. If anything else, tokens.'''
    
    illegal_internal_chars = tokenargs.illegal # TODO: make this better
    
    '''Don't allow these characters in a token's prefix or suffix.'''
    illegal_external_chars = '['
    
    def __init__(self, auto=None, pretty=None, copy=None, value=None, args=None, arg=None, prefix=None, suffix=None, prev=None, next=None, file=None):
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
        file: Indicates the raws.file object to which this token belongs, if any.
        
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
        
        if auto is not None:
            if isinstance(auto, basestring):
                pretty = auto
            elif isinstance(auto, rawstoken):
                copy = auto
            else:
                raise ValueError('Failed to recognize argument of type %s.' % str(type(auto)))
        
        self.value = None
        self.args = None
        self.prefix = None
        self.suffix = None
        self.prev = None
        self.next = None
        self.file = None
        
        if pretty is not None:
            copy = rawstoken.parseone(pretty, apply=self)
            
        if copy is not None:
            value = copy.value
            args = copy.args
            prefix = copy.prefix
            suffix = copy.suffix
            
        if arg is not None:
            args = [arg]
        
        if args is not None or self.args is None: self.setargs(args)
        if value is not None: self.setvalue(value)
        if prefix is not None: self.setprefix(prefix)
        if suffix is not None: self.setsuffix(suffix)
        if prev is not None: self.prev = prev
        if next is not None: self.next = next
        if file is not None: self.file = file
        
    def __hash__(self): # Not that this class is immutable, just means you'll need to be careful about when you're using token hashes
        return hash('%s:%s' % (self.value, self.argsstr()) if self.nargs() else self.value)
    
    def __str__(self):
        '''Get a string representation.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> caste = dwarf.get('CASTE')
            >>> print '"%s"' % str(caste) # show only the value and arguments
            "[CASTE:FEMALE]"
            >>> print '"%s"' % repr(caste) # show everything, including preceding and following text
            "

                Now we'll declare the specific castes.

                [CASTE:FEMALE]"
        '''
        return '[%s%s]' %(self.value, (':%s' % self.argsstr()) if self.args and len(self.args) else '')
    def __repr__(self):
        '''Get a string representation.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> caste = dwarf.get('CASTE')
            >>> print '"%s"' % str(caste) # show only the value and arguments
            "[CASTE:FEMALE]"
            >>> print '"%s"' % repr(caste) # show everything, including preceding and following text
            "

                Now we'll declare the specific castes.

                [CASTE:FEMALE]"
        '''
        return '%s%s%s' % (self.prefix if self.prefix else '', str(self), self.suffix if self.suffix else '')
        
    def __eq__(self, other):
        '''Returns True if this and the other token have the same value and arguments.
        
        Example usage:
            >>> example_a = raws.token('EXAMPLE')
            >>> example_b = raws.token('EXAMPLE')
            >>> example_c = raws.token('ANOTHER_EXAMPLE')
            >>> example_d = raws.token('ANOTHER_EXAMPLE')
            >>> example_a == example_a
            True
            >>> example_a == example_b
            True
            >>> example_a == example_c
            False
            >>> example_c == example_d
            True
        '''
        return self.equals(other)
    def __ne__(self, other):
        '''Returns True if this and the other token have a different value and arguments.
        
        Example usage:
            >>> example_a = raws.token('EXAMPLE')
            >>> example_b = raws.token('EXAMPLE')
            >>> example_c = raws.token('ANOTHER_EXAMPLE')
            >>> print example_a == example_b
            True
            >>> print example_a == example_c
            False
            >>> print example_a != example_b
            False
            >>> print example_a != example_c
            True
        '''
        return not self.equals(other)
    
    def __lt__(self, other):
        '''Returns True if this token appears before the other token in a file.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> elf = creature_standard.get('CREATURE:ELF')
            >>> goblin = creature_standard.get('CREATURE:GOBLIN') # goblins are defined immediately after elves in creature_standard
            >>> print elf > goblin
            False
            >>> print elf < goblin
            True
        '''
        return other.follows(self)
    def __gt__(self, other):
        '''Returns True if this token appears after the other token in a file.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> elf = creature_standard.get('CREATURE:ELF')
            >>> goblin = creature_standard.get('CREATURE:GOBLIN') # goblins are defined immediately after elves in creature_standard
            >>> print elf > goblin
            False
            >>> print elf < goblin
            True
        '''
        return self.follows(other)
    def __le__(self, other):
        '''Returns True if this token appears before the other token in a file, or if this and the other refer to the same token.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> elf = creature_standard.get('CREATURE:ELF')
            >>> print elf < elf
            False
            >>> print elf <= elf
            True
        '''
        return self is other or self.__lt__(other)
    def __ge__(self, other):
        '''Returns True if this token appears after the other token in a file, or if this and the other refer to the same token.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> elf = creature_standard.get('CREATURE:ELF')
            >>> print elf > elf
            False
            >>> print elf >= elf
            True
        '''
        return self is other or self.__gt__(other)
        
    def __add__(self, other):
        '''Concatenates and returns a raws.tokenlist object.
        
        Example usage:
            >>> one = raws.token('NUMBER:ONE')
            >>> two = raws.token('NUMBER:TWO')
            >>> three = raws.token('NUMBER:THREE')
            >>> tokens =  one + two + three
            >>> print tokens
            [NUMBER:ONE][NUMBER:TWO][NUMBER:THREE]
            >>> zero = raws.token('NUMBER:ZERO')
            >>> print zero + tokens
            [NUMBER:ZERO][NUMBER:ONE][NUMBER:TWO][NUMBER:THREE]
        '''
        if isinstance(other, rawstoken):
            tokens = rawstokenlist()
            tokens.append(self)
            tokens.append(other)
            return tokens
        elif isinstance(other, rawsqueryable):
            tokens = rawstokenlist()
            tokens.append(self)
            tokens.extend(other)
            return tokens
        else:
            raise ValueError('Failed to perform concatenation because the type of the other operand was unrecognized.')
    def __radd__(self, other):
        '''Internal: Same as __add__ except reversed.'''
        if isinstance(other, rawstoken):
            tokens = rawstokenlist()
            tokens.append(other)
            tokens.append(self)
            return tokens
        elif isinstance(other, rawsqueryable):
            tokens = rawstokenlist()
            tokens.extend(other)
            tokens.append(self)
            return tokens
        else:
            raise ValueError('Failed to perform concatenation because the type of the other operand was unrecognized.')
            
    def __mul__(self, value):
        '''Concatenates copies of this token the number of times specified.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token * 2
            [EXAMPLE][EXAMPLE]
            >>> print token * 6
            [EXAMPLE][EXAMPLE][EXAMPLE][EXAMPLE][EXAMPLE][EXAMPLE]
        '''
        tokens = rawstokenlist()
        for i in xrange(0, int(value)):
            tokens.append(rawstoken.copy(self))
        return tokens
    
    def __iter__(self):
        yield self.value
        for arg in self.args: yield arg
    def __len__(self):
        return self.nargs()
    def __contains__(self, value):
        return self.containsarg(value)
        
    def __iadd__(self, value):
        self.addarg(value)
            
    def __nonzero__(self):
        return True
        
    @staticmethod
    def autosingular(auto=None, token=None, **kwargs):
        '''Internal: Convenience function for handling method arguments when exactly one token is expected.'''
        if auto is not None:
            if isinstance(auto, basestring):
                kwargs['pretty'] = auto
            elif isinstance(auto, rawstoken):
                return auto
            else:
                raise ValueError('Failed to recognize argument of type %s as valid.' % str(type(auto)))
        return rawstoken(**kwargs)
        
    @staticmethod
    def autoplural(*args, **kwargs):
        '''Internal: Convenience function for handling method arguments when a list of tokens is expected.'''
        token, tokens = rawstoken.autovariable(*args, **kwargs)
        if token is not None:
            tokens = rawstokenlist()
            tokens.append(token)
        return tokens
        
    @staticmethod
    def autovariable(auto=None, pretty=None, token=None, tokens=None, **kwargs):
        '''Internal: Convenience function when either a single token or a list of tokens is acceptable as a method's argument.'''
        if auto is not None:
            if isinstance(auto, basestring):
                pretty = auto
            elif isinstance(auto, rawstoken):
                token = auto
            elif isinstance(auto, rawsqueryable):
                tokens = auto.tokens()
            else:
                tokens = auto
        if pretty is not None:
            tokens = rawstoken.parse(pretty)
        if kwargs:
            token = rawstoken.autosingular(**kwargs)
        if token is not None and tokens is not None:
            raise ValueError('Failed to recognize arguments because both singular and plural token arguments were detected.')
        elif token is None and tokens is None:
            raise ValueError('Received no recognized arguments.')
        return token, tokens
        
    def index(self, index):
        itrtoken = self
        for i in xrange(0, abs(index)):
            itrtoken = itrtoken.next if index > 0 else itrtoken.prev
            if itrtoken is None: return None
        return itrtoken
        
    def follows(self, other):
        if other is not None:
            for token in other.tokens():
                if token is self:
                    return True
        return False
        
    def strip(self):
        self.prefix = None
        self.suffix = None
        
    def nargs(self, count=None):
        '''When count is None, returns the number of arguments the token has. (Length of
        arguments list.) Otherwise, returns True if the number of arguments is equal to the
        given count and False if not.
        
        count: The number of arguments to match.
        
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
        
    def setarg(self, index, value=None):
        '''Sets argument at index, also verifies that the input contains no illegal characters.
        If the index argument is set but not value, then the index is assumed to be referring to
        a value and the index is assumed to be 0.
        
        index: The argument index.
        value: The value to set that argument to.
        
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
        self.args[index] = value
    
    def setargs(self, args=None):
        if self.args is None:
            self.args = tokenargs(args)
        else:
            self.args[:] = args
            
    def clearargs(self):
        self.args.clear()
        
    def addarg(self, value):
        '''Appends an argument to the end of the argument list.
        
        value: The value to add to the argument list.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token
            [EXAMPLE]
            >>> token.addarg('hi!')
            >>> print token
            [EXAMPLE:hi!]
        '''
        self.args.append(value)
        
    def addargs(self, values):
        self.args.extend(values)
        
    def containsarg(self, value):
        return value in self.args
        
    def argsstr(self):
        '''Return arguments joined by ':'.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> print token.argsstr()
            a:b:c
        '''
        return str(self.args)
        
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
        
        value: The value to be set.
        
        Example usage:
            >>> token = raws.token('EXAMPLE:a:b:c')
            >>> token.setvalue('JUST KIDDING')
            >>> print token
            [JUST KIDDING:a:b:c]
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_internal_chars]): raise ValueError('Failed to set token value to %s because the string contains illegal characters.' % valuestr)
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
        
        value: The value to be set.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token
            [EXAMPLE]
            >>> token.setprefix('hello ')
            >>> print repr(token)
            hello [EXAMPLE]
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_external_chars]): raise ValueError('Failed to set token prefix to %s because the string contains illegal characters.' % valuestr)
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
        
        value: The value to be set.
        
        Example usage:
            >>> token = raws.token('EXAMPLE')
            >>> print token
            [EXAMPLE]
            >>> token.setsuffix(' world')
            >>> print repr(token)
            [EXAMPLE] world
        '''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_external_chars]): raise ValueError('Failed to set token suffix to %s because the string contains illegal characters.' % valuestr)
        self.suffix = value
        
    def arg(self, index=None):
        '''When an index is given, the argument at that index is returned. If left
        set to None then the first argument is returned if the token has exactly one
        argument, otherwise an exception is raised.
        
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
        if index is None:
            if len(self.args) != 1: raise ValueError('Failed to retrieve token argument because it doesn\'t have exactly one.')
            return self.args[0]
        else:
            return self.args[index]
        
    def equals(self, other):
        '''Returns True if two tokens have identical values and arguments, False otherwise.
        
        other: The other raws.token object.
        
        Example usage:
            >>> token_a = raws.token('EXAMPLE:hi!')
            >>> token_b = raws.token('EXAMPLE:hello there')
            >>> token_c = raws.token('EXAMPLE:hi!')
            >>> print token_a, token_b, token_c
            [EXAMPLE:hi!] [EXAMPLE:hello there] [EXAMPLE:hi!]
            >>> print token_a.equals(token_b) # Same as token_a == token_b
            False
            >>> print token_b.equals(token_c)
            False
            >>> print token_c.equals(token_a)
            True
            >>> print token_c is token_a
            False
        '''
        return(
            other is not None and
            self.value == other.value and
            self.args == other.args
        )
        
    @staticmethod
    def tokensequal(atokens, btokens):
        '''Determine whether two iterables containing tokens contain equivalent tokens.
        
        atokens: The first iterable.
        btokens: The second iterable.
        
        Example usage:
            >>> a = raws.token.parse('[A][B][C]')
            >>> b = raws.token.parse('[A][B][C]')
            >>> print a is b
            False
            >>> print raws.token.tokensequal(a, b)
            True
        '''
        for atoken, btoken in itertools.izip(atokens, btokens):
            if not atoken.equals(btoken): return False
        return True
    
    @staticmethod
    def copy(*args, **kwargs):
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
        token, tokens = rawstoken.autovariable(*args, **kwargs)
        if token is not None:
            return rawstoken(copy=token)
        elif tokens is not None:
            if inspect.isgenerator(tokens) or inspect.isgeneratorfunction(tokens):
                return rawstoken.icopytokens(tokens=tokens)
            else:
                return rawstoken.copytokens(tokens=tokens)
    
    @staticmethod
    def copytokens(tokens):
        copiedtokens = rawstokenlist()
        prevtoken = None
        for token in tokens:
            copytoken = rawstoken(copy=token)
            copiedtokens.append(copytoken)
            copytoken.prev = prevtoken
            if prevtoken is not None: prevtoken.next = copytoken
            prevtoken = copytoken
        return copiedtokens
        
    @staticmethod
    def icopytokens(tokens):
        prevtoken = None
        for token in tokens:
            copytoken = rawstoken(copy=token)
            copytoken.prev = prevtoken
            if prevtoken is not None: prevtoken.next = copytoken
            prevtoken = copytoken
            yield token
        
    def tokens(self, range=None, include_self=False, reverse=False, until_token=None, step=None):
        '''Iterate through successive tokens starting with this one.
        
        range: If defined as an integer, then iteration stops when this many tokens
            have been iterated over.
        include_self: If True, iteration includes this token. Otherwise, iteration
            starts with the immediately following or preceding token.
        reverse: If False, iteration goes forward through the sequence of tokens. If
            True, it goes backwards.
        until_token: Iteration stops if/when the current token matches this exact
            object.
        step: Increment by this many tokens each step. Defaults to None, which means
            that every token is yielded.
            
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
            [HOW][ARE][YOU]
            >>> print raws.tokenlist(last_token.tokens(reverse=True))
            [YOU][ARE][HOW][HI]
        '''
        count = 0
        itertoken = self if include_self else (self.prev if reverse else self.next)
        while itertoken is not None and (range is None or range > count) and (until_token is None or itertoken is not until_token.next):
            if (step is None) or (count % step == 0): yield itertoken
            itertoken = itertoken.prev if reverse else itertoken.next
            count += 1
    
    def add(self, *args, **kwargs):
        '''
            Adds a token or tokens nearby this one. If reverse is False the token 
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
                >>> print two.list(include_self=True)
                [TWO][THREE]
                >>> three = two.next
                >>> three.add('[TWO AND A HALF][TWO AND THREE QUARTERS]', reverse=True)
                [[TWO AND A HALF], [TWO AND THREE QUARTERS]]
                >>> print two.list(include_self=True)
                [TWO][TWO AND A HALF][TWO AND THREE QUARTERS][THREE]
        ''' % rawstoken.auto_arg_docstring
        reverse = kwargs.get('reverse', False)
        knit = kwargs.get('knit', False)
        token, tokens = rawstoken.autovariable(*args, **kwargs)
        if token is not None:
            return self.addone(token, reverse=reverse, knit=knit)
        elif tokens is not None:
            return self.addall(tokens, reverse=reverse, knit=knit)
            
    def addprop(self, *args, **kwargs):
        '''When this token is an object token like CREATURE:X or INORGANIC:X, a
        new token is usually added immediately afterwards. However, if a token like
        COPY_TAGS_FROM or USE_MATERIAL_TEMPLATE exists underneath the object, then
        the specified tag is only added after that. **kwargs are passed on to the
        add method.
        
        Example usage:
            >>> panda = df.getobj('CREATURE:PANDA, GIGANTIC')
            >>> print panda.tokens(range=4, include_self=True)
            <generator object tokens at 0x10c28f3c0>
            >>> print panda.list(range=4, include_self=True)
            [CREATURE:PANDA, GIGANTIC]
                [COPY_TAGS_FROM:PANDA]
                [APPLY_CREATURE_VARIATION:GIANT]
                [CV_REMOVE_TAG:CHANGE_BODY_SIZE_PERC]
            >>> panda.addprop('FLIER')
            >>> print panda.list(range=5, include_self=True)
            [CREATURE:PANDA, GIGANTIC]
                [COPY_TAGS_FROM:PANDA][FLIER]
                [APPLY_CREATURE_VARIATION:GIANT]
                [CV_REMOVE_TAG:CHANGE_BODY_SIZE_PERC]
        '''
        
        aftervalues = ['COPY_TAGS_FROM', 'CV_REMOVE_TAG']
        beforevalues = ['SELECT_MATERIAL']
        if self.value == 'INORGANIC':
            aftervalues.append('USE_MATERIAL_TEMPLATE')
        elif self.value == 'CREATURE':
            aftervalues.extend(('APPLY_CREATURE_VARIATION', 'APPLY_CURRENT_CREATURE_VARIATION'))
            beforevalues,extend(('CASTE', 'SELECT_CASTE'))
        addafter = self.getlastprop(value_in=aftervalues, until_value_in=beforevalues)
        if not addafter: addafter = self
        addafter.add(*args, **kwargs)
    
    @staticmethod
    def firstandlast(tokens, setfile=None):
        '''Utility method for getting the first and last items of some iterable
        
        Example usage:
            >>> tokens = raws.token.parse('[ONE][TWO][THREE][FOUR]')
            >>> print raws.token.firstandlast(tokens)
            ([ONE], [FOUR])
        '''
        try:
            if setfile is not None: raise ValueError
            return tokens[0], tokens[-1]
        except Exception as e:
            first, last = None, None
            for token in tokens:
                if first is None: first = token
                last = token
                if setfile is not None: token.file = setfile
            return first, last            
        
    def addone(self, token, reverse=False, knit=True):
        '''Internal: Utility method called by add when adding a single token'''
        
        token.file = self.file
        if token.prev is not None or token.next is not None:
            if knit:
                if token.prev is not None: token.prev.next = token.next
                if token.next is not None: token.next.prev = token.prev
            else:
                raise ValueError('Failed to add tokens because they already appear within a sequence of other tokens.')
        
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
    
    def addall(self, tokens, reverse=False, knit=True):
        '''Internal: Utility method called by add when adding multiple tokens'''
        
        first, last = rawstoken.firstandlast(tokens, setfile=self.file, knit=True)
        if token.prev is not None or token.next is not None:
            if knit:
                if first.prev is not None: first.prev.next = last.next
                if last.next is not None: last.next.prev = first.prev
            else:
                raise ValueError('Failed to add tokens because they already appear within a sequence of other tokens.')
                
        if reverse:
            last.next = self
            first.prev = self.prev
            if self.prev: self.prev.next = first
            self.prev = last
        else:
            first.prev = self
            last.next = self.next
            if self.next: self.next.prev = last
            self.next = first
        return tokens
    
    def remove(self, count=0, reverse=False):
        '''Removes this token and the next count tokens in the direction indicated by reverse.
        
        Example usage:
            >>> forest = df.getobj('ENTITY:FOREST')
            >>> print forest.list(range=5, include_self=True)
            [ENTITY:FOREST]
                [CREATURE:ELF]
                [TRANSLATION:ELF]
                [WEAPON:ITEM_WEAPON_SWORD_SHORT]
                [WEAPON:ITEM_WEAPON_SPEAR]
            >>> sword = forest.get('WEAPON:ITEM_WEAPON_SWORD_SHORT')
            >>> sword.remove()
            >>> print forest.list(range=5, include_self=True)
            [ENTITY:FOREST]
                [CREATURE:ELF]
                [TRANSLATION:ELF]
                [WEAPON:ITEM_WEAPON_SPEAR]
                [WEAPON:ITEM_WEAPON_BOW]
        '''
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
        self.file = None
    
    @staticmethod
    def parse(data, implicit_braces=False, **kwargs):
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
                    value = tokenparts[0],
                    args = tokenparts[1:],
                    **kwargs
                )
                tokens.append(token)
                return tokens
            else:
                raise ValueError('Failed to parse data string because it had no braces and because implicit_braces was set to False.')
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
                            value = tokenparts[0],
                            args = tokenparts[1:],
                            prefix = prefix,
                            prev = tokens[-1] if len(tokens) else None,
                            **kwargs
                        )
                        pos = close+1
                if token is not None:
                    if len(tokens): tokens[-1].next = token
                    tokens.append(token)
                else:
                    break
            if len(tokens) and pos<len(data):
                tokens[-1].suffix = data[pos:]
            return tokens
            
    @staticmethod
    def parseone(data, implicit_braces=True, fail_on_multiple=True, apply=None, **kwargs):
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
        if fail_on_multiple and data.count('[') > 1: raise ValueError('Failed to parse token because there was more than one open bracket in the data string.')
        open = data.find('[')
        close = data.find(']')
        tokenparts = None
        if open == -1 and close == -1 and implicit_braces:
            pass
        elif open >= 0 and close >= 0:
            data = data[data.find('[') + 1 : data.find(']')]
        else:
            raise ValueError('Failed to parse token because data string contained mismatched brackets.')
        tokenparts = data.split(':')
        if apply:
            apply.setvalue(tokenparts[0])
            apply.setargs(tokenparts[1:])
            return apply
        else:
            return rawstoken(
                value = tokenparts[0],
                args = tokenparts[1:],
                **kwargs
            )
