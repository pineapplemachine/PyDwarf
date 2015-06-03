import pydwarf
import raws

default_required_property = ('INTELLIGENT', 'CAN_LEARN')

@pydwarf.urist(
    name = 'pineapple.nomaxage',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = '''Removes MAXAGE tokens from creatures.''',
    arguments = {
        'required_property': '''An iterable containing token values, e.g. ('INTELLIGENT', 'CAN_LEARN'):
            for each creature having both a MAXAGE token and one or more of these tokens, that
            creature's MAXAGE token will be removed. If set to None, then no MAXAGE tokens will be
            removed in this way. If set to ['*'], MAXAGE tokens will be removed from all creatures.''',
        'apply_to_creatures': '''Also removes MAXAGE from these creatures regardless of whether
            they possess any of the properties in required_property. Set to None to apply to no
            other creatures. Defaults to None.'''
    },
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def maxage(df, required_property=default_required_property, apply_to_creatures=None):
    removedfrom = []
    creaturedict = df.objdict('CREATURE')
    
    # Handle by properties
    if required_property:
        remove_all = len(required_property) == 1 and required_property[0] == '*'
        for creaturename, creaturetoken in creaturedict.iteritems():
            if remove_all or (creaturetoken.getprop(value_in=required_property) is not None):
                maxage = creaturetoken.getprop('MAXAGE')
                if maxage: maxage.remove(); removedfrom.append(creaturetoken)
                    
    # Handle by creature names
    if apply_to_creatures:
        for creaturename in apply_to_creatures:
            creaturetoken = creaturedict.get(creaturename)
            if creaturetoken:
                maxage = creaturetoken.getprop('MAXAGE')
                if maxage: maxage.remove(); removedfrom.append(creaturetoken)
            else:
                pydwarf.log.error('Couldn\'t find creature %s for removal of MAXAGE token.' % creaturename)
                
    # All done!
    pydwarf.log.debug('Removed MAXAGE tokens from creatures: %s.' % [token.args[0] for token in removedfrom])
    if len(removedfrom):
        return pydwarf.success('Removed MAXAGE tokens from %d creatues.' % len(removedfrom))
    else:
        return pydwarf.failure('Found no MAXAGE tokens to remove.')
        