import pydwarf



reduce_dir = pydwarf.rel(__file__, 'raw/microreduce')

default_entities = 'MOUNTAIN'



@pydwarf.urist(
    name = 'putnam.microreduce',
    version = '1.0.1',
    author = ('Putnam', 'Sophie Kirschner'),
    description = 'A mod to reduce the amount of micromanagement in Dwarf Fortress. One-step soap making and clothesmaking!',
    compatibility = pydwarf.df_0_40
)
def microreduce(df, entities=default_entities):
    return pydwarf.urist.getfn('pineapple.easypatch')(
        df,
        files = reduce_dir,
        loc = 'raw/objects',
        permit_entities = entities  
    )
