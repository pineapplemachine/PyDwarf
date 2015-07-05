import pydwarf



wood_mechanisms_reaction = 

default_log_count = 1

default_entities = ['MOUNTAIN', 'PLAINS']

default_file = 'raw/objects/reaction_woodmechanisms_pineapple.txt'



@pydwarf.urist(
    name = 'pineapple.woodmechanisms',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Allows construction of wooden mechanisms at the craftdwarf's workshop.
        Inspired by/stolen from Rubble's Wooden Mechanisms mod.''',
    arguments = {
        'log_count': 'The number of logs required in the reaction.',
        'entities': 'Adds the reaction to these entities. Defaults to MOUNTAIN and PLAINS.',
        'add_to_file': 'Adds the reaction to this file.'
    },
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def woodmechanisms(df, log_count=default_log_count, entities=default_entities, add_to_file=default_file):
    return pydwarf.urist.getfn('pineapple.utils.addobject')(
        df,
        type = 'REACTION',
        id = 'WOODEN_MECHANISMS_PINEAPPLE',
        tokens = '''
            [NAME:craft wooden mechanisms]
            [BUILDING:CRAFTSMAN:NONE]
            [REAGENT:A:%d:WOOD:NONE:NONE:NONE]
            [PRODUCT:100:1:TRAPPARTS:NONE:GET_MATERIAL_FROM_REAGENT:A:NONE]
            [SKILL:MECHANICS]
        ''' % log_count,
        add_to_file = add_to_file,
        permit_entities = entities
    )
