import os
import pydwarf
import raws



mats_dir = pydwarf.rel(__file__, 'raw/materialsplus')

default_entities = 'MOUNTAIN'

add_paths = [os.path.join(mats_dir, path) for path in [
    'inorganic_alloys_mat_plus.txt',
    'inorganic_metals_mat_plus.txt',
    'inorganic_other_mat_plus.txt',
    'item_mat_plus.txt'
]]

patch_paths = [os.path.join(mats_dir, path) for path in [
    'reaction_alloys_mat_plus.txt',
    'reaction_production_mat_plus.txt'
]]



add_properties = [
    (
        # Identifier for making the log easier to understand
        'zircon',
        # Regex to match inorganic IDs
        '.* ZIRCON',
        # Add these properties
        'MATERIAL_REACTION_PRODUCT:KROLL_PROCESS:INORGANIC:ZIRCONIUM_PUTNAM'
    ),
    (
        'beryl',
        '.* BERYL|HELIODOR|MORGANITE|GOSHENITE|EMERALD',
        'REACTION_CLASS:BERYLLIUM'
    ),
    (
        'silicon',
        'ANDESITE|OLIVINE|HORNBLENDE|SERPENTINE|ORTHOCLASE|MICROCLINE|MICA',
        'REACTION_CLASS:SILICON'
    ),
    (
        'dolomite',
        'DOLOMITE',
        'REACTION_CLASS:PIDGEON_PROCESS'
    ),
    (
        'cromite',
        'CHROMITE',
        '[METAL_ORE:CHROMIUM_PUTNAM:100][METAL_ORE:IRON:50]'
    ),
    (
        'pyrolusite',
        'PYROLUSITE',
        'METAL_ORE:MANGANESE_PUTNAM:100'
    ),
]



@pydwarf.urist(
    name = 'putnam.materialsplus',
    version = '1.0.1',
    author = ('Putnam', 'Sophie Kirschner'),
    description = 'Adds a bunch of materials to the game.',
    compatibility = (pydwarf.df_0_34, pydwarf.df_0_40)
)
def materialsplus(df, entities=default_entities):
    # Add properties to various inorganics as defined by the add_properties dict
    errors = 0
    for identifier, re_id, addprops in add_properties:
        additions = df.allobj(type='INORGANIC', re_id=re_id).each(
            lambda token: token.addprop(addprops), none=True
        )
        if len(additions):
            pydwarf.log.debug('Added %s properties to %d inorganics.' % (identifier, len(additions)))
        else:
            errors += 1
            pydwarf.log.error('Failed to add %s properties because no matching inorganics were found.' % identifier)
    
    for path in add_paths:
        pydwarf.log.debug('Adding file at %s.' % path)
        df.add(path=path, loc='raw/objects')
    
    for path in patch_paths:
        response = pydwarf.urist.getfn('pineapple.easypatch')(
            df,
            files = path,
            loc = 'raw/objects',
            permit_entities = entities
        )
        if not response: return response
    
    if not errors:
        return pydwarf.success()
    else:
        return pydwarf.failure('Failed to add inorganic properties for %d groups.' % errors)
