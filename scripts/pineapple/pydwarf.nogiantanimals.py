import pydwarf

@pydwarf.urist(
    name = 'pineapple.nogiantanimals',
    title = 'Remove Giant Creatures',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''
        Removes all creatures which either have a [APPLY_CREATURE_VARIATION:GIANT]
        token or have an ID matching a few patterns which involve the word 'GIANT' or 'GIGANTIC'.
    ''',
    arguments = {},
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def nogiantanimals(df):
    # Do the removing
    removed = [removedprop for removedprop in df.allobj('CREATURE').each(
        lambda token: (
            token.removeselfandprops() if(
                token.arg().startswith('GIANT_') or
                token.arg().endswith(', GIANT') or
                token.arg().endswith('_GIANT') or
                token.arg().startswith('GIANT ') or
                token.arg().startswith('GIGANTIC ') or
                token.getprop('APPLY_CREATURE_VARIATION:GIANT') 
            ) else None
        )
    ) if removedprop]
    
    # All done!
    if removed:
        return pydwarf.success('Removed %d species of giant animals.' % len(removed))
    else:
        return pydwarf.failure('Found no giant animals to remove.')
