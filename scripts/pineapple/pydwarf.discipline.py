import math
import pydwarf
import raws



default_discipline_bonus = {
    'INTELLIGENT': 0.2,
    'TRAINABLE': 0.1,
    'LARGE_PREDATOR': 0.5,
    'LIKES_FIGHTING': 0.2,
    'CARNIVORE': 0.2,
    'EVIL': 0.6,
    'LAIR': 1.0,
    'MEGABEAST': 1.6,
    'SEMIMEGABEAST': 1.2,
    'NOPAIN': 0.2,
    'NOEMOTION': 0.4,
    'NOT_LIVING': 0.3
}

default_entity_bonus = 0.5

default_badger_bonus = 0.5



@pydwarf.urist(
    name = 'pineapple.discipline',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = '''Applies natural discipline skill bonuses to creatures that should probably
        have them. Credit to Mictlantecuhtli for creating the mod which inspired this one.
        www.bay12forums.com/smf/index.php?topic=140460.0''',
    arguments = {
        'discipline_bonus': '''A dict mapping property names to values: For each of these tokens
            that a creature possesses the corresponding bonuses are summed. The resulting value,
            rounded up, is used to determine the skill bonus.''',
        'entity_bonus': '''Handled separately, adds this value to the bonus for creatures which
            are listed as being members of any entity.''',
        'badger_bonus': '''Also handled separately, adds this skill bonus to badgers.'''
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def discipline(df, discipline_bonus=default_discipline_bonus, entity_bonus=default_entity_bonus, badger_bonus=default_badger_bonus):
    creaturedict = df.objdict('CREATURE')
    discbonusdict = {}
    
    # Add bonuses for badgers and for creatures with given properties
    pydwarf.log.info('Determining bonuses based on misc properties...')
    for creaturename, creaturetoken in creaturedict.iteritems():
        discbonusdict[creaturename] = badger_bonus if 'BADGER' in creaturename else 0.0
        for prop in creaturetoken.allprop(value_in=discipline_bonus):
            discbonusdict[creaturename] += discipline_bonus[prop.value]
            
    # Add bonus for creatures which are part of a civilization
    pydwarf.log.info('Determining bonuses for civilization membership...')
    for entitytoken in df.allobj('ENTITY'):
        for entitycreature in entitytoken.allprop(exact_value='CREATURE', args_count=1):
            if entitycreature.value not in discbonusdict: discbonusdict[entitycreature.arg()] = 0.0
            discbonusdict[entitycreature.arg()] += entity_bonus
        
    # Apply the discipline bonuses
    applied = 0
    for creaturename, discbonus in discbonusdict.iteritems():
        creaturetoken = creaturedict[creaturename]
        if creaturetoken.getprop(exact_value='NATURAL_SKILL', exact_arg=((0, 'DISCIPLINE'),)):
            pydwarf.log.debug('Creature %s already has natural discipline skill, skipping.' % creaturename)
        elif discbonus < 0:
            pydwarf.log.debug('Creature %s would receive a negative bonus %f, skipping.' % (creaturename, discbonus))
        elif discbonus > 0:
            roundedbonus = int(math.ceil(discbonus))
            pydwarf.log.debug('Applying bonus of %f (Rounded up to %d) to creature %s...' % (discbonus, roundedbonus, creaturename))
            creaturetoken.add(raws.token(value='NATURAL_SKILL', args=['DISCIPLINE', str(roundedbonus)]))
            applied += 1
            
    # All done!
    if applied > 0:
        return pydwarf.success('Gave natural discipline skill bonuses to %d creatures.' % applied)
    else:
        return pydwarf.failure('Gave natural discipline skill bonuses to no creatures.')
