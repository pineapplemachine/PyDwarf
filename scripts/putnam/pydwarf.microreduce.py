import os
import pydwarf
from raws import rawstoken

@pydwarf.urist(
    name = 'putnam.microreduce',
    version = 'alpha',
    author = ('Putnam', 'Sophie Kirschner'),
    description = 'A mod to reduce the amount of micromanagement in Dwarf Fortress. One-step soap making and clothesmaking!',
    compatibility = pydwarf.df_0_40
)
def microreduce(raws):
    mountain = raws.get('ENTITY:MOUNTAIN')
    if mountain:
        # Add files
        genericpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Microreduce', '%s.txt')
        for filename in ('building_macro_fantastic', 'item_macro_fantastic', 'reaction_macro_fantastic'):
            rfile = raws.addfile(path=genericpath % filename)
            # Add PERMITTED_BUILDING and PERMITTED_REACTION tokens to ENTITY:MOUNTAIN
            for building in rfile.all(re_value='BUILDING.*', args_count=1):
                mountain.add(rawstoken(value='PERMITTED_BUILDING', args=[building.args[0]]))
            for reaction in rfile.all(exact_value='REACTION', args_count=1):
                mountain.add(rawstoken(value='REACTION', args=[reaction.args[0]]))
        return pydwarf.success()
    else:
        return pydwarf.failure('Couldn\'t find ENTITY:MOUNTAIN.')
