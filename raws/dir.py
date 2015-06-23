import os
from copytree import copytree
from queryable import rawsqueryableobj, rawstokenlist
from file import rawsfile, rawsotherfile



class rawsdir(rawsqueryableobj):
    '''Represents as a whole all the raws contained within a directory.'''
    
    def __init__(self, path=None, dest=None, version=None, log=None, *args, **kwargs):
        '''Constructor for rawsdir object.'''
        self.files = {}
        self.otherfiles = []
        self.path = path
        self.dest = dest
        self.version = version
        self.log = log
        self.hack = None
        if path: self.read(path=path, *args, **kwargs)
        
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        if traceback is None and self.path is not None: self.write(path=self.path)
        
    def __getitem__(self, name):
        return self.get(name)
    def __setitem__(self, name, value):
        return self.set(name, value)
    
    def __contains__(self, item):
        if isinstance(item, basestring):
            return item in self.files
        else:
            return item in self.files.itervalues()
        
    def getfile(self, name, create=None):
        '''Gets the file with a given name. If no file by that name is found,
        None is returned instead. If creature is set to something other than
        None, the behavior when no file by some name exists is altered: A new
        file is created and associated with that name, and then its add
        method is called using the value for create as its argument.'''
        
        file = self.files.get(name)
        if create is not None and file is None:
            file = self.add(name)
            file.add(create)
        return file
        
    def add(self, file=None, path=None, replace=False, **kwargs):
        if file is None:
            if path is None: raise ValueError
            file = rawsfile(path=path, dir=self, **kwargs)
        if isinstance(file, basestring):
            file = rawsfile(name=file, path=path, dir=self, **kwargs)
        else:
            if file.dir is self: raise ValueError
            if file.dir is not None: raise ValueError
            file.dir = self
        if (not replace) and file in self.files: raise KeyError('Dir already contains a file by the name %s.' % file)
        self.files[file] = file
        return file
        
    def remove(self, file=None):
        if file not in self.files: raise KeyError
        self.files[file].dir = None
        del self.files[file]
        
    def addfile(self, filename=None, rfile=None, path=None):
        '''Deprecated: As of v1.0.2. Use the add method instead.'''
        raise ValueError
        return self.add(file=filename if filename is not None else rfile, path=path)
        
    def removefile(self, name=None, file=None):
        '''Deprecated: As of v1.0.2. Use the remove method instead.'''
        raise ValueError
        return self.remove(file if file is not None else name)
        
    def read(self, path=None):
        '''Reads raws from all text files in the specified directory.'''
        
        if path is None:
            if self.path is None: raise ValueError
            path = self.path
        paths = (path,) if isinstance(path, basestring) else path
            
        for path in paths:
            for filename in os.listdir(path):
                filepath = os.path.join(path, filename)
                if filename.endswith('.txt') and os.path.isfile(filepath):
                    if self.log: self.log.debug('Reading raws file %s.' % filepath)
                    with open(filepath, 'rb') as file:
                        filenamekey = os.path.splitext(os.path.basename(filename))[0]
                        self.files[filenamekey] = rawsfile(path=filepath, file=file, dir=self)
                else:
                    if self.log: self.log.debug('Found non-raws file %s.' % filepath)
                    self.otherfiles.append(rawsotherfile(filepath, path))
        
    def write(self, path=None):
        '''Writes raws to the specified directory.'''
        
        if path is None:
            if self.path is None and self.dest is None: raise ValueError
            path = self.dest if self.dest else self.path
        
        # Write raws files
        if self.log: self.log.debug('Writing %d raws files to %s.' % (len(self.files), path))
        for file in self.files.itervalues():
            file.write(path)
        
        # Copy other files
        if self.log: self.log.debug('Copying %d other files to %s.' % (len(self.otherfiles), path))
        for file in self.otherfiles:
            file.write(path)
    
    def tokens(self, *args, **kwargs):
        '''Iterate through all tokens.'''
        for filename in self.files:
            for token in self.files[filename].tokens(*args, **kwargs):
                yield token
                
    def getobjheaders(self, type):
        '''Gets OBJECT:X tokens where X is type. Is also prepared for special cases
        like type=ITEM_PANTS matching OBJECT:ITEM.
        
        Example usage:
            >>> objheaders = df.getobjheaders('INORGANIC')
            >>> for token in objheaders: print token; print token.next
            ...
            [OBJECT:INORGANIC]
            [INORGANIC:PLASTER]
            [OBJECT:INORGANIC]
            [INORGANIC:SANDSTONE]
            [OBJECT:INORGANIC]
            [INORGANIC:IRON]
            [OBJECT:INORGANIC]
            [INORGANIC:CLAY]
            [OBJECT:INORGANIC]
            [INORGANIC:ONYX]
            [OBJECT:INORGANIC]
            [INORGANIC:HEMATITE]
        '''
        
        match_types = self.getobjheadername(type)
        results = rawstokenlist()
        for file in self.files.itervalues():
            root = file.root()
            if root is not None and root.value == 'OBJECT' and root.nargs() == 1 and root.args[0] in match_types:
                results.append(root)
        return results
