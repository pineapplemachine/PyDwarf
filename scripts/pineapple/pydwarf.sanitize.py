import pydwarf
import raws



def objectdict(df):
    allobj = df.allobj()
    objects = {}
    for token in allobj:
        if token.value not in objects: objects[token.value] = {}
        if token.arg() not in objects[token.value]: objects[token.value][token.arg()] = raws.tokenlist()
        objects[token.value][token.arg()].append(token)
    return objects

def itertokens(objects):
    for objecttype, ids in objects.iteritems():
        for id, tokens in ids.iteritems():
            for token in tokens:
                yield token



@pydwarf.urist(
    name = 'pineapple.sanitize.nonexistentids',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''
        Checks for and removes any instances where a COPY_TAGS_FROM or similar token refers
        to an ID that doesn't exist.
    ''',
    arguments = {},
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def nonexistentids(df, objects=None):
    if objects is None: objects = objectdict(df)
    
    # Keep going while we're removing stuff - we might remove something that something else depended on
    removals = True
    while removals:
        removals = []
        
        # Assign tokens for removal
        for token in itertokens(objects):
            # Determine which sorts of tokens need to be looked at for this
            checktokens = [('COPY_TOKENS_FROM', token.value)]
            if token.value == 'INORGANIC':
                checktokens.append(('USE_MATERIAL_TEMPLATE', 'MATERIAL_TEMPLATE'))
            elif token.value == 'CREATURE':
                checktokens.append(('APPLY_CREATURE_VARIATION', 'CREATURE_VARIATION'))
            # Verify that all those IDs actually exist
            for tokenvalue, objecttype in checktokens:
                for template in token.allprop(tokenvalue):
                    if template.arg(0) not in objects.get(objecttype, []): removals.append(token)
                    
        # Perform those removals
        for token in removals:
            pydwarf.log.debug('Removing %s.' % token)
            token.removeselfandallprops()
    