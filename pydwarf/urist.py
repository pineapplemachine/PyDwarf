import logging
import version as versionutils



# Make a default logger object
log = logging.getLogger()



class session:
    def __init__(self, dfraws=None, dfversion=None):
        self.dfraws = dfraws
        self.dfversion = dfversion
        self.successes = []
        self.failures = []
        self.noresponse = []
        
    def successful(self, info):
        return self.inlist(info, self.successes)
    def failed(self, info):
        return self.inlist(info, self.failures)
        
    def inlist(self, info, flist):
        funcs = self.funcs(info)
        if funcs:
            return any([(func in flist) for func in funcs])
        else:
            return False
        
    def eval(self, func, args=None):
        # If the function is actually an urist, make sure we know that
        uristinstance = None
        if isinstance(func, urist): 
            uristinstance = func
            func = uristinstance.fn
            name = uristinstance.getname()
        else:
            name = func.__name__
        # Actually execute the script
        log.info('Running script %s%s.' % (name, ('with args %s' % args) if args else ''))
        try:
            # Call the function
            response = func(self.dfraws, **args) if args else func(self.dfraws)
            if response:
                # Handle success/failure response
                log.info('%s: %s' % ('SUCCESS' if response.success else 'FAILURE', str(response)))
                (self.successes if response.success else self.failures).append(uristinstance if uristinstance else func)
            else:
                log.error('Received no response from script %s.' % name)
                self.noresponse.append(uristinstance if uristinstance else func)
        except Exception:
            log.exception('Unhandled exception while running script %s.' % name)
            return False
        else:
            log.info('Finished running script %s.' % name)
            return True
    
    def funcs(self, info):
        uristinstance, scriptname, scriptfunc, scriptargs, scriptmatch, checkversion = urist.info(info, self.dfversion)
        if uristinstance is None and scriptfunc is None and scriptname is not None:
            return urist.get(scriptname, version=checkversion, match=scriptmatch, session=self)
        elif uristinstance is not None:
            return (uristinstance,)
        elif scriptfunc is not None:
            return (scriptfunc,)
        else:
            return None
    
    def handle(self, info):
        funcs = self.funcs(info)
        if funcs:
            for func in funcs: self.eval(func)
        else:
            log.error('Found no scripts matching %s.' % info)
            
    def handleall(self, infos):
        for info in infos: self.handle(info)
        
        

# Functions in scripts must be decorated with this in order to be made available to PyDwarf
class urist:
    '''Decorates a function as being an urist. Keyword arguments are treated as metadata.
    
    Special metadata - these are given special handling:
        name: If name is not specified, then the function name is used to refer to the script.
            If specified, this is used instead.
        compatibility: Informs PyDwarf, using a regular expression, which Dwarf Fortress
            versions a script is compatible with. If this is an iterable, later patterns
            should describe versions that the plugin is partially compatible with, or that
            it ought to be compatible with but that hasn't been tested. This way, a version
            with a more confident compatibility indicator can be chosen over one with a less
            confident indicator.
        namespace: Should correspond to an author or authors, groups of mods, or anything
            really. When specified, it becomes possible for a user to conveniently reference
            a particular one of multiple identically-named mods by a namespace. If there is
            a period in a script name, the text preceding the last period is assumed to be
            namespace and the text after the name.
        dependency: Will cause an error to be logged when running a script without having
            run all of its dependencies first.
            
    Standard metadata - PyDwarf does nothing special with these, but for the sake of standardization they ought to be included:
        author: Indicates who created the script. In the case of multiple authors, an
            iterable such as a tuple or list should be used to enumerate them.
        version: Indicates the script version.
        description: Describes the script's purpose and functioning.
        arguments: Should be a dict with argument names as keys corresponding to strings which
            explain their purpose.
    '''
    
    # Track registered functions
    registered = {}
    # Track data about which scripts have run successfully, etc.
    session = session()
    
    # Decorator handling
    def __init__(self, **kwargs):
        self.namespace = ''
        self.metadata = kwargs
    def __call__(self, fn):
        self.fn = fn
        if 'name' in self.metadata:
            self.name, self.namespace = urist.splitname(self.metadata['name'])
        else:
            self.name = fn.__name__
        if self.name not in urist.registered: urist.registered[self.name] = []
        urist.registered[self.name].append(self)
        log.debug('Registered script %s.' % self.getname())
        return fn
        
    def __str__(self):
        return self.getname()
        
    def __hash__(self):
        return hash(';'.join((self.getname(), str(self.meta('version')), str(self.meta('author')))))
        
    def getname(self):
        return '.'.join((self.meta('namespace'), self.name)) if 'namespace' in self.metadata else self.name
    
    def namespace(self):
        return self.meta('namespace')
    
    def meta(self, key):
        return self.metadata.get(key)
    
    def matches(self, match):
        return all([self.meta(i) == j for i, j in match.iteritems()]) if match else True
    
    def depsatisfied(self, session):
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
    def info(script, version=None):
        # A script can be specified in a variety of ways in the scripts iterable, this function is for understanding all the different options and returning the info the manager needs.
        uristinstance, scriptname, scriptfunc, scriptargs, scriptmatch = None, None, None, None, None
        scriptignoreversion = None
        
        if isinstance(script, urist):
            uristinstance = script
        elif callable(script):
            scriptfunc = script
            uristinstance = urist.forfunc(scriptfunc)
        elif isinstance(script, basestring):
            scriptname = script
        elif isinstance(script, dict):
            scriptname = script.get('name')
            scriptfunc = script.get('func')
            scriptargs = script.get('args')
            scriptmatch = script.get('match')
            scriptignoreversion = script.get('ignore_df_version')
            
        checkversion = None if scriptignoreversion else version
        
        if uristinstance is not None:
            scriptname = uristinstance.name
            scriptfunc = uristinstance.fn
            
        if scriptname is None and scriptfunc is not None:
            scriptname = scriptfunc.__name__
            
        return uristinstance, scriptname, scriptfunc, scriptargs, scriptmatch, checkversion
        
    @staticmethod
    def getregistered(name, namespace=None):
        named = urist.allregistered() if name == '*' else urist.registered.get(name)
        if named and namespace:
            return [ur for ur in named if ur.namespace == namespace or ur.namespace.startswith(namespace+'.')]
        else:
            return named
        
    @staticmethod
    def allregistered():
        results = []
        for rlist in urist.registered.itervalues():
            for r in rlist: results.append(r)
        return results
    
    @staticmethod
    def get(name, version=None, match=None, session=None):
        # Reduce list based on matching the match dict, version compatibility, dependencies, etc
        return urist.cullcandidates(
            version = version, 
            match = match, 
            session = session if session is not None else urist.session, 
            candidates = urist.getregistered(*urist.splitname(name))
        )
        
    @staticmethod
    def cullcandidates(version, match, session, candidates):
        if candidates and len(candidates):
            candidates = urist.cullcandidates_match(match, candidates)
            candidates = urist.cullcandidates_compatibility(version, candidates)
            candidates = urist.cullcandidates_dependency(session, candidates)
            candidates = urist.cullcandidates_duplicates(candidates)
        return candidates
    
    @staticmethod
    def cullcandidates_match(match, candidates):
        return [c for c in candidates if c.matches(match)] if match else candidates
    
    @staticmethod
    def cullcandidates_compatibility(version, candidates):
        if version:
            comp = []
            nocomp = []
            for candidate in candidates:
                compatibility = candidate.meta('compatibility')
                if compatibility:
                    if versionutils.compatible(compatibility, version): comp.append(candidate)
                else:
                    nocomp.append(candidate)
            return comp + nocomp
        else:
            return candidates
    
    @staticmethod
    def cullcandidates_dependency(session, candidates):
        return [c for c in candidates if c.depsatisfied(session)]
    
    @staticmethod
    def cullcandidates_duplicates(candidates):
        names = {}
        for candidate in candidates:
            candname = candidate.name
            dupe = names.get(candname)
            if dupe is None:
                names[candname] = candidate
            elif candidate.meta('namespace') == dupe.meta('namespace'):
                if ((dupe.meta('version') is None) or ((candidate.meta('version') is not None) and candidate.meta('version') > dupe.meta('version'))):
                    names[candname] = candidate
            else:
                pass # conflicting names in different namespaces, do nothing
        return names.values()
    
    @staticmethod
    def forfunc(func):
        for uristlist in registered:
            for urist in uristlist:
                if urist.fn == func: return urist
        return None
            
    @staticmethod
    def splitname(name):
        if '.' in name:
            nameparts = name.split('.')
            name = nameparts[-1]
            namespace = '.'.join(nameparts[:-1])
            return name, namespace
        else:
            return name, None
