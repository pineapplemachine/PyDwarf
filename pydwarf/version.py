import os
import re

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

# Given a version and a compatibility regex, determine compatibility
def compatible(compatibility, version):
    if isinstance(compatibility, basestring):
        return re.match(compatibility, version) is not None
    else:
        return any([re.match(item, version) for item in compatibility])

def detectversion(paths, recursion=8, log=None):
    # Given a list of directories that may be inside a DF directory, e.g. raws input or output, look for release notes.txt and get the version from that
    if log: log.debug('Attempting to detect Dwarf Fortress version given paths %s.' % [str(p) for p in paths])
    for path in paths:
        if path is not None:
            currentpath = path
            for i in xrange(0, recursion):
                if os.path.isdir(currentpath):
                    if log: log.debug('Checking path %s for release notes.' % currentpath)
                    if 'release notes.txt' in os.listdir(currentpath):
                        version = versionfromreleasenotes(os.path.join(currentpath, 'release notes.txt'), log)
                        if version: return version
                    else:
                        currentpath = os.path.dirname(currentpath)
                else:
                    break
    return None

def versionfromreleasenotes(path, log=None):
    with open(path, 'rb') as releasenotes:
        for line in releasenotes.readlines():
            if line.startswith('Release notes for'): return line.split()[3]
    return None
