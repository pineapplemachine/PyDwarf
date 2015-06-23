# Add some basic functionality for working with DFHack

import os
import shutil



class dfhack:
    nodir = 'Can\'t add file, DFHack directory hasn\'t been specified.'
    
    def __init__(self, path=None, version=None):
        '''Constructor for dfhack object.'''
        self.path = path
        self.version = version # TODO: automatic detection in pydwarf.config isn't reliable (why am I putting it here? who the fuck knows)
    
    def open(path, *args, **kwargs):
        '''Open a file within the DFHack directory. Acts as a shortcut for open('dfhack/path', mode).'''
        
        if not self.path:
            log.error(dfhack.nodir)
            return None
        else:
            return open(os.path.join(self.path, path), *args, **kwargs)
            
    def exists(path):
        return self.path and os.path.exists(os.path.join(self.path, path))
    def isfile(path):
        return self.path and os.path.isfile(os.path.join(self.path, path))
    def isdir(path):
        return self.path and os.path.isdir(os.path.join(self.path, path))
            
    def add(path, dest, overwrite=False):
        '''Copies an existing file into the DFHack directory.'''
        
        if not os.path.exists(path):
            raise ValueError('File %s does not exist.' % path)
        elif not self.path:
            raise ValueError(dfhack.nodir)
        else:
            destpath = os.path.join(self.path, dest)
            destexists = os.path.exists(destpath)
            if destexists and not overwrite:
                raise ValueError('File %s already exists.' % destpath)
            else:
                shutil.copy2(path, destpath)
                return True
        return False
        
    def remove(path):
        '''Removes a file from the DFHack directory.'''
        
        if not self.path:
            raise ValueError(dfhack.nodir)
        else:
            path = os.path.join(self.path, path)
            if os.path.isfile(path):
                os.remove(path)
                return True
            elif os.path.isdir(path):
                shutil.rmtree(path)
                return True
            else:
                raise ValueError('Failed to remove file or directory %s because the path is invalid.' % path)
        return False
