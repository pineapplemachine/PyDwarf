#!/usr/bin/env python
# coding: utf-8

import os

import contentfile



class binfile(contentfile.contentfile):
    '''
        File class which is represented by a string containing its binary
        contents. Good for files which must have their content exposed or be
        manipulated but don't have their own specialized class.
    '''
    
    def __init__(self, content=None, path=None, dir=None, **kwargs):
        '''Initialize a binfile object.'''
        self.dir = None
        self.setpath(path, **kwargs)
        self.dir = dir
        self.content = content
        if self.content is None and self.path is not None and os.path.isfile(self.path): self.read(self.path)
        self.kind = 'bin'
          
    def __len__(self):
        '''Get the length in bytes of the file's binary data string.'''
        return len(self.content)
    
    def __iadd__(self, content):
        '''Add to the end of the file's content string.'''
        self.add(content)
        return self
        
    def ref(self, **kwargs):
        raise ValueError('Failed to cast binfile %s to a reffile because it is an invalid conversion.' % self)
    def bin(self, **kwargs):
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        return self
    def raw(self, **kwargs):
        self.kind = 'raw'
        self.__class__ = rawfile.rawfile
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.read(content=self.content)
        return self
        
    def copy(self):
        '''Create a copy of the file.'''
        copy = binfile()
        copy.path = self.path
        copy.rootpath = self.rootpath
        copy.name = self.name
        copy.ext = self.ext
        copy.loc = self.loc
        copy.content = self.content
        return copy
    
    def add(self, content):
        '''Add to the end of the file's content string.'''
        if self.content is None:
            self.content = str(content)
        else:
            self.content += str(content)



import rawfile
