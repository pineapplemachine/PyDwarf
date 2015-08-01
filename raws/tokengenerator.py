import itertools

import queryable
import tokencollection



class regenerator(object):
    '''
        Wrapper object for generator functions which automatically recalls them
        upon repeated iterations.
    '''
    
    def __init__(self, func, *args, **kwargs):
        '''
            Create a new regenerator given a generator function and the
            arguments which should be passed to it.
        '''
        self.func = func
        self.args = args
        self.kwargs = kwargs
        
    def __iter__(self):
        '''Create and return a new generator.'''
        return self.func(*self.args, **self.kwargs)
        
    def __len__(self):
        '''Get the number of elements in the generator.'''
        return sum(1 for i in self)
        
    
    
class tokengenerator(regenerator, tokencollection.tokencollection, queryable.queryable):
    '''
        Wraps a generator containing token objects with helpful methods and the
        ability to iterate more than just once when desired.
    '''
    
    def copy(self, *args, **kwargs):
        '''Make a copy of this tokengenerator.'''
        kwargs['iter'] = kwargs.get('iter', True)
        return helpers.copytokens(self, *args, **kwargs)
        
    def tokens(self, *args, **kwargs):
        '''Iterate through the generator's tokens.'''
        return self.itokens(*args, **kwargs)
        
    def itokens(self, range=None):
        '''Iterate through the generator's tokens.'''
        count = 0
        for item in self:
            if range is not None and range <= count: break
            yield item
            count += 1
            
    def __eq__(self, other):
        '''Check for equivalency with another iterable containing tokens.'''
        return self.equals(other)



import tokenlist
import helpers
