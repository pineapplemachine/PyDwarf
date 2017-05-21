import pydwarf
import raws



daggerdir = pydwarf.rel(__file__, 'raw/dagger')

default_entities = '*'



@pydwarf.urist(
    name = 'pineapple.dagger',
    title = 'Add Dagger Weapon',
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
def dagger(df, entities=default_entities):
    # Add greensteel raws
    return pydwarf.scripts.pineapple.easypatch(
        df,
        files = daggerdir,
        loc = 'raw/objects',
        permit_entities = entities
    )
