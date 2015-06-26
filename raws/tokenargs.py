class tokenargs(list):
    
    # Disallow these characters inside token arguments
    illegal = '[]:'
    
    # Replace simple inputs with illegal characters with their legal equivalents
    replace = {
        "':'": '58',
        "'['": '91',
        "']'": '93'
    }
    
    @staticmethod
    def sanitize(value):
        '''Internal: Utility method for sanitizing a string intended to be evaluated as an arugment for a token.'''
        valuestr = str(value)
        if valuestr in tokenargs.replace:
            valuestr = tokenargs.replace[valuestr]
        else:
            if any([char in valuestr for char in tokenargs.illegal]): raise ValueError('Illegal character in argument %s.' % valuestr)
        return valuestr
    
    def append(self, item):
        list.append(self, tokenargs.sanitize(item))
    
    def extend(self, items):
        list.extend(self, (tokenargs.sanitize(item) for item in items))
        
    def insert(self, index, item):
        list.insert(self, index, tokenargs.sanitize(item))
        
    def clear(self):
        del self[:]
        
    def reset(self, items):
        self[:] = (tokenargs.sanitize(item) for item in items)
        
    def __str__(self):
        return ':'.join(self)
        
    def __repr__(self):
        return str(self)
        
    def __add__(self, items):
        return list.__add__(self, (tokenargs.sanitize(item) for item in items))
        
    def __contains__(self, item):
        try:
            san = tokenargs.sanitize(item)
        except:
            return False
        else:
            return list.__contains__(self, san)
    
    def __iadd__(self, item):
        list.__iadd__(self, tokenargs.sanitize(item))
    
    def __init__(self, items=None):
        if items:
            list.__init__(self, (tokenargs.sanitize(item) for item in items))
        else:
            list.__init__(self)
        
    def __setslice__(self, start, stop, items):
        list.__setslice__(self, start, stop, (tokenargs.sanitize(item) for item in items))
    
    def __setitem__(self, index, item):
        list.__setitem__(self, index, tokenargs.sanitize(item))
