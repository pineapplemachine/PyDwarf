import os
import traceback

import forward



@forward.declare
class basefile(object):
    '''Base class for file objects.'''
    
    def __init__(self):
        self.dir = None
        self.path = None
        self.rootpath = None
        self.loc = None
        self.name = None
        self.ext = None
        self.kind = None
    
    def __str__(self):
        name = ''.join((self.name, self.ext)) if self.ext and self.name else self.name
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
        return self.path
        
    def setpath(self, path, root=None, loc=None, name=None, ext=None):
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
        return self.ext
        
    def setext(self, ext):
        if '.' in ext: raise ValueError('Failed to set file extension to "%s" because the string contains a period.')
        self.ext = ext
        
    def getloc(self):
        return self.loc
    
    def setloc(self, loc):
        self.loc = loc
        
    def reloc(self, loc):
        if loc and self.loc:
            self.loc = os.path.join(loc, self.loc)
        elif loc:
            self.loc = loc
        
    def dest(self, path, makedir=False):
        '''Internal: Given a root directory that this file would be written to, get the full path of where this file belongs.'''
        dest = os.path.join(path, str(self))
        dir = os.path.dirname(dest)
        if makedir and not os.path.isdir(dir): os.makedirs(dir)
        return dest
                
    def remove(self):
        '''Remove this file from the raws.dir object to which it belongs.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> print dwarf
            [CREATURE:DWARF]
            >>> print dwarf.file
            creature_standard
            >>> dwarf.file.remove()
            >>> print df.getobj('CREATURE:DWARF')
            None
            >>> print df.getfile('creature_standard')
            None
        '''
        if self.dir is not None:
            self.dir.remove(self)
        else:
            raise ValueError('Failed to remove file because it doesn\'t belong to any dir.')
