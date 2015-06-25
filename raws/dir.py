import os

from copytree import copytree
from queryable import rawsqueryable, rawsqueryableobj, rawstokenlist
from file import rawsbasefile, rawsotherfile, rawsfile



class rawsdir(rawsqueryableobj):
    '''Represents as a whole all the raws contained within a directory.'''
    
    def __init__(self, path=None, dest=None, version=None, log=None, *args, **kwargs):
        '''Constructor for rawsdir object.'''
        self.files = {}
        self.filenames = {}
        self.path = path
        self.dest = dest
        self.version = version
        self.log = log
        self.hack = None
        if path: self.read(path=path, *args, **kwargs)
        
    def __str__(self):
        return '\n'.join(['%s %s' % (file.kind, str(file)) for file in self.files.itervalues()])
        
    def __enter__(self):
        return self
    def __exit__(self, type, value, traceback):
        if traceback is None and self.path is not None: self.write(path=self.path)
        
    def __getitem__(self, name):
        return self.getfile(name)
    
    def __setitem__(self, name, content):
        if isinstance(content, rawsbasefile):
            if content.dir: content = content.copy()
            content.setpath(name)
            self.add(file=content, replace=True)
        elif isinstance(content, rawsqueryable):
            self.add(file=name, replace=True, tokens=content.tokens())
        elif isinstance(content, basestring):
            self.add(file=name, replace=True, data=content)
        else:
            self.add(file=name, tokens=content)
    
    def __contains__(self, item):
        return str(item) in self.files
        
    def getfile(self, name, create=None):
        '''Gets the file with a given name. If no file by that name is found,
        None is returned instead. If creature is set to something other than
        None, the behavior when no file by some name exists is altered: A new
        file is created and associated with that name, and then its add
        method is called using the value for create as its argument.'''
        
        file = self.files.get(name)
        if file is None:
            file = self.filenames.get(name)
            if file is not None:
                if len(file) == 1:
                    file = file[0]
                else:
                    raise ValueError('Failed to retrieve file from dir because the name found no exact matches, and because multiple files were found with that name.')
                    
        if create is not None and file is None:
            file = self.add(name)
            file.add(create)
        return file
        
    def add(self, file=None, path=None, loc=None, replace=False, **kwargs):
        if file is None:
            if path is None: raise ValueError('Failed to add file to dir because neither a name, path, nor file object was specified.')
            file = rawsfile(path=path, dir=self, **kwargs)
        if isinstance(file, basestring):
            if path:
                rawsfile(name=file, path=path, dir=self, **kwargs)
            else:
                splitloc, name = os.path.split(file)
                name, ext = os.path.splitext(name)
                loc = os.path.join(loc, splitloc) if loc else splitloc
                file = rawsfile(name=name, ext=ext, loc=loc, path=path, dir=self, **kwargs)
        else:
            if file.dir is not self and file.dir is not None:
                raise ValueError('Failed to add file %s to dir because it already belongs to another dir. You probably meant to remove the file first or to add a copy.' % file)
            file.dir = self
        if str(file) in self.files:
            if replace:
                self.remove(file)
            else:
                raise KeyError('Failed to add file %s to dir because it already contains a file by the same name.' % file)
        self.files[str(file)] = file
        if file.name not in self.filenames: self.filenames[file.name] = []
        self.filenames[file.name].append(file)
        return file
        
    def remove(self, file=None):
        if isinstance(file, basestring): file = self.getfile(file)
        if (file not in self.files) or (file.dir is not self): raise KeyError('Failed to remove file %s from dir because it doesn\'t belong to the dir.' % file)
        self.files[str(file)].dir = None
        del self.files[str(file)]
        
    def addfile(self, filename=None, rfile=None, path=None):
        '''Deprecated: As of v1.0.2. Use the add method instead.'''
        return self.add(file=filename if filename is not None else rfile, path=path)
    def removefile(self, name=None, file=None):
        '''Deprecated: As of v1.0.2. Use the remove method instead.'''
        return self.remove(file if file is not None else name)
    
    def read(self, path=None):
        '''Reads raws from all text files in the specified directory.'''
        
        if path is None:
            if self.path is None: raise ValueError('Failed to read dir because no path was specified.')
            path = self.path
        paths = (path,) if isinstance(path, basestring) else path
            
        for path in paths:
            for root, dirs, files in os.walk(path):
                addeddirs = {}
                # Add files
                for name in files:
                    filepath = os.path.join(root, name)
                    file = rawsbasefile.factory(filepath, root=path, dir=self)
                    addeddirs[os.path.abspath(os.path.dirname(filepath))] = True
                    self.add(file)
                # Add empty directories
                for dir in dirs:
                    dir = os.path.abspath(os.path.join(path, dir))
                    if not any([added.startswith(dir) for added in addeddirs.iterkeys()]):
                        file = rawsotherfile(path=dir, root=path, dir=self)
                        self.add(file)
        
    def write(self, path=None):
        '''Writes raws to the specified directory.'''
        
        if path is None:
            if self.path is None and self.dest is None: raise ValueError('Failed to write dir because no path was specified.')
            path = self.dest if self.dest else self.path
        
        if self.log: self.log.debug('Writing %d files to %s.' % (len(self.files), path))
        for file in self.files.itervalues():
            file.write(path)
    
    def tokens(self, *args, **kwargs):
        '''Iterate through all tokens.'''
        for file in self.files.itervalues():
            if isinstance(file, rawsqueryable):
                for token in file.tokens(*args, **kwargs): yield token
                
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
            if isinstance(file, rawsqueryable):
                root = file.root()
                if root is not None and root.value == 'OBJECT' and root.nargs() == 1 and root.args[0] in match_types:
                    results.append(root)
        return results
