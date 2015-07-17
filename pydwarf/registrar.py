class registrar(object):
    __reserved__ = (
        '__name__',
        '__parent__',
    )
        
    def __init__(self, name=None, parent=None):
        self.__name__ = name
        self.__parent__ = parent
        
    def __call__(self, *args, **kwargs):
        return {key: value(*args, **kwargs) for key, value in self.__dict__.iteritems() if key not in registrar.__reserved__}
        
    def __str__(self):
        if self.__parent__ is not None and self.__parent__.__name__ is not None:
            return '%s.%s' % (self.__parent__, self.__name__)
        elif self.__name__ is not None:
            return self.__name__
        else:
            return 'root'
            
    def __len__(self):
        return len(self.__dict__)
        
    def __repr__(self):
        return self.__str__()
            
    def __iter__(self):
        for key, value in self.__dict__.iteritems():
            if key not in registrar.__reserved__:
                if isinstance(value, registrar):
                    for subitem in value: yield subitem
                else:
                    yield value
    
    def __contains__(self, name):
        parts = name.split('.') if isinstance(name, basestring) else name
        if len(parts) == 1:
            return parts[0] in self.__dict__
        else:
            return self.__dict__[parts[0]].__contains__(parts[1:])
            
    def __len__(self):
        return sum(1 for i in self)
            
    def __getitem__(self, name):
        parts = name.split('.') if isinstance(name, basestring) else name
        if len(parts) == 1:
            if parts[0] == '*':
                return self
            else:
                return self.__dict__[parts[0]]
        else:
            return self.__dict__[parts[0]][parts[1:]]
            
    def __getattr__(self, attr):
        return self.__getitem__(attr)
    
    def __setitem__(self, name, script):
        self.__register__(name, script)
        
    def __iadd__(self, script):
        self.__register__(script)
        return self
    
    def __register__(self, script, name=None):
        if name is None: name = script.getname()
        parts = name.split('.') if isinstance(name, basestring) else name
        if len(parts) == 1:
            if parts[0] in registrar.__reserved__:
                raise KeyError('Failed to register script because its name overlapped one of the registrar\'s reserved attribute names.')
            self.__dict__[parts[0]] = script
        else:
            if parts[0] not in self.__dict__: self.__dict__[parts[0]] = registrar(parts[0], self)
            self[parts[0]].__register__(script, parts[1:])
