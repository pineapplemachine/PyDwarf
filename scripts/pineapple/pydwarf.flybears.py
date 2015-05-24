import pydwarf

@pydwarf.urist(
    name = 'pineapple.flybears',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Causes all female bears to fly.',
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def flybears(raws):
    bears = raws.all(exact_value='CREATURE', re_args=['BEAR_.+'])
    for bear in bears:
        bear.get('CASTE:FEMALE').add('FLIER')
    if len(bears):
        return pydwarf.success('Made %d bear species fliers.' % len(bears))
    else:
        return pydwarf.failure('Couldn\'t find any bears to make fliers.')
