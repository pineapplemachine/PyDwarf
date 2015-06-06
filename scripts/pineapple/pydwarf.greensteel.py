import os
import pydwarf

greendir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'raws/greensteel')


default_entities = ['MOUNTAIN']


@pydwarf.urist(
    name = 'pineapple.greensteel',
    version = 'alpha',
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
        df.read(path=greendir, log=pydwarf.log)
        return pydwarf.urist.getfn('pineapple.utils.addtoentity')(
            df,
            entities = entities,
            permitted_reaction = (
                'GREEN_STEEL_MAKING_ADAMANT_PINEAPPLE',
                'GREEN_STEEL_MAKING_ADMANTINE_PINEAPPLE'
            )
        )
    except:
        pydwarf.log.exception('Failed to add greensteel raws.')
        return pydwarf.failure()
