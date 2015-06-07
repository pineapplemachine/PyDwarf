import pydwarf



default_options = {
    'scales': ('SCALE_TEMPLATE', '[LEATHER][ITEMS_LEATHER][MATERIAL_REACTION_PRODUCT:TAN_MAT:LOCAL_CREATURE_MAT:SCALE]'),
    'feathers': ('FEATHER_TEMPLATE', '[PEARL][ITEMS_SOFT]'),
    'chitin': ('CHITIN_TEMPLATE', '[SHELL][ITEMS_HARD][ITEMS_SCALED]')
}



@pydwarf.urist(
    name = 'pineapple.useablemats',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = '''Causes scales, feathers, and chitin to become useful for crafting.
        Inspired by/stolen from Rubble's Usable Scale/Feathers/Chitin fixes.''',
    arguments = {
        'options': '''A dictionary associating option names with tuples where the first
            element is the name of a MATERIAL_TEMPLATE and the second is tokens to be
            added to that template. Option names, when passed as a keyword argument and
            set to False, will cause that option to be disabled.''',
        'scales': '''Recognized when using the default options dict. If set to True,
            scales will be made to act more like leather for crafting purposes.''',
        'feathers': '''Recognized when using the default options dict. If set to True,
            feathers will be useable for making soft items, such as clothing.''',
        'chitin': '''Recognized when using the default options dict. If set to True,
            chitin will be made to act more like shells for crafting purposes.'''
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def useable(df, options=default_options, **kwargs):
    failures = 0
    
    # Handle each option, simply adding some new tokens to each material template given
    for optionname, option in options.iteritems():
        pydwarf.log.debug('Handling material template option %s.' % optionname)
        if optionname not in kwargs or kwargs[optionname]:
            templatename, templatetokens = option
            template = df.getobj(type='MATERIAL_TEMPLATE', exact_id=templatename)
            if template:
                template.addprop(templatetokens)
                pydwarf.log.info('Added tokens to %s.' % templatename)
            else:
                pydwarf.log.error('Couldn\'t find %s.' % templatename)
                failures += 1
    
    # All done!
    if failures == 0:
        return pydwarf.success()
    else:
        return pydwarf.failure('Failed to add tokens to %d material templates.' % failures)
