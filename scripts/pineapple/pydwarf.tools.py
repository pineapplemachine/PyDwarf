import pydwarf
import raws



toolsdir = pydwarf.rel(__file__, 'raw/tools')



@pydwarf.urist(
    name = 'pineapple.tools.dagger',
    title = 'Add Dagger',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Adds daggers, which are smaller and less lethal than
        short swords, and may be held as tools by civilians. They can be
        made from one unit of metal, stone, or ceramics.''',
    arguments = {
        'entities': '''The entities which should be allowed to produce daggers.
            Defaults to all entities.'''
    }
)
def dagger(df, entities='*'):
    return pydwarf.scripts.pineapple.easypatch(
        df,
        files = toolsdir + '/item_weapon_dagger_pineapple.txt',
        loc = 'raw/objects',
        permit_entities = entities
    )

@pydwarf.urist(
    name = 'pineapple.tools.hatchet',
    title = 'Add Hatchet',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Adds hatchets, small axes which make for weak weapons but
        adequate tree-chopping tools. They can be made from two units of metal
        or stone.''',
    arguments = {
        'entities': '''The entities which should be allowed to produce hatchets.
            Defaults to MOUNTAIN and PLAINS.'''
    }
)
def hatchet(df, entities=['MOUNTAIN', 'PLAINS']):
    return pydwarf.scripts.pineapple.easypatch(
        df,
        files = toolsdir + '/item_weapon_hatchet_pineapple.txt',
        loc = 'raw/objects',
        permit_entities = entities
    )

@pydwarf.urist(
    name = 'pineapple.tools.mallet',
    title = 'Add Mallet',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Adds mallets, small hammers which may be carried as tools
        by civilians and are somewhat suitable as weapons. They can be made
        from two units of metal, stone, or wood.''',
    arguments = {
        'entities': '''The entities which should be allowed to produce mallets.
            Defaults to all entities.'''
    }
)
def mallet(df, entities='*'):
    return pydwarf.scripts.pineapple.easypatch(
        df,
        files = toolsdir + '/item_weapon_mallet_pineapple.txt',
        loc = 'raw/objects',
        permit_entities = entities
    )

@pydwarf.urist(
    name = 'pineapple.tools.staff',
    title = 'Add Staff',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Adds staves, which are tools that may be carried by
        civilains. They are also serviceable as weapons and can be made
        from three units of metal or wood.''',
    arguments = {
        'entities': '''The entities which should be allowed to produce staves.
            Defaults to all entities.'''
    }
)
def staff(df, entities='*'):
    return pydwarf.scripts.pineapple.easypatch(
        df,
        files = toolsdir + '/item_weapon_staff_pineapple.txt',
        loc = 'raw/objects',
        permit_entities = entities
    )
