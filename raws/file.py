import os
import re
import shutil
import traceback

from copytree import copytree
from queryable import rawstokenlist
from queryableobj import rawsqueryableobj
from token import rawstoken



class rawsbasefile(object):
    def __init__(self):
        self.dir = None
        self.path = None
        self.rootpath = None
        self.loc = None
        self.name = None
        self.ext = None
        self.kind = None
    
    @staticmethod
    def factory(path, **kwargs): # TODO: move this elsewhere and make it more easily configurable
        basename = os.path.basename(path)
        try:
            if basename.endswith('.txt'):
                with open(path, 'rb') as txt:
                    if txt.readline().strip() == os.path.splitext(os.path.basename(path))[0]:
                        txt.seek(0)
                        return rawsfile(path=path, file=txt, **kwargs)
            elif basename in ('dfhack.init', 'dfhack.init-example'):
                return rawsbinfile(path=path, **kwargs)
            elif basename in ('init.txt', 'd_init.txt', 'colors.txt', 'interface.txt', 'announcements.txt', 'world_gen.txt', 'overrides.txt'):
                return rawsfile(path=path, file=txt, noheader=True, **kwargs)
        except Exception as e:
            pydwarf.log.warning('Failed to read file from path %s. Defauling to reading as a reffile, which should (hopefully) work despite.' % path)
            pydwarf.log.debug(traceback.format_exc())
        finally:
            return rawsreffile(path=path, **kwargs)
    
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
        


class rawsreffile(rawsbasefile):
    def __init__(self, path=None, dir=None, root=None, **kwargs):
        self.dir = dir
        self.setpath(path, root, **kwargs)
    
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
        self.__class__ = rawsbinfile
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.read()
        return self
    def raw(self, **kwargs):
        print '!!!'
        self.kind = 'raw'
        self.__class__ = rawsfile
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



class rawsbinfile(rawsreffile):
    def __init__(self, content=None, path=None, dir=None, **kwargs):
        self.dir = None
        self.setpath(path, **kwargs)
        self.dir = dir
        self.content = content
        if self.content is None and self.path is not None and os.path.isfile(self.path): self.read(self.path)
        
    def read(self, path=None):
        with open(path if path else self.path, 'rb') as binfile: self.content = binfile.read()
        
    def ref(self, **kwargs):
        raise ValueError('Failed to cast binfile %s to a reffile because it is an invalid conversion.' % self)
    def bin(self, **kwargs):
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        return self
    def raw(self, **kwargs):
        self.kind = 'raw'
        self.__class__ = rawsfile
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.read(content=self.content)
        return self
        
    def copy(self):
        copy = rawsbinfile()
        copy.path = self.path
        copy.dir = self.dir
        copy.rootpath = self.rootpath
        copy.name = self.name
        copy.ext = self.ext
        copy.loc = self.loc
        copy.content = self.content
        return copy
    
    def __repr__(self):
        return str(self.content)
        
    def __len__(self):
        return len(self.content)
        
    def write(self, path):
        dest = self.dest(path, makedir=True)
        with open(dest, 'wb') as file:
            file.write(self.content)
            
    def add(self, content):
        self.content += content



class rawsfile(rawsbasefile, rawsqueryableobj):
    '''Represents a single file within a raws directory.'''
    
    def __init__(self, name=None, file=None, path=None, root=None, content=None, tokens=None, dir=None, readpath=True, noheader=False, **kwargs):
        '''Constructs a new raws file object.
        
        name: The name string to appear at the top of the file. Also used to determine filename.
        data: A string to be parsed into token data.
        path: A path to the file from which this object is being parsed, if any exists.
        tokens: An iterable of tokens from which to construct the object; these tokens will be its initial contents.
        file: A file-like object from which to automatically read the name and data attributes.
        dir: Which raws.dir object this file belongs to.
        '''
        
        self.dir = dir
        self.data = None
        self.noheader = noheader
        self.setpath(path=path, root=root, **kwargs)
        
        self.roottoken = None
        self.tailtoken = None
        
        if file:
            self.read(file)
        elif path and readpath:
            self.read(path)
            
        if name is not None: self.name = name
        
        if content is not None:
            self.read(content=content)
        elif tokens is not None:
            self.settokens(tokens, setfile=True)
        
        if name: self.name = name
        
        if (not self.path) and (not self.ext): self.ext = '.txt'
        self.kind = 'raw'
            
    def __enter__(self):
        return self
    def __exit__(self):
        if self.path: self.write(self.path)
            
    def __eq__(self, other):
        return self.equals(other)
    def __ne__(self, other):
        return not self.equals(other)
        
    def __len__(self):
        return self.length()
        
    def __nonzero__(self):
        return True
        
    def __repr__(self):
        return self.content()
        
    def content(self):
        tokencontent = ''.join([repr(o) for o in self.tokens()])
        if self.noheader:
            return tokencontent
        else:
            return '%s\n%s' %(self.name, tokencontent)
        
    def ref(self, **kwargs):
        raise ValueError('Failed to cast rawfile %s to reffile because it is an invalid conversion.' % self)
    def bin(self, **kwargs):
        self.kind = 'bin'
        self.__class__ =  rawsbinfile
        content = kwargs.get('content', self.content())
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        self.content = content
        return self
    def raw(self, **kwargs):
        for key, value in kwargs.iteritems(): self.__dict__[key] = value
        return self
    
    def index(self, index):
        itrtoken = self.root() if index >= 0 else self.tail()
        index += (index < 0)
        for i in xrange(0, abs(index)):
            itrtoken = itrtoken.next if index > 0 else itrtoken.prev
            if itrtoken is None: return None
        return itrtoken
        
    def getpath(self):
        return self.path
        
    def getname(self):
        '''Get the file name.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> creature_standard = dwarf.file
            >>> print creature_standard.getname()
            creature_standard
            >>> creature_standard.setheader('example_header')
            >>> print creature_standard.getname()
            example_header
        '''
        return self.name
    def setname(self, name):
        '''Set the file name.
        
        Example usage:
            >>> dwarf = df.getobj('CREATURE:DWARF')
            >>> creature_standard = dwarf.file
            >>> print creature_standard.getname()
            creature_standard
            >>> creature_standard.setheader('example_header')
            >>> print creature_standard.getname()
            example_header
        '''
        self.name = name
            
    def settokens(self, tokens, setfile=True):
        '''Internal: Utility method for setting the root and tail tokens given an iterable.'''
        self.roottoken, self.tailtoken = rawstoken.firstandlast(tokens, self if setfile else None)
    
    def copy(self):
        '''Makes a copy of a file and its contents.
        
        Example usage:
            >>> item_food = df.getfile('item_food')
            >>> food_copy = item_food.copy()
            >>> print item_food is food_copy
            False
            >>> print item_food == food_copy
            True
            >>> food_copy.add('EXAMPLE:TOKEN')
            [EXAMPLE:TOKEN]
            >>> print food_copy.list()
            [OBJECT:ITEM]
            [ITEM_FOOD:ITEM_FOOD_BISCUITS]
            [NAME:biscuits]
            [LEVEL:2]
            [ITEM_FOOD:ITEM_FOOD_STEW]
            [NAME:stew]
            [LEVEL:3]
            [ITEM_FOOD:ITEM_FOOD_ROAST]
            [NAME:roast]
            [LEVEL:4][EXAMPLE:TOKEN]
            >>> print item_food == food_copy
            False
        '''
        copy = rawsfile()
        copy.path = self.path
        copy.rootpath = self.rootpath
        copy.name = self.name
        copy.ext = self.ext
        copy.loc = self.loc
        copy.noheader = self.noheader
        copy.settokens(rawstoken.copy(self.tokens()))
        return copy
        
    def equals(self, other):
        return rawstoken.tokensequal(self.tokens(), other.tokens())
        
    def root(self):
        '''Gets the first token in the file.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> print creature_standard.root()
            [OBJECT:CREATURE]
        '''
        while self.roottoken is not None and self.roottoken.prev is not None: self.roottoken = self.roottoken.prev
        return self.roottoken
    def tail(self):
        '''Gets the last token in the file.
        
        Example usage:
            >>> creature_standard = df.getfile('creature_standard')
            >>> print creature_standard.tail()
            [MULTIPLY_VALUE:15]
        '''
        while self.tailtoken is not None and self.tailtoken.next is not None: self.tailtoken = self.tailtoken.next
        return self.tailtoken
        
    def tokens(self, reverse=False, **kwargs):
        '''Iterate through all tokens.
        
        reverse: If False, starts from the first token and iterates forwards. If True,
            starts from the last token and iterates backwards. Defaults to False.
        **kwargs: Other named arguments are passed on to the raws.token.tokens method.
        '''
        if reverse:
            tail = self.tail()
            if tail is None: return
            generator = tail.tokens(include_self=True, reverse=True, **kwargs)
        else:
            root = self.root()
            if root is None: return
            generator = root.tokens(include_self=True, **kwargs)
        for token in generator:
            yield token
            
    def read(self, file=None, content=None, **kwargs):
        '''Given a path or file-like object, reads name and data.'''
        self.roottoken = None
        self.tailtoken = None 
        
        if file is None and content is None:
            with open(self.path, 'rb') as src:
                content = src.read()
        elif isinstance(file, basestring):
            self.path = file
            self.ext = os.path.splitext(file)[1]
            with open(file, 'rb') as src:
                content = src.read()
        else:
            content = file.read()
        
        if content:
            parts = content.split('\n', 1)
            header = None
            data = None
            if len(parts) == 1:
                data = parts[0]
            elif len(parts) == 2:
                header, data = parts
            header = header.strip()
            if self.name:
                if header != self.name: self.noheader = True
            if data:
                self.settokens(rawstoken.parse(data, file=self))
        else:
            self.noheader = True
            self.data = None
            
    def write(self, file):
        '''Given a path to a directory or a file-like object, writes the file's contents to that file.'''
        if isinstance(file, basestring):
            with open(self.dest(file, makedir=True), 'wb') as dest:
                dest.write(self.content())
        else:
            file.write(self.content())
    
    def add(self, *args, **kwargs):
        '''Adds tokens to the end of a file.
        
        Example usage:
            >>> item_food = df.getfile('item_food')
            >>> print item_food.list()
            [OBJECT:ITEM]
            [ITEM_FOOD:ITEM_FOOD_BISCUITS]
            [NAME:biscuits]
            [LEVEL:2]
            [ITEM_FOOD:ITEM_FOOD_STEW]
            [NAME:stew]
            [LEVEL:3]
            [ITEM_FOOD:ITEM_FOOD_ROAST]
            [NAME:roast]
            [LEVEL:4]
            >>> tokens = item_food.add('hi! [THIS][IS][AN][EXAMPLE]')
            >>> print tokens
            hi! [THIS][IS][AN][EXAMPLE]
            >>> print item_food.list()
            [OBJECT:ITEM]
            [ITEM_FOOD:ITEM_FOOD_BISCUITS]
            [NAME:biscuits]
            [LEVEL:2]
            [ITEM_FOOD:ITEM_FOOD_STEW]
            [NAME:stew]
            [LEVEL:3]
            [ITEM_FOOD:ITEM_FOOD_ROAST]
            [NAME:roast]
            [LEVEL:4]hi! [THIS][IS][AN][EXAMPLE]
        '''
        tail = self.tail()
        if tail:
            return tail.add(*args, **kwargs)
        else:
            token, tokens = rawstoken.autovariable(*args, **kwargs)
            if token is not None:
                self.roottoken = token
                self.tailtoken = token
                token.file = self
                return token
            elif tokens is not None:
                self.settokens(tokens)
                return tokens
        
    def length(self, *args, **kwargs):
        '''Get the number of tokens in this file.
        
        Example usage:
            >>> print df.getfile('creature_standard').length()
            5516
            >>> print df.getfile('inorganic_metal').length()
            1022
            >>> print df.getfile('item_pants').length()
            109
        '''
        return sum(1 for token in self.tokens(*args, **kwargs))
        
    def clear(self):
        '''Remove all tokens from this file.
        
        Example usage:
            >>> item_pants = df.getfile('item_pants')
            >>> print item_pants.length()
            109
            >>> item_pants.clear()
            >>> print item_pants.length()
            0
        '''
        for token in self.tokens(): token.file = None
        self.roottoken = None
        self.tailtoken = None
        
    def getobjheaders(self, type):
        match_types = self.getobjheadername(type)
        root = self.root()
        return (root,) if root is not None and root.value == 'OBJECT' and root.nargs(1) and root.args[0] in match_types else tuple()
