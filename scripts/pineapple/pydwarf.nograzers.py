import pydwarf

@pydwarf.urist(
    name = 'pineapple.nograzers',
    title = 'Remove Grazing Tokens',
    version = '1.0.1',
    author = 'Sophie Kirschner',
    description = 'Removes all [GRAZER] and [STANDARD_GRAZER] tokens.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def nograzers(df):
    # Do the removing
    grazers = df.removeall('GRAZER')
    standardgrazers = df.removeall('STANDARD_GRAZER')
    
    # All done!
    if len(grazers) or len(standardgrazers):
        return pydwarf.success('Removed %d GRAZER and %d STANDARD_GRAZER tokens.' % (len(grazers), len(standardgrazers)))
    else:
        return pydwarf.failure('I found no grazer tokens to remove.')
