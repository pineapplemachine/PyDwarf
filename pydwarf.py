import os
import logging
import re

__version__ = 'alpha'

# Can be expected to match all past and future 0.40.* releases. (Time of writing is 21 May 15, the most recent version is 0.40.24.)
df_0_40 = '(0\.40\.\d{2,}[abcdefg]?)'
# Matches all DF 0.34.* releases
df_0_34 = '(0\.34\.(1[10]|0\d))'
# Matches all DF 0.31.* releases
df_0_31 = '(0\.31\.(2[0-5]|[01]\d))'
# Matches all DF 0.34 and 0.31 releases
df_0_3x = '|'.join(df_0_31, df_0_34)
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
df_0_2x = '|'.join(df_0_21, df_0_22, df_0_23, df_0_27, df_0_28)

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
            

