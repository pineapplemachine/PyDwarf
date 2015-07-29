#!/usr/bin/env python
# coding: utf-8

import textwrap
import numbers

import queryableadd
import tokencollection



class tokenlist(tokencollection.tokencollection, queryableadd.queryableadd):
    '''Wraps builtin list with token querying functionality.'''
    
    def __init__(self, content=None):
        self.list = list()
        if content is not None: self.append(content)
    
    def __len__(self):
        '''Return the number of items in the list.'''
        return len(self.list)
    
    def __iter__(self):
        '''Iterate through the tokens in the list.'''
        return self.list.__iter__()
    
    def __add__(self, other):
        '''Concatenate and return a tokenlist.'''
        tokens = self.copy()
        tokens.append(other)
        return tokens
        
    def __radd__(self, other):
        '''Concatenate and return a tokenlist.'''
        tokens = tokenlist()
        tokens.append(other)
        tokens.append(self)
        return tokens
        
    def __mul__(self, count):
        '''Concatenate the list with itself some number of times.'''
        result = tokenlist()
        for i in xrange(0, count): result.add(self.copy())
        return result
        
    def __iadd__(self, other):
        '''Append an item to the list.'''
        self.append(other)
        
    def __isub__(self, count):
        '''Remove some number of items from the end of the list.'''
        self.sub(count)
        return self
        
    def __setitem__(self, index, value):
        '''Set the token at an index.'''
        self.list[index] = value
        
    def __delitem__(self, item):
        '''Remove an item or items from the list.'''
        self.remove(item)
    
    def __eq__(self, other):
        '''Check equivalency with another iterable of tokens.'''
        return self.equals(other)
    
    def itokens(self, range=None, reverse=False):
        '''Iterate through the list's tokens.'''
        count = 0
        for i in xrange(self.__len__()-1, -1, -1) if reverse else xrange(0, self.__len__()):
            if range is not None and range <= count: break
            yield self.__getitem__(i)
            count += 1
            
    def append(self, item):
        '''Add a new token to this list, or extend it with another iterable containing tokens.'''
        if isinstance(item, token.token):
            self.list.append(item)
        elif isinstance(item, queryable.queryable):
            self.extend(item.tokens())
        elif isinstance(item, basestring):
            self.extend(tokenparse.parseplural(item, implicit=True))
        else:
            self.extend(item)
            try:
                self.extend(item)
            except:
                raise TypeError('Failed to append item because it was of unrecognized type %s.' % type(item))
                
    def extend(self, items):
        '''Extend the list with another iterable containing tokens.'''
        self.list.extend(items)
                
    def add(self, *args, **kwargs):
        '''Add token or tokens to the last token in this list, and also add those tokens to the list itself.'''
        if len(self):
            added = self[-1].add(*args, **kwargs)
            self.append(added)
            return added
        else:
            raise ValueError('Failed to add tokens to tokenlist because the list was already empty.')
    
    def sub(self, count):
        '''Remove some number of items from the end of the list.'''
        self.list[:] = self.list[:-count]
    
    def index(self, index):
        '''Get the token at an index.'''
        return self.list[index]
        
    def clear(self):
        '''Remove all tokens from the list.'''
        del self.list[:]
        
    def remove(self, item):
        '''Remove an item or items from the list.'''
        if item is Ellipsis:
            self.clear()
        elif item is None:
            pass
        elif isinstance(item, basestring):
            filter = filters.tokenfilter(pretty=item)
            self.list = [i for i in self.list if not filter.matches(i)]
        elif isinstance(item, token.token):
            self.list = [i for i in self.list if i is not item]
        elif isinstance(item, numbers.Number):
            del self.list[item]
        elif isinstance(item, slice):
            newlist = list()
            for index, i in enumerate(self.list):
                if not(
                    (item.start is None or index >= item.start) and
                    (item.stop is None or index <= item.stop) and
                    (item.step is None or (index - item.start) % item.step == 0)
                ):
                    newlist.append(i)
            self.list = newlist
        elif callable(item):
            self.list = [i[0] for i in self.iquery(filters=item) if i is not None]
        elif hasattr(item, '__iter__') or hasattr(item, '__getitem__'):
            for i in item: self.remove(i)
        
    def copy(self, shallow=False):
        '''Create a copy of the list.'''
        if shallow:
            return tokenlist(token for token in self)
        else:
            return helpers.lcopytokens(self)
    
    

import queryable
import tokenparse
import token
import helpers
import filters
