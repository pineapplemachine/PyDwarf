#!/usr/bin/env python
# coding: utf-8

import basefile



class contentfile(basefile.basefile):
    '''Base class for file classes which can have their contents represented as a string.'''
    
    def __init__(self):
        self.content = None
        
    def getcontent(self):
        '''Get the file's content.'''
        return self.content
        
    def setcontent(self, content):
        '''Set the file's content.'''
        self.content = content
        
    def read(self, file=None):
        '''Read the file contents given a path or file-like object.'''
        if file is None:
            path = self.path
        elif isinstance(file, basestring):
            path = file
        else:
            self.setcontent(file.read())
        with open(path, 'rb') as contentfile:
            self.setcontent(contentfile.read())
            
    def write(self, file):
        '''Write the file contents to a path or file-like object.'''
        if file is None or isinstance(file, basestring):
            dest = self.dest(path, makedir=True)
            with open(dest, 'wb') as file:
                file.write(self.getcontent())
        else:
            file.write(self.getcontent())
            
        
