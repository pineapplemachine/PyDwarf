import pydwarf
import raws



default_creatures = ('DWARF', 'ELF', 'HUMAN', 'GOBLIN')

mode_info = {
    'hetero': ( # Straight
        1,      # disinterest in same gender
        0,      # interest in same gender (no marriage)
        0,      # commitment to same gender (marriage)
        0,      # disinterest in other gender
        0,      # interest in other gender (no marriage)
        1       # commitment to other gender
    ),
    'gay': ( # Gay
        0, 0, 1,
        1, 0, 0
    ),
    'bi': ( # Bisexual
        0, 0, 1,
        0, 0, 1
    ),
    'ace': ( # Asexual
        1, 0, 0,
        1, 0, 0
    ),
    'default': ( # DF's default values
        75, 20, 5,
        5, 20, 75
    )
}

default_lover_chance = (0, 0)



@pydwarf.urist(
    name = 'pineapple.orientation',
    title = 'Change Sexual Orientation',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Causes all creatures of some type to have a single sexuality,
        heterosexual being the default. (You boring snob!)''',
    arguments = {
        'creatures': '''An iterable containing creatures whose sexuality should be
            affected. Set to None to affect all creatures.''',
        'mode': '''Accepts one of these strings as its value, or None: 
            "hetero", the default, makes the creatures exclusively straight.
            "gay" makes the creatures exclusively gay.
            "bi" makes the creatures exclusively bisexual.
            "ace" makes the creatures exclusively asexual.
            Can alternatively be set as a custom tuple same as those found in the
            mode_info dict: The list/tuple should contain six values corresponding
            to (disinterest in the same gender, romantic (but not marriage) 
            interest in the same, commitment to the same, disinterest in the other
            gender, romantic interest in the other, commitment to the other).''',
    },
    compatibility = pydwarf.df_0_40
)
def orientation(df, creatures=default_creatures, mode='hetero', lover_chance=default_lover_chance):
    if isinstance(mode, basestring):
        if mode not in mode_info: return pydwarf.failure('Invalid mode %s. Recognized modes are these: %s.' % (mode, ', '.join(mode_tokens.keys())))
        usemode = mode_info[mode]
    else:
        usemode = mode
    
    # Unpack variables for convenience
    disinterestsame, loversame, commitsame, disinterestother, loverother, commitother = usemode
    
    # Get tokens for all the specified creatures
    creatures = df.allobj(type='CREATURE', id_in=creatures)
    pydwarf.log.debug('Found %d applicable creatures.' % len(creatures))
    
    # Add tokens after [FEMALE] and [MALE] tokens
    added = 0
    for creature in creatures:
        pydwarf.log.debug('Applying ORIENTATION changes to %s.' % creature)
        
        # Remove any existing ORIENTATION tokens
        removetokens = creature.allprop(exact_value='ORIENTATION')
        if len(removetokens):
            pydwarf.log.debug('Removing %d existing ORIENTATION tokens from token %s.' % (len(removetokens), gendertoken))
            for removetoken in removetokens: removetoken.remove()
        
        # Add the new orientation tokens
        gendertokens = creature.allprop(value_in=('FEMALE', 'MALE'), args_count=0)
        for gendertoken in gendertokens:
            othergender = 'FEMALE' if gendertoken.value == 'MALE' else 'MALE'
            gendertoken.add(raws.token(value='ORIENTATION', args=[othergender, disinterestother, loverother, commitother]))
            gendertoken.add(raws.token(value='ORIENTATION', args=[gendertoken.value, disinterestsame, loversame, commitsame]))
            added += 1
    
    # All done!
    if added > 0:
        return pydwarf.success('Appended ORIENTATION tokens after %d gender tokens.' % added)
    else:
        return pydwarf.failure('Found no gender tokens to add ORIENTATION to.')
