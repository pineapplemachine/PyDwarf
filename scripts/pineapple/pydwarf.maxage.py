import pydwarf
import raws

default_ages = {
    'CREEPING_EYE': (80, 95),
    'POND_GRABBER': (10, 15),
    'CAVE_DRAGON': (3800, 4600),
    'CAVE_BLOB': (5, 15),
    'SEA_MONSTER': (550, 610),
    'ELF': (480, 600),
    'GOBLIN': (55, 75),
    'SATYR': (120, 135),
    'GIANT': (60, 95),
    'CYCLOPS': (60, 95),
    'ETTIN': (35, 55),
    'MINOTAUR': (70, 105),
    'BLIZZARD_MAN': (100, 130),
    'FAIRY': (10, 15),
    'PIXIE': (10, 15),
    'GRIMELING': (30, 45),
    'BLENDEC_FOUL': None, # Immortal
    'NIGHTWING': (60, 80),
    'HARPY': (180, 220),
    'WAMBLER_FLUFFY': (5, 10),
    'IMP_FIRE': None, # Immortal
    'SNAKE_FIRE': (10, 15),
    'MAGGOT_PURRING': (10, 15)
}

@pydwarf.urist(
    name = 'pineapple.maxage',
    title = 'Add MAXAGE Tokens',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Applies a MAXAGE to most vanilla creatures which don't already have one.''',
    arguments = {
        'ages': '''A dictionary mapping creature names as keys to what that creature's arguments
            should be for MAXAGE: That is, it should look like (minimum_lifespan, maximum_lifespan).''',
        'output_needs_age': '''When True, creatures that have no MAXAGE and aren't specified in the
            ages dict will be outputted to the log. Can maybe be helpful for debugging things.''',
        'apply_default_age': '''Most creatures that don't have a MAXAGE and aren't specified in the
            ages dict will have this default applied to their MAXAGE. It should be an iterable
            containing arguments same as values in the ages dict. This will not be applied to wagons,
            to megabeasts, to undead, or to nonexistent creatures.'''
    },
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def maxage(df, ages=default_ages, apply_default_age=None, output_needs_age=False):
    added = []
    modified = []
    
    # Handle each creature
    for creaturetoken in df.allobj('CREATURE'):
        creaturename = creaturetoken.args[0]
        maxage = creaturetoken.getprop('MAXAGE')
        
        # Creature is in the ages dict, give it the age specified
        if creaturename in ages:
            agetuple = ages.get(creaturename)
            if agetuple is not None:
                pydwarf.log.debug('Applying MAXAGE %s to %s...' % (agetuple, creaturetoken))
                if maxage:
                    modified.append(creaturename)
                    maxage.args = list(agetuple)
                else:
                    added.append(creaturename)
                    creaturetoken.addprop(raws.token(value='MAXAGE', args=list(agetuple)))
                    
        # Creature isn't in the ages dict, check about applying a default or simply outputting its existence
        elif (not maxage) and (output_needs_age or apply_default_age):
            props = creaturetoken.propdict()
            if not(
                'COPY_TAGS_FROM' in props or    
                'EQUIPMENT_WAGON' in props or
                'MEGABEAST' in props or
                'DOES_NOT_EXIST' in props or
                'NOT_LIVING' in props
            ):
                if apply_default_age is not None:
                    pydwarf.log.debug('Applying default MAXAGE %s to %s...' % (apply_default_age, creaturetoken))
                    creaturetoken.addprop(raws.token(value='MAXAGE', args=list(apply_default_age)))
                    added.append(creaturename)
                else:
                    pydwarf.log.info('Creature %s has no MAXAGE.')
                    
    # All done!
    pydwarf.log.debug('Modified MAXAGE tokens of creatures: %s.' % modified)
    pydwarf.log.debug('Added MAXAGE tokens to creatures: %s.' % added)
    if len(added) or len(modified):
        return pydwarf.success('Added %d MAXAGE tokens and modified %d existing ones.' % (len(added), len(modified)))
    else:
        return pydwarf.failure('No MAXAGE tokens affected.')
