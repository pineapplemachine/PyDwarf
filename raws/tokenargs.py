class tokenargs(list):
    
    # Disallow these characters inside token arguments
    illegal = '[]:'
    
    # Replace simple inputs with illegal characters with their legal equivalents
    replace = {
        "':'": '58',
        "'['": '91',
        "']'": '93'
    }
    
    def __init__(self, items):
        if items is not None:
            self.reset()
        elif isinstance(items, basestring):
            self.reset(items.split(':'))
        else:
            self.reset(items)
    
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
        
    def reset(self, items=None):
        self[:] = (tokenargs.sanitize(item) for item in items) if items is not None else []
        
    def add(self, item):
        if isinstance(item, basestring):
            self.extend(item.split(':'))
        elif hasattr(item, '__iter__') or hasattr(item, '__getitem__'):
            self.extend(item)
        else:
            self.add(str(item))
            
    def sub(self, items):
        self[:] = self[:-items]
        
    def __str__(self):
        return ':'.join(self)
        
    def __repr__(self):
        return str(self)
        
    def __add__(self, items):
        return list.__add__(self, (tokenargs.sanitize(item) for item in items))
        
    def __iadd__(self, item):
        self.add(item)
        
    def __isub__(self, items):
        self.sub(items)
        
    def __contains__(self, item):
        try:
            san = tokenargs.sanitize(item)
        except:
            return False
        else:
            return list.__contains__(self, san)
    
    def __init__(self, items=None):
        if items:
            list.__init__(self, (tokenargs.sanitize(item) for item in items))
        else:
            list.__init__(self)
        
    def __setslice__(self, start, stop, items):
        list.__setslice__(self, start, stop, (tokenargs.sanitize(item) for item in items))
    
    def __setitem__(self, index, item):
        list.__setitem__(self, index, tokenargs.sanitize(item))
