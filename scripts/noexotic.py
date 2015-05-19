import pydwarf

@pydwarf.urist(
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Replaces all [PET_EXOTIC] and [MOUNT_EXOTIC] tags with their non-exotic counterparts.'
)
def noexotic(raws):
    pets = raws.all('PET_EXOTIC')
    mounts = raws.all('MOUNT_EXOTIC')
    for token in pets: token.value = 'PET'
    for token in mounts: token.value = 'MOUNT'
    return pydwarf.success('Replaced %d PET_EXOTIC and %d MOUNT_EXOTIC tokens.' % (len(pets), len(mounts)))
