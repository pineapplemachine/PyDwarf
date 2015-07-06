import pydwarf

@pydwarf.urist(
    name = 'pineapple.noexotic',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = 'Replaces all [PET_EXOTIC] and [MOUNT_EXOTIC] tags with their non-exotic counterparts.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def noexotic(df):
    # Do the removing
    pets = df.all('PET_EXOTIC').each(lambda token: token.setvalue('PET'))
    mounts = df.all('MOUNT_EXOTIC').each(lambda token: token.setvalue('MOUNT'))
    
    # All done!
    if len(pets) or len(mounts):
        return pydwarf.success('Replaced %d PET_EXOTIC and %d MOUNT_EXOTIC tokens.' % (len(pets), len(mounts)))
    else:
        return pydwarf.failure('I found no PET_EXOTIC or MOUNT_EXOTIC tokens to replace.')
