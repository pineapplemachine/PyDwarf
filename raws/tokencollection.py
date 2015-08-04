class tokencollection(object):
    def __str__(self):
        '''Get a string representation.'''
        return helpers.tokensstring(self)
    
    def each(self, func=None, filter=None, iter=None, output=None, none=False):
        '''
            Call a function for each entry in the list with that entry as the
            argument and return the results as the given output type or, if no
            such class is provided, as the same class as this object.
        '''
        
        if iter is None: iter = self.itokens()
        
        def gen():
            for token in iter:
                if filter is None or filter(token):
                    if func:
                        result = func(token)
                    else:
                        result = token
                    if none or result is not None:
                        yield result
        
        if output is None: output = type(self)
        return output(gen())
        
    def equals(self, other):
        '''Check for equivalency with another iterable containing tokens.'''
        return helpers.tokensequal(self.itokens(), other)



import helpers
