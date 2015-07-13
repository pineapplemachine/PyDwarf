import pydwarf
import raws
import json



gemset_dir = pydwarf.rel(__file__, 'gemset')
properties_path = pydwarf.rel(__file__, 'gemsetproperties.json')



@pydwarf.urist(
    name = 'dragondeplatino.gemset.full',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        Performs a full installation, and this is probably what you want to run.
    ''',
    arguments = {
        'variety': '''Which tileset to use. Should be either '24x24' or '48x48'.''',
        'properties': 'todo'
    },
    compatibility = pydwarf.df_0_40
)
def full(df, variety='24x24', properties=properties_path):
    pydwarf.log.info('Running dragondeplatino.gemset.twbt.')
    response = twbt(df, variety)
    if not response: return response
    
    pydwarf.log.info('Running dragondeplatino.gemset.graphics.')
    response = graphics(df, variety)
    if not response: return response
    
    pydwarf.log.info('Running dragondeplatino.gemset.font.')
    response = font(df, variety)
    if not response: return response
    
    pydwarf.log.info('Running dragondeplatino.gemset.art.')
    response = art(df, variety)
    if not response: return response
    
    pydwarf.log.info('Running dragondeplatino.gemset.hack.')
    response = hack(df)
    if not response: return response
    
    pydwarf.log.info('Running dragondeplatino.gemset.objects.')
    response = objects(df, properties)
    if not response: return response
    
    # All done
    return pydwarf.success()



art_files = [
    'mouse.png',
    'shadows.png',
]

override_files = [
    '_overrides_constructed.png',
    '_overrides_feature.png',
    '_overrides_frozen.png',
    '_overrides_items.png',
    '_overrides_lava.png',
    '_overrides_mineral.png',
    '_overrides_plants.png',
    '_overrides_soil_misc.png',
    '_overrides_stone.png',
    '_overrides_tree_cap.png',
]

curses_resolutions = {
    '24x24': '1280x600',
    '48x48': '2560x1200',
}

hack_lines = '''
multilevel 3
multilevel shadowcolor 0.6 0.7 0.8 0.4
multilevel fogcolor 0.6 0.8 1
multilevel fogdensity 0.15 0 1
'''





@pydwarf.urist(
    name = 'dragondeplatino.gemset.art',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        Writes miscelleneous image files to data/art/.
    ''',
    arguments = {
        'variety': '''Which tileset to use. Should be either '24x24' or '48x48'.'''
    },
    compatibility = pydwarf.df_0_40
)
def art(df, variety='24x24'):
    # Copy over image files
    for artfile in art_files:
        df.add(
            path = pydwarf.rel(gemset_dir, 'data/art', variety, artfile),
            loc = 'data/art',
            replace = True,
            kind = raws.reffile
        )
    
    # All done
    return pydwarf.success()
    
    
    
@pydwarf.urist(
    name = 'dragondeplatino.gemset.font',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        Puts the appropriate curses and map files in their appropriate places,
        and modifies settings in data/init/init.txt such that the new
        graphics will be loaded.
    ''',
    arguments = {
        'variety': '''Which tileset to use. Should be either '24x24' or '48x48'.'''
    },
    compatibility = pydwarf.df_0_40
)
def font(df, variety='24x24'):
    # Copy over the font image
    mapfile = 'gemset_map.png'
    df.add(
        path = pydwarf.rel(gemset_dir, 'data/art/', variety, mapfile),
        loc = 'data/art',
        kind = raws.reffile
    )
    
    # Copy over the curses image
    cursesfile = 'gemset_curses_%s.png' % curses_resolutions.get(variety)
    df.add(
        path = pydwarf.rel(gemset_dir, 'data/art/', variety, cursesfile),
        loc = 'data/art',
        kind = raws.reffile
    )
    
    # Adjust init.txt settings accordingly
    init = df['data/init/init.txt'].raw()
    init.set(value='FONT', arg=cursesfile)
    init.set(value='FULLFONT', arg=cursesfile)
    init.set('GRAPHICS:YES')
    init.set(value='GRAPHICS_FONT', arg=mapfile)
    init.set(value='GRAPHICS_FULLFONT', arg=mapfile)
    init.set('PRINT_MODE:TWBT')
    init.set('BLACK_SPACE:YES')
    init.set('TRUETYPE:NO')
    
    # All done
    return pydwarf.success()



@pydwarf.urist(
    name = 'dragondeplatino.gemset.graphics',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        Writes a number of image and raws files to raw/graphics/.
    ''',
    arguments = {
        'variety': '''Which tileset to use. Should be either '24x24' or '48x48'.''',
        'remove_example': 'todo'
    },
    compatibility = pydwarf.df_0_40
)
def graphics(df, variety='24x24', remove_example=True):
    # Remove example file if it still exists
    examplepath = 'raw/graphics/graphics_example.txt'
    if remove_example and examplepath in df: df.remove(examplepath)
            
    # Copy over image and graphics files
    df.add(
        path = pydwarf.rel(gemset_dir, 'raw/graphics', variety),
        loc = 'raw/graphics',
        replace = True
    )
    
    # All done
    return pydwarf.success()
   


@pydwarf.urist(
    name = 'dragondeplatino.gemset.hack',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        Adds multilevel commands to DFHack's raw/onLoad.init.
    ''',
    compatibility = pydwarf.df_0_40
)
def hack(df):
    return pydwarf.urist.getfn('pineapple.utils.addhack')(
        df,
        auto_run = hack_lines
    )



@pydwarf.urist(
    name = 'dragondeplatino.gemset.objects',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        In the raws, sets the tiles and colors for creatures, inorganics, and some
        plants.
    ''',
    arguments = {
        'properties': 'todo'
    },
    compatibility = pydwarf.df_0_40
)
def objects(df, properties=properties_path):
    # Load the json file which tells the script which changes to make
    with open(properties, 'rb') as propertiesfile: props = json.load(propertiesfile)
    data = props['properties']
    growths = props['growths']
    
    # Make changes to the various properties
    for objecttype, objectids in data.iteritems():
        df.allobj(type=objecttype, id_in=objectids).each(
            lambda token: [
                token.set(value=value, args=args) for value, args in objectids[token.arg()].iteritems()
            ]
        )
        
    # Make changes to growths
    df.allobj(type='PLANT', id_in=growths).each(
        lambda token: [
            token.getprop(exact_value='GROWTH', exact_arg=(0, growthname)).get('GROWTH_PRINT').args.reset(growthargs) for growthname, growthargs in growths[token.arg()].iteritems()
        ]
    )

    # All done
    return pydwarf.success()



@pydwarf.urist(
    name = 'dragondeplatino.gemset.overrides',
    version = '1.0.0',
    author = ('DragonDePlatino', 'Sophie Kirschner'),
    description = '''
        Handles TWBT files: An overrides.txt file is placed in data/init/ and the
        pertinent image files are placed in `data/art/`.
    ''',
    arguments = {
        'variety': '''Which tileset to use. Should be either '24x24' or '48x48'.'''
    },
    compatibility = pydwarf.df_0_40
)
def twbt(df, variety='24x24'):
    # Copy over the overrides.txt file
    df.add(
        path = pydwarf.rel(gemset_dir, 'data/init/overrides.txt'),
        loc = 'data/init',
        kind = raws.reffile,
        replace = True
    )
    
    # Copy over the image files
    for overridefile in override_files:
        df.add(
            path = pydwarf.rel(gemset_dir, 'data/art/', variety, overridefile),
            loc = 'data/art',
            kind = raws.reffile,
            replace = True
        )
        
    # All done
    return pydwarf.success()
