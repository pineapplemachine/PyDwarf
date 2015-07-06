import os
import shutil

from copytree import copytree
from queryable import rawsqueryable, rawsqueryableobj, rawstokenlist
from file import rawsbasefile, rawsfile, rawsbinfile, rawsreffile



class rawsdir(rawsqueryableobj):
    '''Represents as a whole all the raws contained within a directory.'''
    
    def __init__(self, root=None, dest=None, paths=None, version=None, log=None, **kwargs):
        '''Constructor for rawsdir object.'''
        self.files = {}
        self.filenames = {}
        self.root = root    # Root input directory
        self.dest = dest    # Root output directory
        self.paths = paths  # Only worry about these file paths in input/output directories
        self.version = version
        self.log = log
        if root: self.read(**kwargs)
        
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
            self.add(file=name, replace=True, content=content)
        else:
            self.add(file=name, tokens=content)
    
    def __contains__(self, item):
        if isinstance(item, rawsbasefile):
            return item in self.files.itervalues()
        else:
            return str(item) in self.files or str(item) in self.filenames
        
    def getfile(self, name, create=None, conflicts=False):
        '''Gets the file with a given name. If no file by that name is found,
        None is returned instead. If creature is set to something other than
        None, the behavior when no file by some name exists is altered: A new
        file is created and associated with that name, and then its add
        method is called using the value for create as its argument.'''
        
        if isinstance(name, rawsbasefile):
            return name if name in self.files.itervalues() else None
        
        file = self.files.get(name)
        if file is None:
            file = self.filenames.get(name)
            if file is not None:
                if len(file) == 1:
                    file = file[0]
                else:
                    if not conflicts: raise ValueError('Failed to retrieve file from dir because the name found no exact matches, and because multiple files were found with that name.')
                    return file
                    
        if create is not None and file is None:
            file = self.add(name)
            file.add(create)
        return file
        
    def iterfiles(self, *args, **kwargs):
        return self.files.itervalues(*args, **kwargs)
        
    def add(self, auto=None, **kwargs):
        if auto is not None:
            return self.addbyauto(auto, **kwargs)
        elif 'file' in kwargs:
            return self.addbyfile(**kwargs)
        elif 'dir' in kwargs:
            return self.addbydir(**kwargs)
        elif 'tokens' in kwargs:
            return self.addbytokens(**kwargs)
        elif 'content' in kwargs:
            return self.addbybincontent(**kwargs)
        elif 'name' in kwargs:
            return self.addbyname(**kwargs)
        elif 'path' in kwargs:
            path = kwargs['path']
            if os.path.isfile(path):
                return self.addbyfilepath(**kwargs)
            else:
                return self.addbydirpath(**kwargs)
        elif 'filepath' in kwargs:
            kwargs['path'] = kwargs['filepath']
            del kwargs['filepath']
            return self.addbyfilepath(**kwargs)
        elif 'dirpath' in kwargs:
            kwargs['path'] = kwargs['dirpath']
            del kwargs['dirpath']
            return self.addbydirpath(**kwargs)
        else:
            raise ValueError('Failed to add file because no recognized arguments were specificed.')
        
    def addbyauto(self, auto, **kwargs):
        if isinstance(auto, rawsbasefile):
            return self.addbyfile(auto, **kwargs)
        elif isinstance(auto, basestring):
            if os.path.isfile(auto):
                return self.addbyfilepath(auto, **kwargs)
            elif os.path.isdir(auto):
                return self.addbydirpath(auto, **kwargs)
            else:
                return self.addbyname(auto, **kwargs)
        elif isinstance(auto, rawsdir):
            return self.addbydir(auto, **kwargs)
            
    def addbyfile(self, file, **kwargs):
        self.addfiletodicts(file, **kwargs)
        return file
    def addbyname(self, name, ext=None, loc=None, kind=None, **kwargs):
        file = self.filebyname(name=name, ext=ext, loc=loc, kind=kind)
        self.addfiletodicts(file, **kwargs)
        return file
    def addbyfilepath(self, path, root=None, loc=None, kind=None, **kwargs):
        file = self.filebyfilepath(path=path, root=root, loc=loc, kind=kind)
        self.addfiletodicts(file, **kwargs)
        return file
    def addbydirpath(self, path, root=None, loc=None, kind=None, **kwargs):
        files = self.filesbydirpath(path=path, root=root, loc=loc, kind=kind)
        self.addfilestodicts(files, **kwargs)
        return files
    def addbydir(self, dir, loc=None, **kwargs):
        files = self.filesbydir(dir=dir, loc=loc)
        self.addfilestodicts(files, **kwargs)
        return files
    def addbytokens(self, name, tokens, **kwargs):
        file = self.addbyname(name, **kwargs)
        file.add(tokens)
        return file
    def addbybincontent(self, name, content, **kwargs):
        file = self.addbyname(name, kind=rawsbinfile, **kwargs)
        file.content = content
        return file
        
    def filebyname(self, name, ext=None, loc=None, kind=None):
        if kind is None: kind = rawsfile
        splitloc, name = os.path.split(name)
        if not ext: name, ext = os.path.splitext(name)
        loc = os.path.join(loc, splitloc) if loc else splitloc
        return kind(name=name, ext=ext, loc=loc, dir=self)
    def filebyfilepath(self, path, root=None, loc=None, kind=None):
        if kind is None: kind = rawsfile
        return kind(path=path, loc=loc, dir=self) 
    def filesbydirpath(self, path, root=None, loc=None, kind=None):
        for walkroot, walkdirs, walkfiles in os.walk(path):
            return ((kind if kind else rawsbasefile.factory)(path=os.path.join(walkroot, walkfile), root=root, loc=loc, dir=self) for walkfile in walkfiles)
    def filesbydir(self, dir, loc=None):
        for dirfile in dir.files.iteritems():
            newfile = dirfile.copy()
            newfile.dir = self
            newfile.reloc(loc)
            yield newfile
        
    def addtodicts(self, file, replace=False):
        if isinstance(file, rawsbasefile):
            self.addfiletodicts(file)
        else:
            self.addfilestodicts(file)
    def addfilestodicts(self, files, replace=False):
        for file in files: self.addfiletodicts(file, replace)
    def addfiletodicts(self, file, replace=False):
        '''Internal: Used to add a file to files and filenames dictionaries.'''
        
        if file.dir is not self and file.dir is not None:
            raise ValueError('Failed to add file %s to dir because it already belongs to another dir. You probably meant to remove the file first or to add a copy.' % file)
        
        if str(file) in self.files:
            if not replace: raise KeyError('Failed to add file %s to dir because it already contains a file by the same name.' % file)
            self.remove(self.files[str(file)])
            
        file.dir = self
        
        self.files[str(file)] = file
        
        if file.name not in self.filenames: self.filenames[file.name] = []
        self.filenames[file.name].append(file)
        
    def remove(self, file=None):
        if isinstance(file, basestring): file = self.getfile(file)
        if (file is None) or (file.dir is not self) or not any(file is f for f in self.iterfiles()): raise KeyError('Failed to remove file %s from dir because it doesn\'t belong to the dir.' % file)
        self.filenames[file.name].remove(file)
        self.files[str(file)].dir = None
        del self.files[str(file)]
        
    def addfile(self, filename=None, rfile=None, path=None):
        '''Deprecated: As of v1.0.2. Use the add method instead.'''
        return self.add(file=filename if filename is not None else rfile, path=path)
    def removefile(self, name=None, file=None):
        '''Deprecated: As of v1.0.2. Use the remove method instead.'''
        return self.remove(file if file is not None else name)
    
    def read(self, root=None, paths=None):
        '''Reads raws from all text files in the specified directory.'''
        
        if root is None:
            if self.root is None: raise ValueError('Failed to read dir because no root directory was specified.')
            root = self.root
        
        if paths is None: paths = self.paths
        if paths is not None:
            paths = (paths,) if isinstance(paths, basestring) else paths
        else:
            paths = os.listdir(root)
        
        addeddirs = {}
            
        for path in paths:
            path = os.path.join(root, path)
            
            if os.path.isdir(path):
                for walkroot, walkdirs, walkfiles in os.walk(path):
                    
                    # Add files
                    for name in walkfiles:
                        filepath = os.path.join(walkroot, name)
                        file = rawsbasefile.factory(filepath, root=root, dir=self)
                        addeddirs[os.path.abspath(os.path.dirname(filepath)).replace('\\', '/')] = True
                        self.add(file)
                    
                    # Add empty directories
                    for dir in walkdirs:
                        dir = os.path.abspath(os.path.join(walkroot, dir)).replace('\\', '/')
                        if not any([added.startswith(dir) for added in addeddirs.iterkeys()]):
                            file = rawsbasefile.factory(path=dir, root=root, dir=self)
                            self.add(file)
            
            elif os.path.isfile(path):
                file = rawsbasefile.factory(path, root=root, dir=self)
                addeddirs[os.path.abspath(os.path.dirname(path))] = True
                self.add(file)
                
            else:
                raise ValueError('Failed to read dir because a bad path %s was provided.' % path)
        
    def write(self, dest=None):
        '''Writes raws to the specified directory.'''
        dest = self.getdestforfileop(dest)
        if self.log: self.log.debug('Writing %d files to %s.' % (len(self.files), dest))
        for file in self.files.itervalues():
            file.write(dest)
            
    def clean(self, dest=None):
        dest = self.getdestforfileop(dest)
        if self.log: self.log.debug('Cleaning files in %s.' % dest)
        for path in self.paths:
            path = os.path.join(dest, path)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            
    def getdestforfileop(self, dest, exception=True):
        '''Internal'''
        if dest is None:
            dest = self.dest if self.dest else self.root
            if exception and dest is None: raise ValueError('Failed to write dir because no destination path was specified.')
        return dest
    
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
