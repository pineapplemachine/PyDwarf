import pydwarf

@pydwarf.urist(
    name = 'pineapple.noexotic',
    title = 'No Exotic Pets or Mounts',
    version = '1.0.1',
    author = 'Sophie Kirschner',
    description = 'Replaces all [PET_EXOTIC] and [MOUNT_EXOTIC] tags with their non-exotic counterparts.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def noexotic(df):
    # Do the removing
    pets = df.all('PET_EXOTIC').each(lambda token: token.setvalue('PET'), none=True)
    mounts = df.all('MOUNT_EXOTIC').each(lambda token: token.setvalue('MOUNT'), none=True)
    
    # All done!
    if len(pets) or len(mounts):
        return pydwarf.success('Replaced %d PET_EXOTIC and %d MOUNT_EXOTIC tokens.' % (len(pets), len(mounts)))
    else:
        return pydwarf.failure('I found no PET_EXOTIC or MOUNT_EXOTIC tokens to replace.')
