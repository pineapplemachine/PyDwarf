import pydwarf
import raws

default_templates = {
    'WOOD_TEMPLATE': 'WOOD',
    'METAL_TEMPLATE': 'BARS',
    'STONE_TEMPLATE': 'BOULDER'
}

@pydwarf.urist(
    name = 'pineapple.butcherinorganic',
    title = 'Butcher Inorganic Corpses',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Allows butchering of some inorganics, get things like wood
        or stone from some corpses. Inspired by/stolen from Igfig's Modest Mod.''',
    arguments = {
        'templates': '''Associates material template names as keys with items as
            values. Each named template will be given a BUTCHER_SPECIAL:ITEM:NONE
            token, where ITEM is the value given. Defaults to adding logs, bars,
            and boulders to wood, metal, and stone templates respectively.'''
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def butcherinorganic(df, templates=default_templates):
    added = 0
    
    # Apply BUTCHER_SPECIAL tokens to material templates
    for templatename, butcherspecial in templates.iteritems():
        template = df.getobj(type='MATERIAL_TEMPLATE', exact_id=templatename)
        if template:
            pydwarf.log.debug('Adding BUTCHER_SPECIAL item %s to material template %s.' % (butcherspecial, templatename))
            template.addprop(raws.token(value='BUTCHER_SPECIAL', args=[butcherspecial, 'NONE']))
            added += 1
        else:
            pydwarf.log.error('Unable to find template %s, skipping.' % templatename)
            
    # All done!
    if added > 0:
        return pydwarf.success('Added BUTCHER_SPECIAL to %d material templates.' % added)
    else:
        return pydwarf.failure('Added BUTCHER_SPECIAL to no material templates.')
