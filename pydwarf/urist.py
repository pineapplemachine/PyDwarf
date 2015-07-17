#!/usr/bin/env python
# coding: utf-8

import registrar



# Functions in scripts must be decorated with this in order to be made available to PyDwarf
class urist:
    '''
        Decorates a function as being an urist. Keyword arguments are treated as metadata.
        
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
    registrar = registrar.registrar()
    
    # Decorator handling
    def __init__(self, **kwargs):
        self.metadata = kwargs
    def __call__(self, func):
        script = uristscript.uristscript(func, **self.metadata)
        urist.register(script)
        return script
        
    @staticmethod
    def register(script):
        urist.registrar.__register__(script)
        log.debug('Registered script %s.' % script.getname())
    
    @staticmethod
    def info(script, version=None):
        # A script can be specified in a variety of ways in the scripts iterable, this function is for understanding all the different options and returning the info the manager needs.
        uristinstance, scriptname, scriptfunc, scriptargs, scriptmatch = None, None, None, None, None
        scriptignoreversion = None
        
        if isinstance(script, uristscript.uristscript):
            uristinstance = script
        elif callable(script):
            scriptfunc = script
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
            scriptfunc = uristinstance.func
            
        if scriptname is None and scriptfunc is not None:
            scriptname = scriptfunc.__name__
            
        return uristinstance, scriptname, scriptfunc, scriptargs, scriptmatch, checkversion
        
    @staticmethod
    def get(name, version=None, match=None, session=None):
        # Reduce list based on matching the match dict, version compatibility, dependencies, etc
        
        candidates = urist.registrar[name]
        if isinstance(candidates, registrar.registrar):
            candidates = list(candidates)
        else:
            candidates = [candidates]
        
        return urist.cullcandidates(
            version = version, 
            match = match, 
            session = session, 
            candidates = candidates
        )
        
    @staticmethod
    def getfn(name, **kwargs):
        # TODO: deprecate
        candidates, original, culled = urist.get(name, **kwargs)
        if len(candidates):
            return candidates[0]
        else:
            return None
            
    @staticmethod
    def list():
        names = {}
        total = 0
        for uristlist in urist.registered.itervalues():
            for uristinstance in uristlist:
                uname = uristinstance.getname()
                if uname not in names: names[uname] = []
                names[uname].append(uristinstance)
                total += 1
        return sorted(names.keys())
            
    @staticmethod
    def doclist(names=[], delimiter='\n\n', format=None):
        urists = []
        if len(names):
            for name in names: urists += urist.getregistered(*urist.splitname(name))
        else:
            urists = urist.allregistered()
        items = sorted(ur.doc(format=format) for ur in urists)
        template = uristdoc.template.format.get(format if format else 'txt')
        if items and template:
            text = template.concat(items)
        else:
            text = delimiter.join(items)
        return text
    
    @staticmethod
    def cullcandidates(version, match, session, candidates):
        if candidates and len(candidates):
            original_candidates = list(candidates)
            culled_match = 0
            culled_compatibility = 0
            culled_dependency = 0
            
            candidates, culled_match = urist.cullcandidates_match(match, candidates)
            candidates, culled_compatibility = urist.cullcandidates_compatibility(version, candidates)
            candidates, culled_dependency = urist.cullcandidates_dependency(session, candidates)
            candidates = urist.cullcandidates_duplicates(candidates)
            
            return candidates, original_candidates, {
                'Unmatched metadata': culled_match,
                'Incompatible with Dwarf Fortress version %s' % version: culled_compatibility,
                'Unfulfilled dependencies': culled_dependency
            }
            
        else:
            return [], [], {}
    
    @staticmethod
    def cullcandidates_match(match, candidates):
        newcand, culled = [], []
        for cand in candidates: (newcand if cand.matches(match) else culled).append(cand)
        return newcand, culled
    
    @staticmethod
    def cullcandidates_compatibility(version, candidates):
        if version:
            culled = []
            comp = []
            nocomp = []
            for candidate in candidates:
                compatibility = candidate.meta('compatibility')
                ((comp if versionutils.compatible(compatibility, version) else culled) if compatibility else nocomp).append(candidate)
            return comp + nocomp, culled
        else:
            return candidates, []
    
    @staticmethod
    def cullcandidates_dependency(session, candidates):
        if session:
            newcand, culled = [], []
            for cand in candidates: (newcand if cand.depsatisfied(session) else culled).append(cand)
            return newcand, culled
        else:
            return candidates, []
    
    @staticmethod
    def cullcandidates_duplicates(candidates):
        names = {}
        for candidate in candidates:
            candname = candidate.name
            dupe = names.get(candname)
            if dupe is None:
                names[candname] = candidate
            elif candidate.namespace == dupe.namespace:
                if ((dupe.meta('version') is None) or ((candidate.meta('version') is not None) and candidate.meta('version') > dupe.meta('version'))):
                    names[candname] = candidate
            else:
                pass # conflicting names in different namespaces, do nothing
        return names.values()



import uristscript
import version as versionutils
from logger import log
