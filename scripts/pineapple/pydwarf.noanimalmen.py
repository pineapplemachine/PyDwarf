import pydwarf

@pydwarf.urist(
    name = 'pineapple.noanimalmen',
    title = 'Remove Animal Men',
    version = '1.0.1',
    author = 'Sophie Kirschner',
    description = '''
        Removes all creatures which either have a [APPLY_CREATURE_VARIATION:ANIMAL_PERSON]
        token or have an ID ending in '_MAN'.
    ''',
    arguments = {},
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def noanimalmen(df):
    # Do the removing
    removed = [removedprop for removedprop in df.allobj('CREATURE').each(
        lambda token: token.removeselfandprops() if (
            token.arg().endswith('_MAN') or token.arg().endswith(' MAN') or
            token.getprop('APPLY_CREATURE_VARIATION:ANIMAL_PERSON')
        ) else None
    ) if removedprop]
    
    # All done!
    if removed:
        return pydwarf.success('Removed %d species of animal men.' % len(removed))
    else:
        return pydwarf.failure('Found no animal men to remove.')
