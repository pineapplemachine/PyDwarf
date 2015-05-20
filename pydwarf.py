import os
import logging
import re

__version__ = 'alpha'

# Make a default log object if none exists already
if 'log' not in vars() and 'log' not in globals(): log = logging.getLogger()

# Convenience functions which scripts can use for returning success/failure responses
def success(status=None): return response(True, status)
def failure(status=None): return response(False, status)
def response(success=None, status=None):
    result = {}
    if success is not None: result['success'] = success
    if status is not None: result['status'] = status
    return result
    
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
            
    Standard metadata - PyDwarf does nothing special with these, but for the sake of standardization they ought to be included:
        author: Indicates who created the script.
        version: Indicates the script version.
        description: Describes the script's purpose and functioning.
        arguments: Should be a dict with argument names as keys corresponding to strings which
            explain their purpose.
    '''
    
    registered = {}
    def __init__(self, **kwargs):
        self.metadata = kwargs
    def __call__(self, fn):
        self.name = self.metadata['name'] if 'name' in self.metadata else fn.__name__
        self.fn = fn
        if self.name not in urist.registered: urist.registered[self.name] = []
        urist.registered[self.name].append(self)
        log.debug('Registered script %s.' % self.name)
        return fn
    @staticmethod
    def get(name, version=None, match=None):
        candidates = urist.registered.get(name)
        if candidates and len(candidates):
            if match:
                candidates = [c for c in candidates if all([c.metadata.get(i) == j for i, j in match.iteritems()])]
            if version:
                compmap = []
                nocomp = []
                for candidate in candidates:
                    meta = candidate.metadata
                    compatibility = meta.get('compatibility')
                    if compatibility:
                        compindex = -1
                        if isinstance(compatibility, basestring):
                            if re.match(compatibility, version): compindex = 0
                        else:
                            index = 0
                            for item in compatibility:
                                if re.match(item, version):
                                    compindex = index; break
                                else:
                                    index += 1
                        if compindex >= 0:
                            while compindex >= len(compmap): compmap.append([])
                            compmap[compindex].append(candidate)
                    else:
                        nocomp.append(candidate)
                candidates = []
                for comp in compmap: candidates += comp
                candidates += nocomp
        return candidates
            

