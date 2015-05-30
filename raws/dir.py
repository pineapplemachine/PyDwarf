import os
from queryable import rawsqueryable_obj
from file import rawsfile

class rawsdir(rawsqueryable_obj):
    '''Represents as a whole all the raws contained within a directory.'''
    
    def __init__(self, **kwargs):
        '''Constructor for rawsdir object.'''
        self.files = {}
        if len(kwargs): self.read(**kwargs)
        
    def getfile(self, filename):
        return self.files.get(filename)
    def addfile(self, filename=None, rfile=None, path=None):
        if path is not None:
            return self.addpath(path)
        else:
            if rfile and not filename: filename = rfile.header
            if filename in self.files: raise KeyError
            if not rfile: rfile = rawsfile(header=filename)
            self.files[filename] = rfile
            rfile.dir = self
            return rfile
    def setfile(self, filename=None, rfile=None):
        if rfile and not filename: filename = rfile.header
        rfile.dir = self
        self.files[filename] = rfile
    def removefile(self, filename=None, rfile=None):
        if not rfile.dir == self: raise ValueError
        if rfile and not filename: filename = rfile.header
        rfile.dir = None
        del self.files[filename]
        
    def addpath(self, path):
        with open(path, 'rb') as rfilestream:
            rfile = rawsfile(path=path, rfile=rfilestream, dir=self)
            if rfile.header in self.files: raise ValueError
            self.files[rfile.header] = rfile
            return rfile
        
    def __getitem__(self, name): return self.getfile(name)
    def __setitem__(self, name, value): return self.setfile(name, value)
    
    def read(self, path, log=None):
        '''Reads raws from all text files in the specified directory.'''
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if filename.endswith('.txt') and os.path.isfile(filepath
                ):
                if log: log.debug('Reading file %s...' % filepath)
                with open(filepath, 'rb') as rfile:
                    filenamekey = os.path.splitext(os.path.basename(filename))[0]
                    self.files[filenamekey] = rawsfile(path=filepath, rfile=rfile, dir=self)
        return self
        
    def write(self, path, log=None):
        '''Writes raws to the specified directory.'''
        for filename in self.files:
            filepath = os.path.join(path, filename)
            if not filepath.endswith('.txt'): filepath += '.txt'
            with open(filepath, 'wb') as rfile:
                if log: log.debug('Writing file %s...' % filepath)
                self.files[filename].write(rfile)
        return self
    
    def tokens(self):
        '''Iterate through all tokens.'''
        for filename in self.files:
            for token in self.files[filename].tokens():
                yield token
