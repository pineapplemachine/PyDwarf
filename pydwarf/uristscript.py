import textwrap



class uristscript(object):
    '''Registered functions and their metadata are tracked by instances of this class.'''
    
    def __init__(self, func, **metadata):
        '''Initialize an uristscript object.'''
        self.func = func
        self.metadata = metadata
        self.setname(metadata.get('name', func.__name__))
        
    def __call__(self, df, *args, **kwargs):
        '''Call the script's function with the given arguments.'''
        return self.func(df, *args, **kwargs)
    
    def __str__(self):
        '''Get a string representation.'''
        return self.getname()
        
    def __hash__(self):
        '''Get a hash, even though registered functions aren't strictly immutable.'''
        return hash(';'.join((self.getname(), str(self.meta('version')), str(self.meta('author')))))
        
    def within(self, namespace):
        '''Check whether the script is contained within a namespace.'''
        if isinstance(namespace, basestring): namespace = namespace.split('.')
        if self.namespace is None:
            return not namespace
        elif len(namespace) > len(self.namespace):
            return False
        else:
            return all(space == self.namespace[index] for index, space in enumerate(namespace))
        
    def setname(self, name):
        '''Set the script's name given a string.'''
        self.name, self.namespace = uristscript.splitname(name)
        
    def getname(self):
        '''Get the script's full name, including namespace.'''
        if self.namespace:
            namespace = '.'.join(self.namespace)
            return '%s.%s' % (namespace, self.name)
        else:
            return self.name
    
    def meta(self, key, default=None):
        '''Get metadata attribute for the script by name.'''
        return self.metadata.get(key, default)
    
    def matches(self, match):
        '''Determine whether the script's metadata matches the keys, values in a dict.'''
        return all([self.meta(i) == j for i, j in match.iteritems()]) if match else True
    
    @staticmethod
    def splitname(name):
        '''Split a full name string into namespace and name.'''
        if '.' in name:
            nameparts = name.split('.')
            return nameparts[-1], nameparts[:-1]
        else:
            return name, tuple()
            
    def doc(self, format=None):
        '''Make a pretty metadata string using the script's metadata.'''
        
        template = uristdoc.template.format.get(format if format else 'txt')
        if template is None: raise KeyError('Failed to create documentation string because the format %s was unrecognized.' % format)
        
        handled_metadata_keys = (
            'name', 'namespace', 'author', 'version',
            'description', 'arguments', 'compatibility', 'title'
        )
        
        return template.full(
            name = self.getname(),
            title = self.meta('title'),
            version = self.meta('version'),
            author = self.meta('author'),
            description = self.meta('description'),
            compatibility = self.meta('compatibility'),
            arguments = self.meta('arguments'),
            metadata = {key: value for key, value in self.metadata.iteritems() if key not in handled_metadata_keys},
            allmeta = self.metadata,
        )



import uristdoc
