#!/usr/bin/env python
# coding: utf-8

import os
import shutil

import copytree
import queryable
import tokenlist
import queryableobj
import basefile
import reffile
import binfile
import rawfile
import filefactory



class dir(queryableobj.queryableobj):
    '''Represents files contained within a Dwarf Fortress directory.'''
    
    def __init__(self, root=None, dest=None, paths=None, version=None, log=None, **kwargs):
        '''Initialize a dir object.'''
        self.files = {}
        self.filenames = {}
        self.root = root    # Root input directory
        self.dest = dest    # Root output directory
        self.paths = paths  # Only worry about these file paths in input/output directories
        self.version = version
        self.log = log # TODO: take this out, it doesn't belong here. move logging statements to session or get rid of them entirely.
        if root: self.read(**kwargs)
        
    def __str__(self):
        '''Get a string representation.'''
        return '\n'.join(['%s %s' % (file.kind, str(file)) for file in self.files.itervalues()])
        
    def __enter__(self):
        '''Support for with/as syntax.'''
        return self
    def __exit__(self, type, value, traceback):
        '''Support for with/as syntax.'''
        if traceback is None and self.root is not None: self.write(self.root)
        
    def __getitem__(self, name):
        '''Get member file by name or full relative path.'''
        return self.getfile(name)
    
    def __setitem__(self, name, content):
        '''Set file given a name.'''
        if isinstance(content, basefile.basefile):
            if content.dir: content = content.copy()
            content.setpath(name)
            self.add(file=content, replace=True)
        elif isinstance(content, queryable.queryable):
            self.add(file=name, replace=True, tokens=content.tokens())
        elif isinstance(content, basestring):
            self.add(file=name, replace=True, content=content)
        else:
            self.add(file=name, tokens=content)
    
    def __contains__(self, item):
        '''Check if the dir contains a file name or object.'''
        if isinstance(item, basefile.basefile):
            return item in self.files.itervalues()
        else:
            return any(item is file for file in self.iterfiles())
            
    def __len__(self):
        '''Get the number of file objects tracked by the dir.'''
        return len(self.files)
        
    def __nonzero__(self):
        '''Always returns True.'''
        return True
            
    def __eq__(self, other):
        '''Check equivalency with another dir object.'''
        return self.equals(other)
    def __ne__(self, other):
        '''Check inequivalency with another dir object.'''
        return not self.equals(other)
        
    def __iadd__(self, file):
        '''Add a file to the dir.'''
        self.add(file=file)
        
    def equals(self, other):
        '''Check equivalency with another dir object.'''
        if len(self.files) == len(other.files):
            for file in self.iterfiles():
                matchingfile = other.getfile(str(file))
                if not(matchingfile and file == matchingfile): return False
            return True
        else:
            return False
        
    def getfile(self, name, create=None, conflicts=False, **kwargs):
        '''Gets the file with a given name. If no file by that name is found,
        None is returned instead. If creature is set to something other than
        None, the behavior when no file by some name exists is altered: A new
        file is created and associated with that name, and then its add
        method is called using the value for create as its argument.'''
        
        if isinstance(name, basefile.basefile):
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
            file = self.add(name, **kwargs)
            file.add(create)
        return file
        
    def iterfiles(self, *args, **kwargs):
        '''Iterate through the dir's file objects.'''
        return self.files.itervalues(*args, **kwargs)
        
    def add(self, auto=None, **kwargs):
        '''Add a file to the dir.'''
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
            elif os.path.isdir(path):
                return self.addbydirpath(**kwargs)
            else:
                raise ValueError('Failed to add file because the path %s refers to neither a file nor a directory.' % path)
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
        '''Internal: Add a file when given an 'auto' argument.'''
        if isinstance(auto, basefile.basefile):
            return self.addbyfile(auto, **kwargs)
        elif isinstance(auto, basestring):
            if os.path.isfile(auto):
                return self.addbyfilepath(auto, **kwargs)
            elif os.path.isdir(auto):
                return self.addbydirpath(auto, **kwargs)
            else:
                return self.addbyname(auto, **kwargs)
        elif isinstance(auto, dir):
            return self.addbydir(auto, **kwargs)
        else:
            try:
                self.addbytokens(auto, **kwargs)
            except:
                return ValueError('Failed to add file because the argument type %s was unrecognized.' % type(auto))
            
    def addbyfile(self, file, **kwargs):
        '''Internal: Add a file when given a 'file' argument.'''
        self.addfiletodicts(file, **kwargs)
        return file
    def addbyname(self, name, ext=None, loc=None, kind=None, **kwargs):
        '''Internal: Add a file when given a 'name' argument.'''
        file = self.filebyname(name=name, ext=ext, loc=loc, kind=kind)
        self.addfiletodicts(file, **kwargs)
        return file
    def addbyfilepath(self, path, root=None, loc=None, kind=None, **kwargs):
        '''Internal: Add a file when given a 'filepath' argument.'''
        file = self.filebyfilepath(path=path, root=root, loc=loc, kind=kind)
        self.addfiletodicts(file, **kwargs)
        return file
    def addbydirpath(self, path, root=None, loc=None, kind=None, **kwargs):
        '''Internal: Add a file when given a 'dirpath' argument.'''
        files = self.filesbydirpath(path=path, root=root, loc=loc, kind=kind)
        self.addfilestodicts(files, **kwargs)
        return files
    def addbydir(self, dir, loc=None, **kwargs):
        '''Internal: Add a file when given a 'dir' argument.'''
        files = self.filesbydir(dir=dir, loc=loc)
        self.addfilestodicts(files, **kwargs)
        return files
    def addbytokens(self, name, tokens, **kwargs):
        '''Internal: Add a file when given a 'tokens' argument.'''
        file = self.addbyname(name, **kwargs)
        file.add(tokens)
        return file
    def addbybincontent(self, name, content, **kwargs):
        '''Internal: Add a file when given a 'content' argument.'''
        file = self.addbyname(name, kind=binfile.binfile, **kwargs)
        file.content = content
        return file
        
    def filebyname(self, name, ext=None, loc=None, kind=None):
        '''Internal: Create a file object to be added to the dir.'''
        if kind is None: kind = rawfile.rawfile
        splitloc, name = os.path.split(name)
        if not ext: name, ext = os.path.splitext(name)
        loc = os.path.join(loc, splitloc) if loc else splitloc
        return kind(name=name, ext=ext, loc=loc, dir=self)
    def filebyfilepath(self, path, root=None, loc=None, kind=None):
        '''Internal: Create a file object to be added to the dir.'''
        if kind is None: kind = rawfile.rawfile
        return kind(path=path, loc=loc, dir=self) 
    def filesbydirpath(self, path, root=None, loc=None, kind=None):
        '''Internal: Create a file object to be added to the dir.'''
        for walkroot, walkdirs, walkfiles in os.walk(path):
            for walkfile in walkfiles:
                if kind:
                    return kind(path=os.path.join(walkroot, walkfile), root=root, loc=loc, dir=self)
                else:
                    return filefactory.filefactory(path=os.path.join(walkroot, walkfile), root=root, loc=loc, dir=self)
    def filesbydir(self, dir, loc=None):
        '''Internal: Create multiple file objects to be added to the dir.'''
        for dirfile in dir.files.iteritems():
            newfile = dirfile.copy()
            newfile.dir = self
            newfile.reloc(loc)
            yield newfile
        
    def addtodicts(self, file, replace=False):
        '''Internal: Used to add a file or files to files and filenames dicts.'''
        if isinstance(file, basefile.basefile):
            self.addfiletodicts(file)
        else:
            self.addfilestodicts(file)
    def addfilestodicts(self, files, replace=False):
        '''Internal: Used to add multiple files to files and filenames dicts at once.'''
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
        '''Remove a file from this dir.'''
        
        if file is None: raise KeyError('Failed to remove file because no file was given.')
        if isinstance(file, basestring): file = self.getfile(file)
        
        if file.dir is not self: raise KeyError('Failed to remove file because it belongs to a different dir.')
        if not any(file is f for f in self.iterfiles()): raise KeyError('Failed to remove file because it doesn\'t belong to this dir.')
        
        filenamelist = self.filenames[file.name]
        for index, filenameentry in enumerate(filenamelist):
            if file is filenameentry:
                del filenamelist[index]
                break
        
        self.files[str(file)].dir = None
        del self.files[str(file)]
        
    def addfile(self, filename=None, rfile=None, path=None):
        '''Deprecated: As of v1.0.2. Use the add method instead.'''
        return self.add(file=filename if filename is not None else rfile, path=path)
    def removefile(self, name=None, file=None):
        '''Deprecated: As of v1.0.2. Use the remove method instead.'''
        return self.remove(file if file is not None else name)
    
    def read(self, root=None, paths=None, skipfails=False):
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
                        file = filefactory.filefactory(filepath, root=root, dir=self)
                        addeddirs[os.path.abspath(os.path.dirname(filepath)).replace('\\', '/')] = True
                        self.add(file)
                    
                    # Add empty directories
                    for dir in walkdirs:
                        dir = os.path.abspath(os.path.join(walkroot, dir)).replace('\\', '/')
                        if not any([added.startswith(dir) for added in addeddirs.iterkeys()]):
                            file = filefactory.filefactory(path=dir, root=root, dir=self)
                            self.add(file)
            
            elif os.path.isfile(path):
                file = filefactory.filefactory(path, root=root, dir=self)
                addeddirs[os.path.abspath(os.path.dirname(path))] = True
                self.add(file)
                
            elif skipfails:
                raise ValueError('Failed to read dir because a bad path %s was provided.' % path)
        
    def write(self, dest=None):
        '''Writes raws to the specified directory.'''
        dest = self.getdestforfileop(dest)
        if self.log: self.log.debug('Writing %d files to %s.' % (len(self.files), dest))
        for file in self.files.itervalues():
            try:
                file.write(dest)
            except:
                if self.log: self.log.exception('Failed to write file %s to %s.' % (file, dest))
            
    def clean(self, dest=None):
        '''
            Cleans an output directory, typically before writing, so that files
            that are present in the output directory but not in the dir object
            won't stick around and interfere with things.
        '''
        dest = self.getdestforfileop(dest)
        if self.log: self.log.debug('Cleaning files in %s.' % dest)
        for path in self.paths:
            path = os.path.join(dest, path)
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
                
    def copy(self):
        '''Create a copy of this dir.'''
        copy = dir()
        copy.root = self.root
        copy.dest = self.dest
        copy.paths = self.paths
        copy.version = self.version
        copy.log = self.log
        for file in self.iterfiles():
            copy.add(file=file.copy())
        return copy
            
    def clear(self):
        '''Remove all files from this dir.'''
        for file in self.files.values(): self.remove(file)
        self.files = {}
        self.filenames = {}
        
    def reset(self):
        '''
            Reload the dir object from its associated directory, consequently
            discarding all changes.
        '''
        self.clear()
        self.read()
            
    def getdestforfileop(self, dest, exception=True):
        '''Internal: Wonky method for determining a true destination path given one provided as an argument'''
        if dest is None:
            dest = self.dest if self.dest else self.root
            if exception and dest is None: raise ValueError(
                'Failed to write dir because no destination path was specified.'
            )
        return dest
    
    def itokens(self, *args, **kwargs):
        '''Iterate through all tokens.'''
        for file in self.files.itervalues():
            if isinstance(file, queryable.queryable):
                for token in file.tokens(*args, **kwargs):
                    yield token
                
    def getobjheaders(self, type=None):
        '''
            Gets OBJECT:X tokens where X is type. Is also prepared for special
            cases like type=ITEM_PANTS matching OBJECT:ITEM.
        '''
        
        match_types = self.getobjheadername(type)
        results = tokenlist.tokenlist()
        for file in self.files.itervalues():
            if isinstance(file, queryable.queryable):
                root = file.root()
                if root is not None and root.value == 'OBJECT' and root.nargs() == 1 and root.args[0] in match_types:
                    results.append(root)
        return results
