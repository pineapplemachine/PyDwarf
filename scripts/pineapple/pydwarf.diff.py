import os
import pydwarf
import difflib
import raws

class diffrecord:
    '''Class for keeping track of differences found by difflib.SequenceMatcher'''
    def __init__(self, a, b, bpath, op, afrom, auntil, bfrom, buntil):
        self.a = a
        self.b = b
        self.bpath = bpath
        self.op = op
        self.afrom = afrom
        self.auntil = auntil
        self.bfrom = bfrom
        self.buntil = buntil
        self.alower = a[afrom]
        self.aupper = a[auntil] if auntil < len(a) else a[-1]
        self.blower = b[bfrom]
        self.bupper = b[buntil] if buntil < len(b) else b[-1]
        self.ignore = False
        self.conflicts = None
    def atokens(self):
        for i in xrange(self.afrom, min(len(self.a), self.auntil)): yield self.a[i]
    def btokens(self):
        for i in xrange(self.bfrom, min(len(self.b), self.buntil)): yield self.b[i]
    def __str__(self):
        return '%s %d:%d' % ({'equal': '..', 'delete': '--', 'insert': '++', 'replace': '//'}[self.op], self.afrom, self.auntil)
        
@pydwarf.urist(
    name = 'pineapple.diff',
    version = '1.0.2',
    author = 'Sophie Kirschner',
    description = '''Merges and applies changes made to some modded raws via diff checking.
        Should be reasonably smart about automatic conflict resolution but if it complains
        then I recommend giving things a manual checkover afterwards. Also, the token-based
        diff'ing approach should work much better than any line-based diff. Using this tool
        to apply mods made to other versions of Dwarf Fortress probably won't work so well.''',
    arguments = {
        'paths': '''Should be an iterable containing paths to individual raws files or to
            directories containing many. Files that do not yet exist in the raws will be
            added anew. Files that do exist will be compared to the current raws and the
            according additions/removals will be made. At least one path must be given.'''
    },
    compatibility = '.*'
)
def diff(df, paths):
    
    # Get all the files in the mods
    newfiles = []
    for path in paths:
        if os.path.isfile(path) and path.endswith('.txt'):
            with open(path, 'rb') as rfilestream:
                rfiles = (raws.rawfile(rfile=rfilestream, path=path),)
        elif os.path.isdir(path):
            rfiles = raws.dir(path=path).files.values()
        else:
            return pydwarf.failure('Failed to load raws from path %s.' % path)
        newfiles.append(rfiles)
    
    operations = {}
    conflicts = 0
    
    currentfiletokensdict = {}
    for newfilelist in newfiles:
        for newfile in newfilelist:
            pydwarf.log.info('Handling diff for file %s...' % newfile.header)
            
            # Get list of tokens for current file (And don't do it for the same file twice)
            currentfiletokens = None
            if newfile.header in currentfiletokensdict:
                currentfiletokens = currentfiletokensdict[newfile.header]
            elif newfile.header in df.files:
                currentfiletokens = list(df.getfile(newfile.header))
                currentfiletokensdict[newfile.header] = currentfiletokens
            
            # Do a diff
            if currentfiletokens:
                newfiletokens = list(newfile.tokens())
                diff = difflib.SequenceMatcher(None, currentfiletokens, newfiletokens)
                if newfile.header not in operations: operations[newfile.header] = {'insert': [], 'delete': [], 'replace': [], 'equal': []}
                for item in diff.get_opcodes():
                    if item[0] != 'equals':
                        op = item[0]
                        operations[newfile.header][op].append(diffrecord(currentfiletokens, newfiletokens, newfile.path, *item))
                                
            # File doesn't exist yet, don't bother with a diff
            else:
                pydwarf.log.debug('File didn\'t exist yet, adding...')
                df.add(newfile)
                
    for fileheader, fileops in operations.iteritems():
        # Do some handling for potentially conflicting replacements
        for i in xrange(0, len(fileops['replace'])):
            irecord = fileops['replace'][i]
            if not irecord.ignore:
                for j in xrange(i+1, len(fileops['replace'])):
                    jrecord = fileops['replace'][j]
                    # Replacements overlap?
                    if (jrecord.bpath is not irecord.bpath) and (irecord.afrom <= jrecord.auntil and jrecord.afrom <= irecord.auntil):
                        jrecord.ignore = True
                        if not raws.helpers.tokensequal(irecord.btokens(), jrecord.btokens()):
                            # Replacements aren't identical (this means there's a conflict)
                            if not irecord.conflicts: irecord.conflicts = []
                            irecord.conflicts.append(jrecord)
                            
        # Make replacements (insertions)
        for record in fileops['replace']:
            if not record.ignore:
                if record.conflicts is None:
                    tokens = record.btokens()
                else:
                    # Handle conflicts
                    pydwarf.log.error('Encountered potentially conflicting changes in %s, block replaced by %d input files.' % (fileheader, len(record.conflicts)+1))
                    tokens = []
                    lasttoken = None
                    for conflict in record.conflicts + [record]:
                        conflict.blower.prefix = '\n<<<diff from %s;%s' % (conflict.bpath, conflict.blower.prefix if conflict.blower.prefix else '')
                        for token in conflict.btokens():
                            lasttoken = token
                            tokens.append(token)
                        lasttoken.suffix = '%s\n>>>\n' % (lasttoken.suffix if lasttoken.suffix else '')
                    tokens[0].prefix = '\n<<<<<<diff potential conflict! block modified by %d files %s;\n%s' % (len(record.conflicts)+1, ', '.join([r.bpath for r in record.conflicts] + [record.bpath]), tokens[0].prefix if tokens[0].prefix else '')
                    lasttoken.suffix = '%s\n>>>>>>\n\n' % (lasttoken.suffix if lasttoken.suffix else '')
                    conflicts += 1
                tokens = record.alower.add(tokens=raws.helpers.copytokens(tokens))
                
        # Make insertions
        for record in fileops['insert']:
            record.alower.add(raws.helpers.copytokens(tokens=record.btokens()))
            
        # Make deletions
        for record in fileops['delete']:
            for token in record.atokens():
                token.remove()
                
        # Make replacements (deletions)
        for record in fileops['replace']:
            for token in record.atokens():
                token.remove()
        
    if conflicts == 0:
        return pydwarf.success('Merged %d mods without conflicts.' % len(paths))
    else:
        return pydwarf.failure('Merged %d mods with %d conflicts. Recommended you search in outputted raws for text like "<<<<<<diff potential conflict!" and resolve manually.' % (len(paths), conflicts))
