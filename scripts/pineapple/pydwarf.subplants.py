import pydwarf
import raws

seasons = ('SPRING', 'SUMMER', 'AUTUMN', 'WINTER')

@pydwarf.urist(
    name = 'pineapple.subplants',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = 'Makes all subterranean plants grow year-round.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def subterraneanplants(df):
    # Get subterranean plants
    subplants = []
    for plant in df.allobj('PLANT'):
        if plant.getuntil(pretty='BIOME:SUBTERRANEAN_WATER', until_exact_value='PLANT'):
            subplants.append(plant)
    if not len(subplants): return pydwarf.failure('Found no subterranean plants.')
    
    # Ensure each has all four seasons
    pydwarf.log.info('Found %d subterranean plants. Modifying...' % len(subplants))
    modified = 0
    for subplant in subplants:
        seasontokens = subplant.allprop(value_in=seasons)
        if len(seasontokens) > 0 and len(seasontokens) < len(seasons):
            pydwarf.log.debug('Adding season tokens to %s...' % subplant)
            # First remove the existing tokens (To avoid making duplicates)
            for seasontoken in seasontokens:
                seasontoken.remove()
            # Then add all four anew
            for season in seasons:
                subplant.add(raws.token(value=season))
            modified += 1
        else:
            pydwarf.log.debug('Plant %s either has no seasonal tokens or already has all of them, skipping.' % subplant)
    
    # All done
    if modified > 0:
        return pydwarf.success('Made %d subterranean plants grow year-round.' % modified)
    else:
        return pydwarf.failure('All subterranean plants already grew year-round.')
