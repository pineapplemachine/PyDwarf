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
    # Get subterranean plants
    subplants = []
    for plant in dfraws.allobj('PLANT'):
        if plant.getuntil(pretty='BIOME:SUBTERRANEAN_WATER', until_exact_value='PLANT'):
            subplants.append(plant)
    if not len(subplants): return pydwarf.failure('Found no subterranean plants.')
    
    # Ensure each has all four seasons
    pydwarf.log.info('Found %d subterranean plants. Modifying...' % len(subplants))
    modified = 0
    for subplant in subplants:
        pydwarf.log.debug('Handling %s...' % subplant)
        seasontokens = subplant.alluntil(value_in=seasons, until_exact_value='PLANT')
        if len(seasontokens) == 4:
            # First remove the existing tokens
            for seasontoken in seasontokens:
                seasontoken.remove()
            # Then add all four anew
            for season in seasons:
                subplant.add(raws.token(value=season))
            modified += 1
    
    # All done
    if modified > 0:
        return pydwarf.success('Made %d subterranean plants grow year-round.' % modified)
    else:
        return pydwarf.failure('All subterranean plants already grew year-round.')
