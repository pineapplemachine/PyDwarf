class tokencollection(object):
    def __str__(self):
        '''Get a string representation.'''
        return helpers.tokensstring(self)
    
    def each(self, func=None, filter=None, output=None):
        '''
            Call a function for each entry in the list with that entry as the
            argument and return the results as the given output type or, if no
            such class is provided, as the same class as this object.
        '''
        if output is None: output = type(self)
        return output(
            (func(token) if func is not None else token) for token in self if (filter is None or filter(token))
        )
        
    def equals(self, other):
        '''Check for equivalency with another iterable containing tokens.'''
        return helpers.tokensequal(self, other)



import helpers
