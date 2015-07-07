import pydwarf
import raws



default_grasses = {
    'FLOOR FUNGI': {
        # Arguments for GRASS_COLORS token
        'colors': raws.color.yellow() + raws.color.brown() + raws.color.lgray() + raws.color.dgray(),
        # Arguments for UNDERGROUND_DEPTH
        'depth': (1, 1)
    },
    'PALE FERN PINEAPPLE': {
        # Defining a new grass, so it will need a few more things than the previous ones
        # Copy tokens from this plant (exluding ALL_NAMES, NAME, NAME_PLURAL, and ADJ)
        'template': 'CAVE MOSS',
        # Add these tokens
        'add_tokens': '[NAME:pale fern][NAME_PLURAL:pale ferns][ADJ:pale fern]',
        # And these are the same as above
        'colors': raws.color.lgreen() + raws.color.lgray() + raws.color.brown() + raws.color.dgray(),
        'depth': (1, 1)
    },
    'THORN GRASS PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:thorn grass]',
        'remove_tokens': '[WET]', # Removes these tokens after applying the template
        'colors': raws.color.lgreen() + raws.color.green() + raws.color.lgray() + raws.color.dgray(),
        'depth': (1, 1)
    },
    'ANGEL WEED PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:angel weed]',
        'colors': raws.color.brown() + raws.color.yellow() + raws.color.lgray() + raws.color.dgray(),
        'depth': (1, 1)
    },
    
    'CAVE MOSS': {
        'colors': raws.color.lgreen() + raws.color.green() + raws.color.lgray() + raws.color.dgray(),
        'depth': (1, 2)
    },
    'GLOWMOSS PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:glowmoss]',
        'colors': raws.color.cyan() + raws.color.lcyan() + raws.color.blue() + raws.color.dgray(),
        'depth': (1, 2)
    },
    
    'BLUE CREEPER PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:blue creeper]',
        'remove_tokens': '[DRY]',
        'colors': raws.color.blue() + raws.color.lblue() + raws.color.lgray() + raws.color.dgray(),
        'depth': (2, 2)
    },
    'SILVERBLADE PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[NAME:silverblade][NAME_PLURAL:silverblades][ADJ:silverblade]',
        'colors': raws.color.lcyan() + raws.color.lgray() + raws.color.cyan() + raws.color.dgray(),
        'depth': (2, 2)
    },
    
    'ROYAL MOLD PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:royal mold]',
        'colors': raws.color.lmagenta() + raws.color.magenta() + raws.color.dgray() + raws.color.dgray(),
        'depth': (2, 3)
    },
    'IRONWEED PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:ironweed]',
        'colors': raws.color.lgray() + raws.color.dgray() + raws.color.dgray() + raws.color.dgray(),
        'depth': (2, 3)
    },
    
    'SCORCHED FUNGI PINEAPPLE': {
        'template': 'FLOOR FUNGI',
        'add_tokens': '[NAME:scorched fungus][NAME_PLURAL:scorched fungi][ADJ:scorched fungus]',
        'remove_tokens': '[WET]',
        'colors': raws.color.white() + raws.color.lgray() + raws.color.dgray() + raws.color.dgray(),
        'depth': (3, 3)
    },
    'BLOOD TENDRIL PINEAPPLE': {
        'template': 'FLOOR FUNGI',
        'add_tokens': '[NAME:blood tendril][NAME_PLURAL:blood tendrils][ADJ:blood tendril]',
        'colors': raws.color.red() + raws.color.lred() + raws.color.lgray() + raws.color.dgray(),
        'depth': (3, 3)
    },
    'GOREWEED PINEAPPLE': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:goreweed]',
        'colors': raws.color.lred() + raws.color.brown() + raws.color.dgray() + raws.color.dgray(),
        'depth': (3, 3)
    },
    'GHOST MOSS': {
        'template': 'CAVE MOSS',
        'add_tokens': '[ALL_NAMES:ghost moss]',
        'colors': raws.color.lred() + raws.color.magenta() + raws.color.lgray() + raws.color.dgray(),
        'depth': (3, 3)
    }
}



@pydwarf.urist(
    name = 'pineapple.cavegrass',
    version = '1.0.2',
    author = 'Sophie Kirschner',
    description = '''Changes the grasses in each cavern level to make the different
        levels more visually distinct, as well as adding a much greater variety.
        With default arguments the first cavern will be primarly green and yellow,
        the second blue and cyan, the third red and gray.
        Inspired by/stolen from Rubble's Cave Color mod.''',
    arguments = {
        'grasses': '''A dictionary specifying which grasses to change and modify.
            See the default_grasses dict for documentation.'''
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def cavegrass(df, grasses=default_grasses, add_file='plant_grasses_cavegrass_pineapple'):
    # Add the new file for new grasses
    grassfile = None
    if add_file:
        try:
            grassfile = df.add(add_file)
            grassfile.add('OBJECT:PLANT')
        except:
            pydwarf.log.exception('Failed to add file %s.' % add_file)
            return pydwarf.failure('Failed to add file %s.' % add_file)
    
    # Handle each grass
    failures = 0
    added = 0
    changed = 0
    grasstokens = df.objdict(type='PLANT')
    for grassname, grassdict in grasses.iteritems():
        pydwarf.log.debug('Handling grass %s.' % grassname)
        grasstoken = grasstokens.get(grassname)
        
        # Some extra handling for new grasses
        if not grasstoken:
            pydwarf.log.debug('Grass %s isn\'t defined yet, adding.' % grassname)
            grasstoken = grassfile.add(raws.token(value='PLANT', args=[grassname], prefix='\n\n'))
            if 'template' in grassdict:
                templatetoken = grasstokens.get(grassdict['template'])
                if not templatetoken:
                    pydwarf.log.error('Couldn\'t find template %s to apply to grass %s.' % (grassdict['template'], grassname))
                    failures += 1
                else:
                    props = templatetoken.allprop(value_not_in=('ALL_NAMES', 'NAME', 'NAME_PLURAL', 'ADJ'))
                    grasstoken.add(raws.token.copy(props))
            added += 1
        else:
            changed += 1
        
        # Handling for both new and existing grasses
        if 'add_tokens' in grassdict:
            grasstoken.add(grassdict['add_tokens'])
        if 'remove_tokens' in grassdict:
            tokens = raws.token.parse(grassdict['remove_tokens'])
            for token in tokens:
                removetoken = grasstoken.getprop(match_token=token)
                if removetoken:
                    removetoken.remove()
                else:
                    pydwarf.log.error('Attempted to remove token %s from %s but the token wasn\'t present.' % (removetoken, grassname))
        if 'colors' in grassdict:
            grasscolors = grasstoken.getprop('GRASS_COLORS')
            if grasscolors:
                grasscolors.args = list(grassdict['colors'])
            else:
                grasstoken.add(raws.token(value='GRASS_COLORS', args=list(grassdict['colors'])))
        if 'depth' in grassdict:
            grassdepth = grasstoken.getprop('UNDERGROUND_DEPTH')
            if grassdepth:
                grassdepth.args = list(grassdict['depth'])
            else:
                grasstoken.add(raws.token(value='UNDERGROUND_DEPTH', args=list(grassdict['depth'])))
                
    # All done!
    if failures == 0:
        return pydwarf.success('Changed %d grasses and added %d new ones.' % (changed, added))
    else:
        return pydwarf.failure()

def edittoken(token, rates):
    # Convenience method: Set a skill token's last three arguments to NONE:NONE:NONE. (This kills the rust.)
    if existingtoken.args[-4:-1] == rates:
        return False
    else:
        for i in xrange(1, 4): existingtoken.args[-i] = rates[i-1]
        return True
