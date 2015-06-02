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
            creature's MAXAGE token will be removed. If set to None, then all MAXAGE tokens will be
            removed.'''
    },
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def maxage(df, required_property=default_required_property):
    removedfrom = []
    
    # Handle each creature
    for creaturetoken in df.allobj('CREATURE'):
        creaturename = creaturetoken.args[0]
        if required_property == None or (creaturetoken.getprop(value_in=required_property) is not None):
            maxage = creaturetoken.getprop('MAXAGE')
            if maxage:
                maxage.remove()
                removedfrom.append(creaturetoken)
                
    # All done!
    pydwarf.log.debug('Removed MAXAGE tokens from creatures: %s.' % [token.args[0] for token in removedfrom])
    if len(removedfrom):
        return pydwarf.success('Removed MAXAGE tokens from %d creatues.' % len(removedfrom))
    else:
        return pydwarf.failure('Found no MAXAGE tokens to remove.')
        