import os
import shutil

import forward

from basefile import basefile
from copytree import copytree



@forward.declare
class reffile(basefile):
    def __init__(self, path=None, dir=None, root=None, **kwargs):
        self.dir = dir
        self.setpath(path, root, **kwargs)
        self.kind = 'ref'
    
    def copy(self):
        copy = rawsotherfile()
        copy.path = self.path
        copy.dir = self.dir
        copy.rootpath = self.rootpath
        copy.name = self.name
        copy.ext = self.ext
        copy.loc = self.loc
        return copy
    
    def ref(self, **kwargs):
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        return self
    def bin(self, **kwargs):
        self.kind = 'bin'
        self.__class__ = forward.declare.binfile
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.read()
        return self
    def raw(self, **kwargs):
        self.kind = 'raw'
        self.__class__ = forward.declare.rawfile
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.read()
        return self
    
    def write(self, path):
        dest = self.dest(path, makedir=True)
        if self.path != dest:
            if os.path.isfile(self.path):
                shutil.copy2(self.path, dest)
            elif os.path.isdir(self.path):
                copytree(self.path, dest)
            else:
                raise ValueError('Failed to write file because its path %s refers to neither a file nor a directory.' % self.path)
