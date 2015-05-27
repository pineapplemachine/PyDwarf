import os
import logging
import re

__version__ = 'alpha'

# Make a default logger object
log = logging.getLogger()

# Can be expected to match all past and future 0.40.* releases. (Time of writing is 21 May 15, the most recent version is 0.40.24.)
df_0_40 = '(0\.40\.\d{2,}[abcdefg]?)'
# Matches all DF 0.34.* releases
df_0_34 = '(0\.34\.(1[10]|0\d))'
# Matches all DF 0.31.* releases
df_0_31 = '(0\.31\.(2[0-5]|[01]\d))'
# Matches all DF 0.34 and 0.31 releases
df_0_3x = '|'.join((df_0_31, df_0_34))
# Matches all DF 0.28.* releases
df_0_28 = '(0\.28\.181\.(40[abcd]|39[abcdef]))'
# Matches all DF 0.27.* releases
df_0_27 = '(0\.27\.((176|173)\.38|169\.(33[abcedefg]|32a)))'
# Matches all DF 0.23.* releases
df_0_23 = '(0\.23\.125\.23a)'
# Matches all DF 0.22.* releases
df_0_22 = '(0\.22\.1(23\.23a|2[01]\.23[ab]|10\.(23[abc]|22[abcdef])|07\.21a))'
# Matches all DF 0.21.* releases
df_0_21 = '(0\.21\.(10(5\.21a|4\.(21[abc]|19[abc])|2\.19a|1\.19[abcd]|0\.19a)|9[53]\.19[abc]))'
# Matches all DF 0.27, 0.23, 0.22, and 0.21 releases
df_0_2x = '|'.join((df_0_21, df_0_22, df_0_23, df_0_27, df_0_28))

# Generates a regex which should properly match from, until, and each version in-between.
# For example: pydwarf_range('0.40.14', '0.40.24')
def df_revision_range(prettymin=None, prettymax=None, major=None, minor=None, minrevision=None, maxrevision=None):
    if prettymin:
        parts = prettymin.split('.')
        major = parts[0] if len(parts) else '0'
        minor = parts[1] if len(parts) > 1 else '0'
        minrevision = parts[2] if len(parts) > 2 else '0'
    if prettymax:
        parts = prettymax.split('.')
        maxrevision = parts[2] if len(parts) > 2 else '0'
    return '%s\.%s\.(%s)' % (major, minor, '|'.join([str(r) for r in range(int(minrevision), int(maxrevision)+1)]))

# Convenience functions which scripts can use for returning success/failure responses
def success(status=None): return response(True, status)
def failure(status=None): return response(False, status)
def response(success=None, status=None):
    result = {}
    if success is not None: result['success'] = success
    if status is not None: result['status'] = status
    return result

class session:
    def __init__(self, dfraws):
        self.raws = dfraws
        self.successful = []
        self.failed = []
        # todo

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
    
    registered = {}
    def __init__(self, **kwargs):
        self.metadata = kwargs
    def __call__(self, fn):
        self.fn = fn
        if 'name' in self.metadata:
            self.name, namespace = urist.splitname(self.metadata['name'])
            if namespace is not None: self.metadata['namespace'] = namespace
        else:
            self.name = fn.__name__
        if self.name not in urist.registered: urist.registered[self.name] = []
        urist.registered[self.name].append(self)
        log.debug('Registered script %s.' % self.name)
        return fn
    
    def meta(self, key):
        return self.metadata.get(key)
    
    def matches(self, match):
        return all([self.meta(i) == j for i, j in match.iteritems()]) if match else True
    
    @staticmethod
    def get(name, version=None, match=None):
        name, namespace = urist.splitname(name)
        if namespace is not None:
            if not match: match = {}
            match['namespace'] = namespace
        candidates = urist.registered.get(name)
        if candidates and len(candidates):
            if match:
                candidates = [c for c in candidates if c.matches(match)]
            if version:
                comp = []
                nocomp = []
                for candidate in candidates:
                    meta = candidate.metadata
                    compatibility = meta.get('compatibility')
                    if compatibility:
                        compindex = -1
                        if isinstance(compatibility, basestring):
                            if re.match(compatibility, version): comp.append(candidate)
                        else:
                            for item in compatibility:
                                if re.match(item, version): comp.append(candidate); break
                    else:
                        nocomp.append(candidate)
                candidates = comp + nocomp
        return candidates
        
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
            namespace = '.'.join(nameparts[-1:])
            return name, namespace
        else:
            return name, None
