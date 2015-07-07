import pydwarf



library_dir = pydwarf.rel(__file__, 'raw/higherlearning')

default_entities = 'MOUNTAIN'

librarian_position = '''
    [POSITION:LIBRARIAN]
    [NAME:librarian:librarians]
    [SITE]
    [NUMBER:1]
    [RESPONSIBILITY:MEET_WORKERS]
    [APPOINTED_BY:EXPEDITION_LEADER]
    [APPOINTED_BY:MAYOR]
    [PRECEDENCE:180]
    [DO_NOT_CULL]
    [COLOR:5:0:0]
    [DUTY_BOUND]
    [REQUIRED_BEDROOM:1]
    [REQUIRED_OFFICE:1]
'''



@pydwarf.urist(
    name = 'shukaro.higherlearning',
    version = '1.0.1',
    author = ('Shukaro', 'Sophie Kirschner'),
    description = '''Have you ever wondered to yourself, "Man, my dwarves are such idiots,
        I wish I could chisel some intelligence into their heads."? No? Then, er, disregard
        that last bit. What I present to you, here and now, no strings attached, is a workshop
        to solve a problem that you probably didn't even know you had! I call it, the Dwarven
        Higher Learning Mod. Now, what this thingawazzit does, is give your dwarves an
        opportunity to polish up some skills that they may have trouble practicing elsewhere.
        You know the situation, Urist McDoctor has your legendary axedwarf on your table, and
        he's got no idea how to stop him from bleeding out from wounds caused by rogue fluffy
        wamblers. Or you have precious little metal available on the glacier you so stupidly
        bravely embarked on, so you can't afford to waste it on dabbling weaponsmiths who've
        never handled a hammer before in their lives. This mod's workshops allow training
        through the time-honored traditions of; hitting rocks until your hands bleed,
        performing repetitive actions that will sap your will to live, practicing your skills
        on subjects that are worth less than most peasants (and won't sue for malpractice),
        and studying the works of your fellow dwarves, knowing full-well that you'll never be
        quite as good as them.''',
    arguments = {
        'entities': '''An iterable containing names of entities the workshops will be
            added to. Defaults to only MOUNTAIN.'''
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x) # I think it should be compatible with 0.40.x? Haven't actually tried it yet.
)
def higherlearning(df, entities=default_entities):
    # Add librarian position
    response = pydwarf.urist.getfn('pineapple.utils.addtoentity')(
        df,
        entities = entities,
        tokens = librarian_position
    )
    if not response: return response
    
    # Add buildings, reactions, items from raws
    return pydwarf.urist.getfn('pineapple.easypatch')(
        df,
        files = library_dir,
        loc = 'raw/objects',
        permit_entities = entities  
    )
    