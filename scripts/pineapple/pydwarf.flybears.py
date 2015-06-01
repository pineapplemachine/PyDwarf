import pydwarf

@pydwarf.urist(
    name = 'pineapple.flybears',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Example script which causes all female bears to fly.',
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def flybears(raws):
    # Get all bear creature tokens
    bears = raws.allobj('CREATURE', re_id='BEAR_.+')
    
    # Add [FLIER] to each of them, immediately after the first CASTE:FEMALE token
    for bear in bears:
        bear.get('CASTE:FEMALE').add('FLIER')
        
    # All done!
    if len(bears):
        return pydwarf.success('Made %d bear species fliers.' % len(bears))
    else:
        return pydwarf.failure('Couldn\'t find any bears to make fliers.')
