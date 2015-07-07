import pydwarf

@pydwarf.urist(
    name = 'pineapple.noaquifers',
    version = '1.0.1',
    author = 'Sophie Kirschner',
    description = 'Removes all AQUIFER tokens.',
    compatibility = (pydwarf.df_0_27, pydwarf.df_0_28, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def noaquifers(df):
    # Do the removing
    aquifers = df.removeall('AQUIFER')
    # All done!
    if len(aquifers):
        return pydwarf.success('Removed %d AQUIFER tokens.' % len(aquifers))
    else:
        return pydwarf.failure('Found no AQUIFER tokens.')
