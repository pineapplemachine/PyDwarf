import pydwarf
import raws



threats_path = pydwarf.rel(__file__, 'data/smallthings/threat.txt')
nofamily_path = pydwarf.rel(__file__, 'data/smallthings/no_family.txt')
small_dir = pydwarf.rel(__file__, 'raw/smallthings')



# A bit of esoteric code which makes smallraws only be read once
def getsmallraws():
    if 'smallraws' not in globals():
        globals()['smallraws'] = raws.dir(root=small_dir, log=pydwarf.log)
    return smallraws



# Help shapes get mapped to words
shapenamedict = {
    'ELF': 'FOREST',
    'DWARF': 'MOUNTAIN',
    'HUMAN': 'PLAIN',
    'MALE': 'MAN',
    'FEMALE': 'WOMAN',
    'OVERSEER': 'STAND',
    'MESSAGE': 'PAPER',
    'BADLAND': 'SAVAGE',
    'PARTY': 'CELEBRATE',
    'WATERFALL': 'WATER',
    'SKIRMISH': 'WAR',
    'HUNTER': 'BOW',
    'RETREAT': 'DEN',
    'STRONGHOLD': 'FORTRESS',
    'SAVANNA': 'PLAIN'
}



@pydwarf.urist(
    name = 'umiman.smallthings.prefstring',
    version = '1.0.0',
    author = ('Umiman', 'Fieari', 'Sophie Kirschner'),
    description = '''This mod simply just adds to the number of prefstrings for
        everything in the game to a minimum of five each. Prefstrings are the stuff
        that tell your dwarves what to like about a creature. For example, "He likes
        large roaches for their ability to disgust". With this mod, you'll see more
        fleshed out descriptions of the things your dwarves like, as well as more
        varied ones. With five each, it's pretty rare to see the same two twice.
        Hopefully I don't have any repeating prefstrings.
    ''',
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def prefstring(df):
    # Get the smallthings ModBase raws, which is where this data will be coming from
    smallraws = getsmallraws()
    if not smallraws: return pydwarf.failure('Failed to read smallthings raws.')
    
    # Get all creatures
    smallcreatures = smallraws.allobj('CREATURE')
    dfcreaturesdict = df.objdict('CREATURE')
    
    # Add the new prefstrings
    failedcreatures = 0
    for smallcreature in smallcreatures:
        dfcreature = dfcreaturesdict.get(smallcreature.args[0])
        if not dfcreature:
            pydwarf.log.debug('Found prefstrings for %s but there was no corresponding creature in the DF raws. Skipping.' % smallcreature)
            failedcreatures += 1
        else:
            prefs = smallcreature.alluntil(exact_value='PREFSTRING', args_count=1, until_exact_value='CREATURE')
            dfcreature.add(tokens=raws.token.copy(prefs))
            pydwarf.log.debug('Added %d prefstrings to %s.' % (len(prefs), dfcreature))
            
    # All done!
    if (len(smallcreatures) - failedcreatures):
        return pydwarf.success('Added prefstrings to %d creatures.' % (len(smallcreatures) - failedcreatures))
    else:
        return pydwarf.failure('Added prefstrings to no creatures.')



@pydwarf.urist(
    name = 'umiman.smallthings.engraving',
    version = '1.0.0',
    author = ('Umiman', 'Fieari', 'Sophie Kirschner'),
    description = '''Has this been done before? While I think it's impossible to change
        any of the inbuilt engraving stuff like, "this is a picture of a dwarf and a
        tentacle demon. The dwarf is embracing the tentacle demon", it is possible to
        edit and add to more basic ones such as "this is a picture of a crescent moon".
        Basically, I added maybe 100 or so new engravings you can potentially see on
        your floors, walls, studded armour, images, and the like. Keep in mind maybe
        one or two metagame just a tad but it's funny! I swear!
    ''',
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def engraving(df):
    if 'descriptor_shape_umiman' in df: return pydwarf.failure('File descriptor_shape_umiman already exists.')
        
    # Get the smallthings ModBase raws, which is where this data will be coming from
    smallraws = getsmallraws()
    if not smallraws: return pydwarf.failure('Failed to read smallthings raws.')
    
    # Get existing words and shapes
    dfwordsdict = df.objdict('WORD')
    dfshapesdict = df.objdict('SHAPE')
    
    # Add a new file for the new shapes
    dfshapesfile = df.add('raw/objects/descriptor_shape_umiman.txt')
    dfshapesfile.add('OBJECT:DESCRIPTOR_SHAPE')
    shapesadded = 0
    
    # Add each shape
    smallshapes = smallraws['descriptor_shape_standard']
    if smallshapes is None: return pydwarf.failure('Failed to find smallthings raws file named descriptor_shape_standard.')
    for smallshape in smallshapes.all(exact_value='SHAPE'):
        if smallshape.args[0] not in dfshapesdict: # Verify that the shape isn't already in the raws
            pydwarf.log.debug('Adding shape %s...' % smallshape)
            
            # Get the tokens describing this shape
            smallshapetokens = smallshape.until(exact_value='SHAPE')
            
            # Shapes in DF's descriptor_shape_standard all have a [WORD:X] token but these do not
            # To compensate, let's do our best to map each shape to a word automatically
            smallshapename = smallshape.get(exact_value='NAME', args_count=2)
            if smallshapename:
                useshapename = smallshapename.args[0].upper()
                if useshapename in shapenamedict: useshapename = shapenamedict[useshapename]
                shapeword = dfwordsdict.get(useshapename)
            else:
                pydwarf.log.error('Found no names for %s.' % shallshape)
                
            # Actually add the new shape to the raws
            dfshapesfile.add(raws.token.copy(smallshape))
            dfshapesfile.add(raws.token.copy(smallshapetokens))
            
            # And also add the word, provided one was found
            if shapeword:
                dfshapesfile.add(raws.token(value='WORD', args=(shapeword.args[0],)))
            else:
                pydwarf.log.info('Found no word for %s, named %s.' % (smallshape, smallshapename))
            
            # And on to the next iteration
            shapesadded += 1
    
    # All done!
    return pydwarf.success('Added %s new shapes.' % shapesadded)

@pydwarf.urist(
    name = 'umiman.smallthings.speech.threats',
    version = '1.0.0',
    author = ('Umiman', 'Sophie Kirschner'),
    description = '''Awhile back I asked the community to contribute to fill out the
        threat.txt which is used in adventurer when someone threatens you. I.E: in vanilla,
        when you face a megabeast or someone who has killed a named creature, they will
        talk about who they killed and then say, "prepare to die!!!". That's all they said.
        Boring. This compilation has some of the best threats (around 150 and counting)
        compiled from that thread and should make killing things too proud of their own
        achievements a lot more fun.
    ''',
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def threats(df):
    df.add(path=threats_path, loc='data/speech', kind=raws.binfile, replace=True)
    return pydwarf.success()
    
@pydwarf.urist(
    name = 'umiman.smallthings.speech.nofamily',
    version = '1.0.0',
    author = ('Umiman', 'Sophie Kirschner'),
    description = '''Adds more dialog options to no_family.txt.''',
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def nofamily(df):
    df.add(path=nofamily_path, loc='data/speech', kind=raws.binfile, replace=True)
    return pydwarf.success()
