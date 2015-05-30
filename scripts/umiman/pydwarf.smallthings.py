import os
import pydwarf
import raws

smalldir = librarydir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smallthingsmod')



# A bit of esoteric code which makes smallraws only be read once
def getsmallraws():
    if 'smallraws' not in globals():
        globals()['smallraws'] = raws.dir(path=smalldir, log=pydwarf.log)
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
    version = 'alpha',
    author = ('Umiman', 'Fieari', 'Sophie Kirschner'),
    description = '''This mod simply just adds to the number of prefstrings for
        everything in the game to a minimum of five each. Prefstrings are the stuff
        that tell your dwarves what to like about a creature. For example, "He likes
        large roaches for their ability to disgust". With this mod, you'll see more
        fleshed out descriptions of the things your dwarves like, as well as more
        varied ones. With five each, it's pretty rare to see the same two twice.
        Hopefully I don't have any repeating prefstrings.
        
        Originally created by Umiman. Ported to ModBase by Fieari. Ported again to
        PyDwarf by Sophie.''',
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def prefstring(dfraws):
    smallraws = getsmallraws()
    if not smallraws: return pydwarf.failure('Failed to read smallthings raws.')
    # Get all creatures
    smallcreatures = smallraws.allobj('CREATURE')
    dfcreaturesdict = dfraws.objdict('CREATURE')
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
    return pydwarf.success('Added prefstrings to %d creatures.' % (len(smallcreatures) - failedcreatures))



@pydwarf.urist(
    name = 'umiman.smallthings.engraving',
    version = 'alpha',
    author = ('Umiman', 'Fieari', 'Sophie Kirschner'),
    description = '''Has this been done before? While I think it's impossible to change
        any of the inbuilt engraving stuff like, "this is a picture of a dwarf and a
        tentacle demon. The dwarf is embracing the tentacle demon", it is possible to
        edit and add to more basic ones such as "this is a picture of a crescent moon".
        Basically, I added maybe 100 or so new engravings you can potentially see on
        your floors, walls, studded armour, images, and the like. Keep in mind maybe
        one or two metagame just a tad but it's funny! I swear!
        
        Originally created by Umiman. Ported to ModBase by Fieari. Ported again to
        PyDwarf by Sophie.''',
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def engraving(dfraws):
    dfwordsdict = dfraws.objdict('WORD')
    dfshapesdict = dfraws.objdict('SHAPE')
    
    dfshapesfile = dfraws.addfile(filename='descriptor_shape_umiman')
    dfshapesfile.add('OBJECT:DESCRIPTOR_SHAPE')
    shapesadded = 0
    
    smallraws = getsmallraws()
    
    for smallshape in smallraws['descriptor_shape_standard'].all(exact_value='SHAPE'):
        if smallshape.args[0] not in dfshapesdict:
            pydwarf.log.debug('Adding shape %s...' % smallshape)
            
            smallshapetokens = smallshape.until(exact_value='SHAPE')
            
            smallshapename = smallshape.get(exact_value='NAME', args_count=2)
            if smallshapename:
                useshapename = smallshapename.args[0].upper()
                if useshapename in shapenamedict: useshapename = shapenamedict[useshapename]
                shapeword = dfwordsdict.get(useshapename)
            else:
                pydwarf.log.error('Found no names for %s.' % shallshape)
                
            dfshapesfile.add(raws.token.copy(smallshape))
            dfshapesfile.add(raws.token.copy(smallshapetokens))
            
            if shapeword:
                dfshapesfile.add(raws.token(value='WORD', args=(shapeword.args[0],)))
            else:
                pydwarf.log.info('Found no word for %s, named %s.' % (smallshape, smallshapename))
            
            shapesadded += 1
                
    return pydwarf.success('Added %s new shapes.' % shapesadded)
