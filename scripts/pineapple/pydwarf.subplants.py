import pydwarf
import raws

seasons = ('SPRING', 'SUMMER', 'AUTUMN', 'WINTER')

@pydwarf.urist(
    name = 'pineapple.subplants',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Makes all subterranean plants grow year-round.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def subterraneanplants(dfraws):
    subplants = []
    for plant in dfraws.allobj('PLANT'):
        if plant.getuntil(pretty='BIOME:SUBTERRANEAN_WATER', until_exact_value='PLANT'):
            subplants.append(plant)
    if not len(subplants): return pydwarf.failure('Found no subterranean plants.')
    pydwarf.log.info('Found %d subterranean plants. Modifying...' % len(subplants))
    for subplant in subplants:
        pydwarf.log.debug('Handling %s...' % subplant)
        for seasontoken in subplant.alluntil(value_in=seasons, until_exact_value='PLANT'):
            seasontoken.remove()
        for season in seasons:
            subplant.add(raws.token(value=season))
    return pydwarf.success('Made %d subterranean plants grow year-round.' % len(subplants))
