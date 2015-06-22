import os
import shutil
from queryable import rawsqueryable_obj, rawstokenlist
from file import rawsfile



class rawsdir(rawsqueryable_obj):
    '''Represents as a whole all the raws contained within a directory.'''
    
    def __init__(self, *args, **kwargs):
        '''Constructor for rawsdir object.'''
        
        self.files = {}
        self.otherfiles = []
        if len(args) or len(kwargs): self.read(*args, **kwargs)
        
    def getfile(self, filename, create=None):
        '''Gets the file with a given name. If no file by that name is found,
        None is returned instead. If creature is set to something other than
        None, the behavior when no file by some name exists is altered: A new
        file is created and associated with that name, and then its add
        method is called using the value for create as its argument.'''
        
        rfile = self.files.get(filename)
        if create is not None and rfile is None:
            rfile = self.addfile(filename)
            rfile.add(create)
        return rfile
        
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
    def __contains__(self, name): return name in self.files
    
    def read(self, path, log=None):
        '''Reads raws from all text files in the specified directory.'''
        for filename in os.listdir(path):
            filepath = os.path.join(path, filename)
            if filename.endswith('.txt') and os.path.isfile(filepath):
                if log: log.debug('Reading raws file %s.' % filepath)
                with open(filepath, 'rb') as rfile:
                    filenamekey = os.path.splitext(os.path.basename(filename))[0]
                    self.files[filenamekey] = rawsfile(path=filepath, rfile=rfile, dir=self)
            else:
                if log: log.debug('Found non-raws file %s.' % filepath)
                self.otherfiles.append((path, filename))
        
    def write(self, path, log=None):
        '''Writes raws to the specified directory.'''
        
        # Write raws files
        for filename in self.files:
            filepath = os.path.join(path, filename)
            if not filepath.endswith('.txt'): filepath += '.txt'
            with open(filepath, 'wb') as rfile:
                if log: log.debug('Writing raws file %s.' % filepath)
                self.files[filename].write(rfile)
        # Copy other files
        for filepath, filename in self.otherfiles:
            if filepath != path:
                originalpath = os.path.join(filepath, filename)
                writepath = os.path.join(path, filename)
                if log: log.debug('Writing non-raws file %s.' % writepath)
                if os.path.isfile(originalpath):
                    shutil.copy2(originalpath, writepath)
                elif os.path.isdir(originalpath):
                    copytree(originalpath, writepath)
                elif log:
                    log.error('Failed to write non-raws file %s: it\'s neither a file nor a directory.' % writepath)
    
    def tokens(self):
        '''Iterate through all tokens.'''
        for filename in self.files:
            for token in self.files[filename].tokens():
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
        for rfile in self.files.itervalues():
            root = rfile.root()
            if root is not None and root.value == 'OBJECT' and root.nargs() == 1 and root.args[0] in match_types:
                results.append(root)
        return results



# credit belongs to http://stackoverflow.com/a/13814557/3478907
def copytree(src, dst, symlinks=False, ignore=None):
    if not os.path.exists(dst):
        os.makedirs(dst)
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copytree(s, d, symlinks, ignore)
        else:
            if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                shutil.copy2(s, d)
