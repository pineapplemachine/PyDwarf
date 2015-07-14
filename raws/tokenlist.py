#!/usr/bin/env python
# coding: utf-8

import queryable
import textwrap



class tokenlist(list, queryable.queryable):
    '''Extends builtin list with token querying functionality.'''
    
    def tokens(self, range=None, reverse=False):
        for i in xrange(self.__len__()-1, -1, -1) if reverse else xrange(0, self.__len__()):
            if range is not None and range <= count: break
            yield self.__getitem__(i)
            
    def add(self, item):
        if isinstance(item, token.token):
            self.append(item)
        elif isinstance(item, queryable.queryable):
            self.extend(item.tokens())
        elif isinstance(item, list):
            self.extend(item)
        else:
            raise ValueError('Failed to add item because it was of an unrecognized type.')
    
    def each(self, func=None, filter=None):
        '''Calls a function for each entry in the list with that entry as the argument, and
        appends each result to a returned tokenlist.'''
        return tokenlist(
            (func(token) if func is not None else token) for token in self if (filter is None or filter(token))
        )
        
    def copy(self, shallow=False):
        if shallow:
            return tokenlist(token for token in self)
        else:
            return token.token.copytokens(self)
            
    def remove(self, *args, **kwargs):
        for token in self: token.remove(*args, **kwargs)
    
    def __add__(self, other):
        return self.copy().add(other)
        
    def __mul__(self, count):
        result = tokenlist()
        for i in xrange(0, count): result.add(self.copy())
        return result
        
    def __iadd__(self, other):
        self.add(other)
    
    def __getitem__(self, *args, **kwargs):
        result = list.__getitem__(self, *args, **kwargs)
        if isinstance(result, list): result = tokenlist(result)
        return result
    
    def __getslice__(self, *args, **kwargs):
        return tokenlist(list.__getslice__(self, *args, **kwargs))
    
    def __str__(self):
        if len(self) == 0:
            return ''
        elif len(self) == 1:
            return str(self[0])
        else:
            parts = []
            minindent = None
            for token in self:
                prefix = ''
                text = str(token)
                suffix = ''
                if token is not self[0] and ((token.prefix and '\n' in token.prefix)): prefix += '\n'
                if token.prefix: prefix += token.prefix.split('\n')[-1]
                if token.suffix: suffix += token.suffix.split('\n')[0]
                if token is not self[-1] and ((token.suffix and '\n' in token.suffix)): suffix += '\n'
                parts.extend((prefix, text, suffix))
            fulltext = ''.join(parts)
            return textwrap.dedent(fulltext)



import token
