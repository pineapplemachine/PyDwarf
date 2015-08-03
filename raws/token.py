#!/usr/bin/env python
# coding: utf-8

import queryableaddprop
import tokenargs



class token(queryableaddprop.queryableaddprop):
    
    illegal_internal_chars = tokenargs.tokenargs.illegal # TODO: make this better
    
    '''Don't allow these characters in a token's prefix or suffix.'''
    illegal_external_chars = '['
    
    def __init__(self, auto=None, pretty=None, copy=None, value=None, args=None, arg=None, prefix=None, suffix=None, prev=None, next=None, file=None):
        '''Constructs a token object.'''
        
        if auto is not None:
            if isinstance(auto, basestring):
                pretty = auto
            elif isinstance(auto, rawstoken):
                copy = auto
            else:
                raise TypeError('Failed to recognize argument of type %s.' % str(type(auto)))
        
        self.value = None
        self.args = None
        self.prefix = None
        self.suffix = None
        self.prev = None
        self.next = None
        self.file = None
        
        if pretty is not None:
            copy = tokenparse.parsesingular(pretty, apply=self)
            
        if copy is not None:
            value = copy.value
            args = copy.args
            prefix = copy.prefix
            suffix = copy.suffix
            
        if arg is not None:
            args = [arg]
        
        if self.args is None or args is not None: self.args = args
        if value is not None: self.setvalue(value)
        if prefix is not None: self.setprefix(prefix)
        if suffix is not None: self.setsuffix(suffix)
        if prev is not None: self.prev = prev
        if next is not None: self.next = next
        if file is not None: self.file = file
        
    def __hash__(self):
        '''
            Not that this class is immutable, just means you'll need to be
            careful about when you're using token hashes.
        '''
        return hash('%s:%s' % (self.value, self.args) if self.nargs() else self.value)
    
    def __str__(self, short=True):
        '''Get a string representation.'''
        internal = '[%s%s]' %(self.value, (':%s' % self.args) if self.args else '')
        if short:
            return internal
        else:
            return '%s%s%s' % (self.prefix if self.prefix else '', internal, self.suffix if self.suffix else '')
        
    def __eq__(self, other):
        '''Returns True if this and the other token have the same value and arguments.
        '''
        return self.equals(other)
    def __ne__(self, other):
        '''Returns True if this and the other token have a different value and arguments.
        '''
        return not self.equals(other)
    
    def __lt__(self, other):
        '''Returns True if this token appears before the other token in a file.
        '''
        return other.follows(self)
    def __gt__(self, other):
        '''Returns True if this token appears after the other token in a file.
        '''
        return self.follows(other)
    def __le__(self, other):
        '''Returns True if this token appears before the other token in a file, or if this and the other refer to the same token.
        '''
        return self is other or self.__lt__(other)
    def __ge__(self, other):
        '''Returns True if this token appears after the other token in a file, or if this and the other refer to the same token.
        '''
        return self is other or self.__gt__(other)
        
    def __add__(self, other):
        '''Concatenate and return a tokenlist.'''
        if isinstance(other, rawstoken):
            tokens = tokenlist.tokenlist()
            tokens.append(self)
            tokens.append(other)
            return tokens
        elif isinstance(other, queryable.queryable):
            tokens = tokenlist.tokenlist()
            tokens.append(self)
            tokens.extend(other)
            return tokens
        else:
            raise TypeError('Failed to perform concatenation because the type %s of the other operand was unrecognized.' % type(other))
        
    def __radd__(self, other):
        '''Concatenate and return a tokenlist.'''
        if isinstance(other, rawstoken):
            tokens = tokenlist.tokenlist()
            tokens.append(other)
            tokens.append(self)
            return tokens
        elif isinstance(other, queryable.queryable):
            tokens = tokenlist.tokenlist()
            tokens.extend(other)
            tokens.append(self)
            return tokens
        else:
            raise TypeError('Failed to perform concatenation because the type %s of the other operand was unrecognized.' % type(other))
            
    def __mul__(self, value):
        '''Concatenates copies of this token the number of times specified.
        '''
        tokens = tokenlist.tokenlist()
        for i in xrange(0, int(value)):
            tokens.append(self.copy())
        return tokens
    
    def __iter__(self):
        '''Yields the tokens value and then each of its arguments.'''
        yield self.value
        for arg in self.args: yield arg
    def __len__(self):
        '''Returns the number of arguments.'''
        return self.nargs()
    def __contains__(self, value):
        '''Determine whether an argument is present within the token's argument list.'''
        return self.containsarg(value)
        
    def __iadd__(self, value):
        '''Append to the token's argument list.'''
        self.args.add(value)
        return self
    def __isub__(self, value):
        '''Remove the last value from the token's argument list.'''
        self.args.sub(value)
        return self
            
    def __nonzero__(self):
        '''Always returns True.'''
        return True
        
    def __setattr__(self, name, value):
        if name == 'args':
            if 'args' not in self.__dict__ or self.args is None:
                self.__dict__['args'] = tokenargs.tokenargs()
            self.__dict__['args'].reset(value)
        else:
            super(token, self).__setattr__(name, value)
        
    @staticmethod
    def autosingular(auto=None, token=None, **kwargs):
        '''Internal: Convenience function for handling method arguments when exactly one token is expected.'''
        if auto is not None:
            if isinstance(auto, basestring):
                kwargs['pretty'] = auto
            elif isinstance(auto, rawstoken):
                return auto
            else:
                raise TypeError('Failed to recognize argument of type %s as valid.' % str(type(auto)))
        return rawstoken(**kwargs)
        
    @staticmethod
    def autoplural(*args, **kwargs):
        '''Internal: Convenience function for handling method arguments when a list of tokens is expected.'''
        token, tokens = rawstoken.autovariable(*args, implicit=kwargs.get('implicit', False), **kwargs)
        if token is not None:
            tokens = tokenlist.tokenlist()
            tokens.append(token)
        return tokens
        
    @staticmethod
    def autovariable(auto=None, pretty=None, token=None, tokens=None, implicit=True, **kwargs):
        '''Internal: Convenience function when either a single token or a list of tokens is acceptable as a method's argument.'''
        if auto is not None:
            if isinstance(auto, basestring):
                pretty = auto
            elif isinstance(auto, rawstoken):
                token = auto
            elif isinstance(auto, queryable.queryable):
                tokens = auto.tokens()
            else:
                tokens = auto
        if pretty is not None:
            parsed = tokenparse.parsevariable(pretty, implicit=implicit)
            if isinstance(parsed, rawstoken):
                token = parsed
            else:
                tokens = parsed
        if kwargs:
            token = rawstoken.autosingular(**kwargs)
        if token is not None and tokens is not None:
            raise ValueError('Failed to recognize arguments because both singular and plural token arguments were detected.')
        elif token is None and tokens is None:
            raise ValueError('Received no recognized arguments.')
        return token, tokens
        
    def index(self, index):
        '''Return the token at an integer offset relative to this one.'''
        itrtoken = self
        for i in xrange(0, abs(index)):
            itrtoken = itrtoken.next if index > 0 else itrtoken.prev
            if itrtoken is None: return None
        return itrtoken
        
    def follows(self, other):
        '''
            Return True if a particular token is located after this one in some
            file or list.
        '''
        if other is not None:
            for token in other.tokens():
                if token is self:
                    return True
        return False
        
    def strip(self):
        self.prefix = None
        self.suffix = None
        
    def nargs(self, count=None):
        '''
            When count is None, returns the number of arguments the token has.
            Otherwise, returns True if the number of arguments is equal to the
            given count and False if not.
        '''
        return len(self.args) if (count is None) else (len(self.args) == count)

    def setargs(self, args=None):
        '''Set the token's arguments.'''
        self.args = args
        
    def getargs(self):
        '''Get the token's arguments.'''
        return self.args
        
    def getvalue(self):
        '''Get the token's value.'''
        return self.value
        
    def setvalue(self, value):
        '''Set the token's value.'''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_internal_chars]): raise ValueError('Failed to set token value to "%s" because the string contains illegal characters.' % valuestr)
        self.value = value
        
    def getprefix(self):
        '''Get the comment text preceding a token.'''
        return self.prefix
    
    def setprefix(self, value):
        '''Set the comment text preceding a token.'''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_external_chars]): raise ValueError('Failed to set token prefix to "%s" because the string contains illegal characters.' % valuestr)
        self.prefix = value
        
    def getsuffix(self):
        '''Get the comment text following a token.'''
        return self.suffix
    
    def setsuffix(self, value):
        '''Set the comment text following a token.'''
        valuestr = str(value)
        if any([char in valuestr for char in rawstoken.illegal_external_chars]): raise ValueError('Failed to set token suffix to "%s" because the string contains illegal characters.' % valuestr)
        self.suffix = value
        
    def arg(self, index=None):
        '''
            When an index is given, the argument at that index is returned. If left
            set to None then the first argument is returned if the token has exactly one
            argument, otherwise an exception is raised.
        '''
        if index is None:
            if len(self.args) != 1: raise ValueError('Failed to retrieve token argument because it doesn\'t have exactly one.')
            return self.args[0]
        else:
            return self.args[index]
        
    def equals(self, other):
        '''Returns True if two tokens have identical values and arguments, False otherwise.'''
        if isinstance(other, rawstoken):
            return(
                other is not None and
                other is not rawstoken.nulltoken and
                self is not rawstoken.nulltoken and
                self.value == other.value and
                self.args == other.args
            )
        elif isinstance(other, basestring):
            return self.equals(rawstoken(pretty=other))
        else:
            raise TypeError('Failed to check token equivalency against object of type %s.' % type(other))
    
    def copy(self):
        '''Returns a copy of this token.'''
        return rawstoken(copy=self)
        
    def itokens(self, range=None, include_self=False, reverse=False, until=None, step=None):
        '''Iterate through successive tokens starting with this one.'''
        count = 0
        itertoken = self if include_self else (self.prev if reverse else self.next)
        while itertoken is not None and (range is None or range > count) and (until is None or itertoken is not until.next):
            if (step is None) or (count % step == 0): yield itertoken
            itertoken = itertoken.prev if reverse else itertoken.next
            count += 1
    
    def add(self, *args, **kwargs):
        '''
            Adds a token or tokens nearby this one. If reverse is False the token 
            or tokens are added immediately after. If it's True, they are added before.
        '''
        
        reverse = kwargs.get('reverse', False)
        if 'reverse' in kwargs: del kwargs['reverse']
        
        knit = kwargs.get('knit', False)
        if 'knit' in kwargs: del kwargs['knit']
        
        token, tokens = rawstoken.autovariable(*args, **kwargs)
        
        if token is not None:
            return self.addone(token, reverse=reverse, knit=knit)
        elif tokens is not None:
            return self.addall(tokens, reverse=reverse, knit=knit)
        
    def addone(self, token, reverse=False, knit=True):
        '''Internal: Utility method called by add when adding a single token.'''
        
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
        '''Internal: Utility method called by add when adding multiple tokens.'''
        
        first, last = helpers.ends(tokens, setfile=self.file)
        if first.prev is not None or last.next is not None:
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
        
    def propterminationfilter(self, naive=True):
        if self.file is not None:
            # Smartest: Base it off file header and objects knowledge if possible.
            header = self.file.getobjheaders()[0]
        
        elif naive:
            # Naive: If the information for smart isn't available, assume this token itself is the root object token.
            header = objects.headerforobject(self)
        
        else:
            raise ValueError('Failed to get termination filter for token because there wasn\'t enough information and because the naive filter was disallowed.')
            
        terminators = objects.objectsforheader(header)
        return lambda token, count: (False, token.value in terminators and token.nargs(1))
    
    def remove(self, count=0, reverse=False):
        '''Removes this token and the next count tokens in the direction indicated by reverse.'''
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
        self.prev = None
        self.next = None
        
    def removeselfandprops(self, *args, **kwargs):
        tokens = [self] + self.removeallprop(*args, **kwargs)
        self.remove()
        return tokens

token.nulltoken = token()

rawstoken = token



import queryable
import tokenlist
import objects
import tokenparse
import helpers
