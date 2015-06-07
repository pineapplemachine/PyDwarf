import os
import pydwarf
import raws

@pydwarf.urist(
    name = 'putnam.microreduce',
    version = '1.0.0',
    author = ('Putnam', 'Sophie Kirschner'),
    description = 'A mod to reduce the amount of micromanagement in Dwarf Fortress. One-step soap making and clothesmaking!',
    compatibility = pydwarf.df_0_40
)
def microreduce(dfraws):
    mountain = dfraws.get('ENTITY:MOUNTAIN')
    if mountain:
        # Add files
        genericpath = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Microreduce', '%s.txt')
        for filename in ('building_macro_fantastic', 'item_macro_fantastic', 'reaction_macro_fantastic'):
            rfile = dfraws.addfile(path=genericpath % filename)
            # Add PERMITTED_BUILDING and PERMITTED_REACTION tokens to ENTITY:MOUNTAIN
            for building in rfile.all(re_value='BUILDING.*', args_count=1):
                mountain.add(raws.token(value='PERMITTED_BUILDING', args=[building.args[0]]))
            for reaction in rfile.all(exact_value='REACTION', args_count=1):
                mountain.add(raws.token(value='REACTION', args=[reaction.args[0]]))
        return pydwarf.success()
    else:
        return pydwarf.failure('Couldn\'t find ENTITY:MOUNTAIN.')
