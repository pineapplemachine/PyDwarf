import textwrap



class uristscript(object):
    def __init__(self, func, **metadata):
        self.func = func
        self.metadata = metadata
        self.setname(metadata.get('name', func.__name__))
        
    def __call__(self, df, *args, **kwargs):
        return self.func(df, *args, **kwargs)
    
    def __str__(self):
        return self.getname()
        
    def __hash__(self):
        return hash(';'.join((self.getname(), str(self.meta('version')), str(self.meta('author')))))
        
    def within(self, namespace):
        if isinstance(namespace, basestring): namespace = namespace.split('.')
        if self.namespace is None:
            return not namespace
        elif len(namespace) > len(self.namespace):
            return False
        else:
            return all(space == self.namespace[index] for index, space in enumerate(namespace))
        
    def setname(self, name):
        self.name, self.namespace = uristscript.splitname(name)
        
    def getname(self):
        if self.namespace:
            namespace = '.'.join(self.namespace)
            return '%s.%s' % (namespace, self.name)
        else:
            return self.name
    
    def meta(self, key, default=None):
        return self.metadata.get(key, default)
    
    def matches(self, match):
        return all([self.meta(i) == j for i, j in match.iteritems()]) if match else True
        
    def depsatisfied(self, session): # TODO: move this to the session class
        deps = self.meta('dependency')
        if deps is not None:
            # Allow single dependencies to be indicated without being inside an iterable
            if isinstance(deps, basestring) or isinstance(deps, dict): deps = (deps,)
            # Check each dependency
            satisfied = 0
            for dep in deps:
                log.debug('Checking for dependency %s...' % dep)
                satisfied += session.successful(dep)
            # All done
            log.debug('Satisifed %d of %d dependencies.' % (satisfied, len(deps)))
            return satisfied == len(deps)
        else:
            return True
        
    @staticmethod
    def splitname(name):
        if '.' in name:
            nameparts = name.split('.')
            return nameparts[-1], nameparts[:-1]
        else:
            return name, tuple()
            
    def doc(self, format=None):
        '''Make a pretty metadata string.'''
        
        template = uristdoc.template.format.get(format if format else 'txt')
        if template is None: raise KeyError('Failed to create documentation string because the format %s was unrecognized.' % format)
        
        handled_metadata_keys = ('name', 'namespace', 'author', 'version', 'description', 'arguments', 'dependency', 'compatibility')
        
        return template.full(
            name = self.getname(),
            version = self.meta('version'),
            author = self.meta('author'),
            description = self.meta('description'),
            compatibility = self.meta('compatibility'),
            dependencies = self.meta('dependency'),
            arguments = self.meta('arguments'),
            metadata = {key: value for key, value in self.metadata.iteritems() if key not in handled_metadata_keys}
        )



import uristdoc
