#!/usr/bin/env python
# coding: utf-8

import textwrap
import numbers
import traceback

import queryableadd



class tokenlist(queryableadd.queryableadd):
    '''Wraps builtin list with token querying functionality.'''
    
    def __init__(self, content=None):
        self.content = list()
        if content is not None: self.append(content)
    
    def __len__(self):
        '''Return the number of items in the list.'''
        return len(self.content)
    
    def __iter__(self):
        '''Iterate through the tokens in the list.'''
        return self.content.__iter__()
    
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
        for i in xrange(0, count): result.append(self.copy())
        return result
        
    def __imul__(self, count):
        length = len(self)
        for i in xrange(1, count):
            for j in xrange(0, length):
                self.append(self[j])
        return self
        
    def __iadd__(self, other):
        '''Append an item to the list.'''
        self.append(other)
        return self
        
    def __isub__(self, item):
        '''Remove some number of items from the end of the list.'''
        self.sub(item)
        return self
        
    def __setitem__(self, index, value):
        '''Set the token at an index.'''
        
        # TODO: Support slices?
        if isinstance(value, basestring):
            value = token.token(value)
        self.content[index] = value
        
    def __delitem__(self, item):
        '''Remove an item or items from the list.'''
        self.remove(item)
    
    def __eq__(self, other):
        '''Check equivalency with another iterable of tokens.'''
        return self.equals(other)
    
    def itokens(self, range=None, reverse=False, until=None, step=None):
        '''Iterate through the list's tokens.'''
        iter = reversed(self.content) if reverse else self.content
        for index, token in enumerate(iter):
            if (range is not None and index >= range) or (until is not None and token is until):
                break
            elif step is None or index % step == 0:
                yield token
            
    def append(self, item):
        '''Add a new token to this list, or extend it with another iterable containing tokens.'''
        if isinstance(item, token.token):
            self.content.append(item)
        elif isinstance(item, queryable.queryable):
            self.extend(item.tokens())
        elif isinstance(item, basestring):
            self.extend(tokenparse.parseplural(item, implicit=True))
        else:
            try:
                self.extend(item)
            except Exception as e:
                trace = traceback.format_exc()
                raise TypeError('Failed to append item of type %s\n%s.' % (type(item), trace))
                
    def extend(self, items):
        '''Extend the list with another iterable containing tokens.'''
        for item in items:
            self.append(item)
                
    def add(self, *args, **kwargs):
        '''Add token or tokens to the last token in this list, and also add those tokens to the list itself.'''
        if len(self):
            added = self[-1].add(*args, **kwargs)
            self.append(added)
            return added
        else:
            raise ValueError('Failed to add tokens to tokenlist because the list was already empty.')
    
    def sub(self, item):
        '''Remove some number of items from the end of the list.'''
        try:
            self.content[:] = self.content[:-item]
        except:
            self.remove(item)
    
    def index(self, index):
        '''Get the token at an index.'''
        return self.content[index]
        
    def clear(self):
        '''Remove all tokens from the list.'''
        del self.content[:]
        
    def remove(self, item):
        '''Remove an item or items from the list.'''
        if item is Ellipsis:
            self.clear()
        elif item is None:
            pass
        elif isinstance(item, basestring):
            filter = filters.tokenfilter(pretty=item)
            self.content = [i for i in self.content if not filter.match(i)]
        elif isinstance(item, token.token):
            self.content = [i for i in self.content if i is not item]
        elif isinstance(item, numbers.Number):
            del self.content[item]
        elif isinstance(item, slice):
            newlist = list()
            for index, i in enumerate(self.content):
                if not(
                    (item.start is None or index >= item.start) and
                    (item.stop is None or index <= item.stop) and
                    (item.step is None or (index - item.start) % item.step == 0)
                ):
                    newlist.append(i)
            self.content = newlist
        elif callable(item):
            self.content = [i for i in self.content if not item(i)]
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
