import pydwarf



creation_dir = pydwarf.rel(__file__, 'raw/creationforge')

default_entities = ('MOUNTAIN',)



@pydwarf.urist(
    name = 'shukaro.creationforge',
    version = '1.0.0',
    author = ('Shukaro', 'Sophie Kirschner'),
    description = '''This is a simple workshop I modded in to help test custom reactions,
        buildings, and creatures. It's used to create various different items so that you
        don't have to set up an entire fortress to test some reactions. Hopefully it's a
        useful tool to people, even if it's just to look at the raw formatting. ''',
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def creationforge(df, entities=default_entities):
    return pydwarf.urist.getfn('pineapple.easypatch')(
        df,
        files = creation_dir,
        loc = 'raw/objects',
        permit_entities = entities  
    )
