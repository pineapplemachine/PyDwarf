import pydwarf

# Utility function: When adding a token, also append "- WM" after it.
def addwm(token, pretty): token.add('\n\t[%s] - WM ' % pretty)

@pydwarf.urist(
    name = 'witty.restrictednobles',
    version = 'alpha',
    author = ('Witty', 'Sophie Kirschner'),
    description = '''Witty: This is a pretty simple mod I've been meaning to make for a
    while. This should restrict all nobles of a given dwarven civ to dwarves and only
    dwarves. edit: taking into consideration that non-dwarves will be functional fort
    citizens as of the next version, I've decided to go with another option. The newest
    addition will now only exclude goblins from dwarven positions, since their current 
    worldgen behavior still makes them the most likely to dominate dwarven nobility. But
    now the occasional elf or human king will get their fair dues. The dwarf-only
    "module" will still come packaged. Note this will require a new world to take effect.
    All raw changes will be indicated by the WM insignia.
    
    Sophie: By default, this script will only prevent goblins from becoming nobles. Set
    the onlydwarves flag to True in order to prevent all other races as well.
    ''',
    arguments = {
        'onlydwarves': '''Defaults to False. If True, only dwarves will be allowed to
            hold positions in Dwarven forts and civs. If False, only goblins will be
            prevented from holding those positions.'''
    },
    compatibility = pydwarf.df_0_40
)
def restrictnobles(raws, onlydwarves=False):
    return restrictnobles_custom(raws, (['DWARF'] if onlydwarves else None), (None if onlydwarves else ['GOBLIN']))

@pydwarf.urist(
    name = 'witty.restrictednobles_custom',
    version = 'alpha',
    author = ('Witty', 'Sophie Kirschner'),
    description = 'Allows allowing and preventing various species from becoming dwarven nobles.',
    args = {
        'inclusions': '''An iterable containing each species that should be specified as allowed.
            If any is allowed in this way, any species not specifically allowed will be disallowed.''',
        'exclusions': '''An iterable containing each species that should be disallowed. All
            species not disallowed in this way will be able to become dwarven nobles.'''
    },
    compatibility = pydwarf.df_0_40
)
def restrictnobles_custom(raws, inclusions=None, exclusions=None):
    mountain = raws.get('ENTITY:MOUNTAIN')
    if mountain:
        positions = mountain.alluntil(exact_value='POSITION', until_exact_value='ENTITY')
        if inclusions:
            pydwarf.log.debug('Handling position inclusions %s...' % inclusions)
            for inclusion in inclusions:
                for position in positions: addwm(position, 'ALLOWED_CLASS:WITTY_%s' % inclusion)
                creature = raws['creature_standard'].getobj('CREATURE', inclusion)
                if creature:
                    addwm(creature, 'CREATURE_CLASS:WITTY_%s' % inclusion)
                else:
                    return pydwarf.failure('Couldn\'t find CREATURE:%s.' % inclusion)
        if exclusions:
            pydwarf.log.debug('Handling position exclusions %s...' % exclusions)
            for exclusion in exclusions:
                for position in positions: addwm(position, 'REJECTED_CLASS:WITTY_%s' % exclusion)
                creature = raws['creature_standard'].getobj('CREATURE', exclusion)
                if creature:
                    addwm(creature, 'CREATURE_CLASS:WITTY_%s' % exclusion)
                else:
                    return pydwarf.failure('Couldn\'t find CREATURE:%s.' % exclusion)
        return pydwarf.success('Restricted %d positions.' % len(positions))
    else:
        return pydwarf.failure('Couldn\'t find ENTITY:MOUNTAIN.')
    