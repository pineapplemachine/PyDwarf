#!/usr/bin/env python
# coding: utf-8

class tokenargs(object):
    '''Wraps builtin list with checks for illegal characters in token arguments.'''
    
    # Disallow these characters inside token arguments
    illegal = '[]:'
    
    # Replace simple inputs with illegal characters with their legal equivalents
    replace = {
        "':'": '58',
        "'['": '91',
        "']'": '93'
    }
    
    def __init__(self, items=None):
        '''Construct a new list of token arguments.'''
        self.list = list()
        if items is not None: self.reset(items)
        
    def __setitem__(self, item, value):
        '''Set an item in the list.'''
        self.list[item] = self.sanitize(value)
        
    def __getitem__(self, item):
        '''Get an item from the list.'''
        result = self.list[item]
        if isinstance(result, list):
            return tokenargs(result)
        else:
            return result
        
    def __str__(self):
        '''Get a string representation.'''
        return ':'.join(self.list)
        
    def __add__(self, items):
        '''Concatenate two lists of arguments.'''
        return tokenargs(self.list + list(items))
        
    def __radd__(self, items):
        '''Concatenate two lists of arguments.'''
        return tokenargs(list(items) + self.list)
        
    def __iadd__(self, item):
        '''Add an item or items to the end of the list.'''
        self.add(item)
        return self
        
    def __isub__(self, count):
        '''Remove some number of items from the end of the list.'''
        self.sub(count)
        return self
        
    def __contains__(self, item):
        '''Check if the list contains an item.'''
        try:
            item = self.sanitize(item)
        except:
            return False
        else:
            return item in self.list
            
    def __iter__(self):
        '''Iterate through items in the list.'''
        return self.list.__iter__()
        
    def __len__(self):
        '''Get the number of items in the list.'''
        return self.list.__len__()
        
    def __mul__(self, count):
        '''Concatenate the list with itself some number of times.'''
        return tokenargs(self.list * count)
    
    def __imul__(self, count):
        '''Concatenate the list with itself some number of times.'''
        self.list *= count
        
    def __eq__(self, other):
        '''Check equivalency with another list of arguments.'''
        return len(self.list) == len(other) and all(self.list[index] == str(item) for index, item in enumerate(other))
        
    def reset(self, items):
        '''Reset list to contain specified items.'''
        if items is None:
            self.clear()
        elif isinstance(items, basestring):
            self.reset(items.split(':'))
        else:
            self.list[:] = self.sanitize(items)
            
    def set(self, index, item=None):
        '''
            Set a single argument given an index or, if no index is given, set
            the argument at index 0.
        '''
        if item is None:
            item = index
            index = 0
        self.list[index] = self.sanitize(item)
            
    def clear(self):
        '''Remove all items from the list.'''
        del self.list[:]
            
    def sanitize(self, value, replace=True):
        '''
            Internal: Utility method for sanitizing a string intended to be
            evaluated as an arugment for a token.
        '''
        if isinstance(value, basestring):
            if replace and value in tokenargs.replace:
                value = tokenargs.replace[value]
            else:
                if any([char in value for char in tokenargs.illegal]):
                    raise ValueError('Illegal character in argument %s.' % value)
            return value
        else:
            try:
                return (self.sanitize(item, replace) for item in value)
            except:
                return self.sanitize(str(value), replace)
        
    def append(self, item):
        '''Append a single item to the list.'''
        self.list.append(self.sanitize(item))
        
    def extend(self, items):
        '''Append multiple items to the list.'''
        if isinstance(items, basestring):
            self.extend(items.split(':'))
        else:
            self.list.extend(self.sanitize(items))
            
    def insert(self, index, item):
        '''Insert an item at some index.'''
        self.list.insert(index, self.sanitize(item))
        
    def add(self, item, *args):
        '''Add an item or items to the end of the list.'''
        if isinstance(item, basestring):
            self.extend(item.split(':'))
        elif hasattr(item, '__iter__') or hasattr(item, '__getitem__'):
            self.extend(item)
        else:
            self.add(str(item))
        if args:
            self.add(args)
            
    def sub(self, count):
        '''Remove some number of items from the end of the list.'''
        self[:] = self[:-count]
