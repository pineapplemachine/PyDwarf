import pydwarf

@pydwarf.urist(
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Replaces all [PET_EXOTIC] and [MOUNT_EXOTIC] tags with their non-exotic counterparts.',
    # Definitely compatible with 0.40.x and 0.31.x, probably works with anything else too and should
    # at least not break anything even if not.
    compatibility = ('0\.(40|31)\..*', '.*')
)
def noexotic(raws):
    pets = raws.all('PET_EXOTIC')
    mounts = raws.all('MOUNT_EXOTIC')
    for token in pets: token.value = 'PET'
    for token in mounts: token.value = 'MOUNT'
    if len(pets) or len(mounts):
        return pydwarf.success('Replaced %d PET_EXOTIC and %d MOUNT_EXOTIC tokens.' % (len(pets), len(mounts)))
    else:
        return pydwarf.failure('I found no PET_EXOTIC or MOUNT_EXOTIC tokens to replace.')
