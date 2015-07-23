#!/usr/bin/env python
# coding: utf-8

import os
import traceback



class basefile(object):
    '''
        Base abstract class for file objects. The files which belong to dir
        objects inherit from this class.
    '''
    
    def __init__(self):
        self.dir = None
        self.path = None
        self.rootpath = None
        self.loc = None
        self.name = None
        self.ext = None
        self.kind = None
    
    def __str__(self):
        if self.name and self.ext:
            name = ''.join((self.name, self.ext))
        else:
            name = self.name
        path = os.path.join(self.loc, name) if self.loc and name else name
        return path.replace('\\', '/') if path else ''
    def __repr__(self):
        return str(self)
        
    def __hash__(self):
        return hash(str(self))
        
    def __eq__(self, other):
        return str(self) == str(other)
    def __ne__(self, other):
        return str(self) != str(other)
    
    def __gt__(self, other):
        return str(self) > str(other)
    def __ge__(self, other):
        return str(self) >= str(other)
    def __lt__(self, other):
        return str(self) < str(other)
    def __le__(self, other):
        return str(self) <= str(other)
        
    def getpath(self):
        '''Get the path of where the file is located.'''
        return self.path
        
    def setpath(self, path, root=None, loc=None, name=None, ext=None):
        '''
            Set path for file, and set other important attributes like name,
            extension, location while we're at it.
        '''
        if self.dir and self.dir.root and (not root): root = self.dir.root
        path = os.path.abspath(path) if path else None
        root = os.path.abspath(root) if root else None
        self.path = path
        self.rootpath = root
        if not path:
            self.name, self.ext = None, None
        elif os.path.isfile(path):
            self.name, self.ext = os.path.splitext(os.path.basename(path))
        else:
            self.name, self.ext = os.path.basename(path), None
        if root and path and root != path and path.startswith(root):
            self.loc = os.path.dirname(os.path.relpath(path, root))
        else:
            self.loc = None
        if loc: self.loc = loc
        if name: self.name = name
        if ext: self.ext = ext
        self.kind = self.ext[1:] if self.ext else 'dir'
        
    def getname(self):
        '''Get the file name.'''
        return self.name
        
    def setname(self, name):
        '''Set the file name.'''
        self.name = name
        
    def getext(self):
        '''Get the file extension.'''
        return self.ext
        
    def setext(self, ext):
        '''Set the file extension.'''
        if '.' in ext: raise ValueError(
            'Failed to set file extension to "%s" because the string contains a period.'
        )
        self.ext = ext
        
    def getloc(self):
        '''Get the file location relative to a dir object's root.'''
        return self.loc
    
    def setloc(self, loc):
        '''Set the file location relative to a dir object's root.'''
        self.loc = loc
        
    def reloc(self, loc):
        '''Set the file location relative to its current location.'''
        if loc and self.loc:
            self.loc = os.path.join(loc, self.loc)
        elif loc:
            self.loc = loc
        
    def dest(self, path, makedir=False):
        '''
            Internal: Given a root directory that this file would be written to,
            get the full path of where this file belongs.
        '''
        dest = os.path.join(path, str(self))
        dir = os.path.dirname(dest)
        if makedir and not os.path.isdir(dir): os.makedirs(dir)
        return dest
                
    def remove(self):
        '''Remove this file from the dir object to which it belongs.'''
        if self.dir is not None:
            self.dir.remove(self)
        else:
            raise ValueError('Failed to remove file because it doesn\'t belong to any dir.')
