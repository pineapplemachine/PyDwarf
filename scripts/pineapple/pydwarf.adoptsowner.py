import pydwarf

@pydwarf.urist(
    name = 'pineapple.adoptsowner',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = '''todo''',
    arguments = {
        'remove_from': '''If set to None, no ADOPTS_OWNER tokens are removed.
            If set to '*', all ADOPTS_OWNER tokens are removed. If set to an
            iterable containing IDs of creatures, ADOPTS_OWNER will be
            removed from each of those creatures.''',
        'add_to': '''If set to None, no ADOPTS_OWNER tokens are added. If set
            to '*', tokens are added to all creatures. If set to an iterable
            containing IDs of creatures, ADOPTS_OWNER will be added to each
            of those creatures.''',
        'token': '''If set to something other than ADOPS_OWNER, the script is
            instead applied to that token.'''
    },
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def adoptsowner(df, remove_from='*', add_to=None, token='ADOPTS_OWNER'):
    removed = 0
    added = 0
    
    # Remove tokens
    if remove_from == '*':
        for removetoken in df.all(token):
            removetoken.remove()
            removed += 1
    elif remove_from:
        for creaturetoken in df.allobj(type='CREATURE', id_in=remove_from):
            for removetoken in creaturetoken.allprop(token): 
                removetoken.remove()
                removed += 1
        
    # Add tokens
    if add_to:
        for creaturetoken in df.allobj(type='CREATURE', id_in=(None if add_to == '*' else add_to)):
            if not creaturetoken.getprop(token):
                creaturetoken.addprop(token)
                added += 1
        
    # All done!
    if removed or added:
        return pydwarf.success('Added %d %s tokens and removed %d.' % (added, token, removed))
    else:
        return pydwarf.failure('Didn\'t add or remove any %s tokens.' % token)
