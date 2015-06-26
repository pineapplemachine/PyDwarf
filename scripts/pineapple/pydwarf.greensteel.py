import os
import pydwarf



greendir = pydwarf.rel(__file__, 'raw/greensteel')
added_reactions = (
    'GREEN_STEEL_MAKING_ADAMANT_PINEAPPLE',
    'GREEN_STEEL_MAKING_ADMANTINE_PINEAPPLE',
)



default_entities = ['MOUNTAIN']



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
    try:
        df.add(path=greendir, loc='raw/objects')
        return pydwarf.urist.getfn('pineapple.utils.addtoentity')(
            df,
            entities = entities,
            permitted_reaction = added_reactions
        )
    except:
        pydwarf.log.exception('Failed to add greensteel raws.')
        return pydwarf.failure()
