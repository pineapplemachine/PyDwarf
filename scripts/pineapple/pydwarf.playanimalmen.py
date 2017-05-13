import pydwarf

@pydwarf.urist(
    name = 'pineapple.playanimalmen',
    title = 'Animal Men Playable in Adventure Mode',
    version = '1.0',
    author = 'Sophie Kirschner',
    description = '''Makes all animal men playable in adventure mode by adding a
        [OUTSIDER_CONTROLLABLE] token to each.''',
)
def playanimalmen(df):
    added = set()
    
    for animalman in df.allobj('CREATURE', re_id='.+MAN'):
        needprops = ('LARGE_ROAMING', 'CAN_LEARN', 'CAN_SPEAK')
        if(
            animalman.getprop('APPLY_CREATURE_VARIATION:ANIMAL_PERSON') or
            all(animalman.getprop(prop) for prop in needprops)
        ):
            animalman.addprop('OUTSIDER_CONTROLLABLE')
            added.add(animalman.args[0])
    
    # All done, now let PyDwarf know the script did its job successfully.
    return pydwarf.success('Added OUTSIDER_CONTROLLABLE tokens to %d creatures.' % len(added))
