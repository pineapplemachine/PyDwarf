# Defines functions common to shukaro mods

import raws

default_entities = ('MOUNTAIN',)

def getentities(dfraws, entities):
    return dfraws.all(exact_value='ENTITY', re_args=('|'.join(entities),))
    
def addraws(pydwarf, dfraws, rawsdir, entities, extratokens=None):
    # Get the entities that need to have permitted things added to them.
    entitytokens = getentities(dfraws, entities)
    if len(entitytokens) != len(entities):
        if len(entitytokens):
            pydwarf.log.error('Of entities %s passed by argument, only %s were found.' % (entities, entitytokens))
        else:
            return pydwarf.failure('Found none of entities %s to which to add permitted buildings and reactions.' % entities)
            
    # Read the raws
    try:
        shukaroraws = raws.dir(path=rawsdir, log=pydwarf.log)
    except:
        pydwarf.log.exception('Failed to load raws from %s.' % rawsdir)
        return pydwarf.failure('Failed to load raws from %s.' % rawsdir)
        
    # Add new buildings and reactions to entities, and whatever else needs adding
    buildings = shukaroraws.all(exact_value='BUILDING_WORKSHOP', args_count=1)
    reactions = shukaroraws.all(exact_value='REACTION', args_count=1)
    for entity in entitytokens:
        if extratokens: entity.add(extratokens)
        for building in buildings: entity.add(raws.token(value='PERMITTED_BUILDING', args=(building.args[0],)))
        for reaction in reactions: entity.add(raws.token(value='PERMITTED_REACTION', args=(reaction.args[0],)))
    pydwarf.log.info('Added %d permitted buildings and %d permitted reactions to %d entities.' % (len(buildings), len(reactions), len(entitytokens)))
    
    # Add new files
    for filename, rfile in shukaroraws.files.iteritems():
        if filename not in dfraws: dfraws.addfile(rfile=rfile)
        
    # All done!
    return pydwarf.success()
