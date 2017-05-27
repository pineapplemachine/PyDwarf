import pydwarf



@pydwarf.urist(
    name = 'pineapple.playcivs.controllable',
    title = 'Civilizations Playable in Fortress Mode',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Makes civilizations playable in fortress mode by adding
        [SITE_CONTROLLABLE] tokens to them. Defaults to making all civilizations
        controllable in this way, but the script accepts an entities argument
        that can be used to set which entities should receive the token. Any
        entities which possess the token at the time of running the script but
        aren't in the entities list will have the token removed!
        Note that if this isn't used in conjunction with other mods, it may not
        be practical to play as non-dwarf civilizations due to missing items,
        professions, reactions, etc.''',
    arguments = {
        'entities': '''The entities to which [SITE_CONTROLLABLE] tokens should
            belong. Defaults to "*", meaning all entities should be controllable.'''
    }
)
def controllable(df, entities='*'):
    controllable = set()
    
    if entities == '*': # Enable all entities
        for entity in df.allobj('ENTITY'):
            entity.setprop('SITE_CONTROLLABLE')
            controllable.add(entity.args[0])
    else: # Enable listed entities and disable others
        entities = set([entities]) if isinstance(entities, basestring) else set(entities)
        for entity in df.allobj('ENTITY'):
            if entity.args[0] in entities:
                entity.setprop('SITE_CONTROLLABLE')
                controllable.add(entity.args[0])
                entities.remove(entity.args[0])
            else:
                entity.removeprop('SITE_CONTROLLABLE')
        if entities:
            pydwarf.log.error(
                'Nonexistent objects in controllable entities list: %s' % ', '.join(entities)
            )
                
    if controllable:
        return pydwarf.success('Assigned %d controllable entities.' % len(controllable))
    else:
        return pydwarf.failure('Assigned no controllable entities.')
