import pydwarf



default_entities = ['MOUNTAIN']

default_file = 'raw/objects/reaction_smelter_bauxtoalum_pineapple.txt'



@pydwarf.urist(
    name = 'pineapple.bauxitetoaluminum',
    title = 'Smelt Bauxite to Aluminum',
    version = '1.0.2',
    author = 'Sophie Kirschner',
    description = '''Adds a reaction to the smelter to allow the creation of aluminum bars
    from bauxite (as ore) and cryolite (as flux). Credit to this forum discussion for the
    reaction and general inspiration:
    http://www.bay12forums.com/smf/index.php?topic=31523.0''',
    arguments = {
        'aluminum_value': '''Multiplies the MATERIAL_VALUE of aluminum by this much.
            Defaults to 0.75 to account for the increased availability of aluminum as a
            consequence of the new reaction.''',
        'entities': 'Adds the reaction to these entities. Defaults to only MOUNTAIN.',
        'add_to_file': 'Adds the reaction to this file.'
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def bauxitetoaluminum(df, aluminum_value=0.75, entities=default_entities, add_to_file=default_file):
    # Affect value of aluminum
    pydwarf.log.debug('Multiplying value of aluminum by %f.' % aluminum_value)
    try:
        aluminum = df.getobj('INORGANIC:ALUMINUM')
        if aluminum is None: return pydwarf.failure('Couldn\'t find aluminum token to affect its value.')
        matvaluetoken = aluminum.getprop('MATERIAL_VALUE')
        matvaluetoken.args[0] = int( float(matvaluetoken.args[0]) * aluminum_value )
    except:
        pydwarf.log.exception('Failed to affect value of aluminum.')
        return pydwarf.failure()
        
    # Add the reaction
    return pydwarf.urist.getfn('pineapple.utils.addobject')(
        df,
        type = 'REACTION',
        id = 'SMELT_BAUXITE_ALUMINUM_PINEAPPLE',
        tokens = '''
            [NAME:smelt aluminum from bauxite]
            [SMELTER]
            [REAGENT:1:STONE:NO_SUBTYPE:STONE:BAUXITE]
            [REAGENT:1:STONE:NO_SUBTYPE:STONE:CRYOLITE]
            [PRODUCT:100:1:BAR:NO_SUBTYPE:METAL:ALUMINUM]
            [FUEL]
        ''',
        add_to_file = add_to_file,
        permit_entities = entities
    )
