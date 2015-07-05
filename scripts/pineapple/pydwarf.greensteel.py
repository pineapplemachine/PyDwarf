import pydwarf
import raws



greendir = pydwarf.rel(__file__, 'raw/greensteel')

default_entities = 'MOUNTAIN'



@pydwarf.urist(
    name = 'pineapple.greensteel',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Adds an alloy which is lighter and sharper than steel but not so much
        as adamantine. It can be made from similar ingredients as steel with the addition
        of adamantine bars or a new adamant ore.''',
    arguments = {
        'entities': '''The entities which should be permitted this reaction. Defaults to
            only MOUNTAIN.'''
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def greensteel(df, entities=default_entities):
    # Add greensteel raws
    return pydwarf.urist.getfn('pineapple.easypatch')(
        df,
        files = greendir,
        loc = 'raw/objects',
        permit_entities = entities
    )
