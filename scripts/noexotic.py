# Replace all [PET_EXOTIC] and [MOUNT_EXOTIC] tags with their non-exotic counterparts
def noexotic(raws):
    pets = raws.all('PET_EXOTIC')
    mounts = raws.all('MOUNT_EXOTIC')
    for token in pets: token.value = 'PET'
    for token in mounts: token.value = 'MOUNT'
    return {'success': True, 'status': 'Replaced %d PET_EXOTIC and %d MOUNT_EXOTIC tokens.' % (len(pets), len(mounts))}
