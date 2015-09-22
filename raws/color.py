#!/usr/bin/env python
# coding: utf-8

'''
    A bit of clever hackishness to provide a convenient syntax for working with
    color definitions in raws files.
'''

'''
    Examples of what becomes possible:
    
    raws.color.blue == 1
    raws.color.lred == 12
    raws.color.blue() == (1, 0, 0)
    raws.color.lred() == (4, 0, 1)
    raws.color.blue.bg() == (0, 1, 0)
    raws.color.lred.bg() == (0, 12, 0)
    raws.color.lblue(pydwarf.color.red) == (1, 4, 1)
    raws.color.lblue(pydwarf.color.lred) == (1, 12, 1)
'''

class record:
    '''
        Instances record name and index information associated with each of
        Dwarf Fortress' sixteen colors.
    '''
    
    def __init__(self, name, value):
        '''Initialize a color record.'''
        self.name = name
        self.value = value
        
    def __call__(self, *args, **kwargs):
        '''Get token arguments representing this color as the foreground.'''
        return self.fg(*args, **kwargs)
        
    def __int__(self):
        '''Get the color index associated with the record.'''
        return self.value
        
    def __str__(self):
        '''Get the name of the color record.'''
        return self.name
        
    def fg(self, bg=0, i=0):
        '''Get token arguments representing this color as the foreground.'''
        return tokenargs.tokenargs((
            self.value % 8,
            int(bg),
            int(i or (self.value >= 8))
        ))
    def bg(self):
        '''Get token arguments representing this color as the background.'''
        return tokenargs.tokenargs(('0', str(self.value), '0'))
        
    # Overload common operators
    
    def __eq__(self, value):
        return self.value == int(value)
    def __ne__(self, value):
        return self.value != int(value)
    def __add__(self, value):
        return self.value + int(value)
    def __sub__(self, value):
        return self.value - int(value)
    def __mul__(self, value):
        return self.value * int(value)
    def __div__(self, value):
        return self.value / int(value)
    def __mod__(self, value):
        return self.value % int(value)



def __init__():
    '''Internal: Initialize color records.'''
    
    names = (
        'black', 'blue', 'green', 'cyan',
        'red', 'magenta', 'brown', 'lgray',
        'dgray', 'lblue', 'lgreen', 'lcyan',
        'lred', 'lmagenta', 'yellow', 'white',
    )

    get.colorlist = []
    for index, name in enumerate(names):
        col = record(name, index)
        get.colorlist.append(col)
        globals()[name] = col



def get(value, i=0):
    '''Get a color record by value and optional intensity.'''
    value = int(value)
    if i: value += 8
    return get.colorlist[value]
    
def fg(args):
    '''Extract foreground color record from a set of three token arguments.'''
    if isinstance(args, token.token): args = args.args
    return get(args[0], args[2])
    
def bg(args):
    '''Extract background color record from a set of three token arguments.'''
    if isinstance(args, token.token): args = args.args
    return get(args[1])
    
def group(fg=None, bg=None):
    '''
        Combine two color records to get a single list of foreground,
        background, intensity arguments.
    '''
    f = fg() if fg is not None else (0, 0, 0)
    return tokenargs.tokenargs((fg.value % 8, bg.value, int(fg.value >= 8)))



__init__()

list = get.colorlist



import tokenargs
import token
