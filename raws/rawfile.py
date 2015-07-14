#!/usr/bin/env python
# coding: utf-8

import os

import basefile
import queryableobj
import queryableadd



class rawfile(basefile.basefile, queryableobj.queryableobj, queryableadd.queryableadd):
    '''Represents a single file within a raws directory.'''
    
    def __init__(self, name=None, file=None, path=None, root=None, content=None, tokens=None, dir=None, readpath=True, noheader=False, **kwargs):
        '''Constructs a new raws file object.
        
        name: The name string to appear at the top of the file. Also used to determine filename.
        data: A string to be parsed into token data.
        path: A path to the file from which this object is being parsed, if any exists.
        tokens: An iterable of tokens from which to construct the object; these tokens will be its initial contents.
        file: A file-like object from which to automatically read the name and data attributes.
        dir: Which raws.dir object this file belongs to.
        '''
        
        self.dir = dir
        self.data = None
        self.noheader = noheader
        self.setpath(path=path, root=root, **kwargs)
        
        self.roottoken = None
        self.tailtoken = None
        
        if file:
            self.read(file)
        elif path and readpath:
            self.read(path)
            
        if name is not None: self.name = name
        
        if content is not None:
            self.read(content=content)
        elif tokens is not None:
            self.settokens(tokens, setfile=True)
        
        if name: self.name = name
        
        if (not self.path) and (not self.ext): self.ext = '.txt'
        self.kind = 'raw'
            
    def __enter__(self):
        return self
    def __exit__(self):
        if self.path: self.write(self.path)
            
    def __eq__(self, other):
        return self.equals(other)
    def __ne__(self, other):
        return not self.equals(other)
        
    def __len__(self):
        return self.length()
        
    def __nonzero__(self):
        return True
        
    def __repr__(self):
        return self.content()
        
    def content(self):
        tokencontent = ''.join([repr(o) for o in self.tokens()])
        if self.noheader:
            return tokencontent
        else:
            return '%s\n%s' %(self.name, tokencontent)
        
    def ref(self, **kwargs):
        raise ValueError('Failed to cast rawfile %s to reffile because it is an invalid conversion.' % self)
    def bin(self, **kwargs):
        self.kind = 'bin'
        self.__class__ =  binfile.binfile
        content = kwargs.get('content', self.content()) # TODO: rename method to getcontent for sake of consistency
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.content = content
        return self
    def raw(self, **kwargs):
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        return self
    
    def index(self, index):
        itrtoken = self.root() if index >= 0 else self.tail()
        index += (index < 0)
        for i in xrange(0, abs(index)):
            itrtoken = itrtoken.next if index > 0 else itrtoken.prev
            if itrtoken is None: return None
        return itrtoken
        
    def getpath(self):
        return self.path
        
    def settokens(self, tokens, setfile=True):
        '''Internal: Utility method for setting the root and tail tokens given an iterable.'''
        self.roottoken, self.tailtoken = rawstoken.token.firstandlast(tokens, self if setfile else None)
    
    def copy(self):
        '''Makes a copy of a file and its contents.
        '''
        copy = rawfile()
        copy.path = self.path
        copy.rootpath = self.rootpath
        copy.name = self.name
        copy.ext = self.ext
        copy.loc = self.loc
        copy.noheader = self.noheader
        copy.settokens(rawstoken.token.icopytokens(self.tokens()))
        return copy
        
    def equals(self, other):
        return rawstoken.token.tokensequal(self.tokens(), other.tokens())
        
    def root(self):
        '''Gets the first token in the file.
        '''
        while self.roottoken is not None and self.roottoken.prev is not None: self.roottoken = self.roottoken.prev
        return self.roottoken
    def tail(self):
        '''Gets the last token in the file.
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
            
    def read(self, file=None, content=None, **kwargs):
        '''Given a path or file-like object, reads name and data.'''
        self.roottoken = None
        self.tailtoken = None 
        
        if file is None and content is None:
            with open(self.path, 'rb') as src:
                content = src.read()
        elif isinstance(file, basestring):
            self.path = file
            self.ext = os.path.splitext(file)[1]
            with open(file, 'rb') as src:
                content = src.read()
        else:
            content = file.read()
        
        if content:
            parts = content.split('\n', 1)
            header = None
            data = None
            if len(parts) == 1:
                data = parts[0]
            elif len(parts) == 2:
                header, data = parts
            header = header.strip()
            if self.name:
                if header != self.name: self.noheader = True
            if data:
                self.settokens(rawstoken.token.parseplural(data, file=self))
        else:
            self.noheader = True
            self.data = None
            
    def write(self, file):
        '''Given a path to a directory or a file-like object, writes the file's contents to that file.'''
        if isinstance(file, basestring):
            with open(self.dest(file, makedir=True), 'wb') as dest:
                dest.write(self.content())
        else:
            file.write(self.content())
    
    def add(self, *args, **kwargs):
        '''Adds tokens to the end of a file.
        '''
        tail = self.tail()
        if tail:
            return tail.add(*args, **kwargs)
        else:
            token, tokens = rawstoken.token.autovariable(*args, **kwargs)
            if token is not None:
                self.roottoken = token
                self.tailtoken = token
                token.file = self
                return token
            elif tokens is not None:
                self.settokens(tokens)
                return tokens
        
    def length(self, *args, **kwargs):
        '''Get the number of tokens in this file.
        
        Example usage:
            >>> print df.getfile('creature_standard').length()
            5516
            >>> print df.getfile('inorganic_metal').length()
            1022
            >>> print df.getfile('item_pants').length()
            109
        '''
        return sum(1 for token in self.tokens(*args, **kwargs))
        
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
        for token in self.tokens(): token.file = None
        self.roottoken = None
        self.tailtoken = None
        
    def getobjheaders(self, type):
        match_types = self.getobjheadername(type)
        root = self.root()
        return (root,) if root is not None and root.value == 'OBJECT' and root.nargs(1) and root.args[0] in match_types else tuple()



import token as rawstoken
import binfile
