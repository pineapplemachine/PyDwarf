import pydwarf



vegan_reactions = {
    'CLOTH_QUIVER_PKDAWSON': '''
        [NAME:weave cloth quiver]
        [BUILDING:CRAFTSMAN:NONE]
        [REAGENT:mat:1:CLOTH:NONE:NONE:NONE][DOES_NOT_DETERMINE_PRODUCT_AMOUNT]
        [PRODUCT:100:1:QUIVER:NONE:GET_MATERIAL_FROM_REAGENT:mat:NONE]
        [SKILL:CLOTHESMAKING]
    ''',
    'CLOTH_BACKPACK_PKDAWSON': '''
        [NAME:weave cloth backpack]
        [BUILDING:CRAFTSMAN:NONE]
        [REAGENT:mat:1:CLOTH:NONE:NONE:NONE][DOES_NOT_DETERMINE_PRODUCT_AMOUNT]
        [PRODUCT:100:1:BACKPACK:NONE:GET_MATERIAL_FROM_REAGENT:mat:NONE]
        [SKILL:CLOTHESMAKING]
    ''',
}

default_entities = ['MOUNTAIN', 'PLAINS']

default_file = 'raw/objects/reaction_vegan_pkdawson.txt'

default_lua_file = 'hack/scripts/autolabor-vegan-pkdawson.lua'

lua_content = '''
default_labors = {
    %(labors)s
}
for i, labor in ipairs(nonvegan_labors) do
    dfhack.run_command(string.format("autolabor %(format)s 0 0", labor))
end
'''

default_labors = [
    'BUTCHER',
    'TRAPPER',
    'DISSECT_VERMIN',
    'LEATHER',
    'TANNER',
    'MAKE_CHEESE',
    'MILK',
    'FISH',
    'CLEAN_FISH',
    'DISSECT_FISH',
    'HUNT',
    'BONE_CARVE',
    'SHEARER',
    'BEEKEEPING',
    'WAX_WORKING',
    'GELD',
]

def format_lua_content(content, labors):
    return content % {'labors': '\n    '.join('"%s"' % labor for labor in labors), 'format': '%s'}



@pydwarf.urist(
    name = 'pkdawson.vegan',
    version = '1.0.0',
    author = ('Patrick Dawson', 'Sophie Kirschner'),
    description = '''Adds reactions to the craftdwarf's workshop for making quivers and
        backpacks from cloth, which normally require leather. Also adds a DFHack script
        which disables non-vegan labors using autolabor.''',
    arguments = {
        'labors': '''These labors will be disabled using a DFHack script. If set to None
            then no DFHack script will be written. The default labors are %s.
            ''' % ', '.join(default_labors),
        'lua_file': '''The DFHack script will be added to this path, relative to DF's
            root directory. If set to None then no DFHack script will be written.''',
        'auto_run':  '''If set to True, and if the DFHack script is added, then a line
            will be added to the end of dfhack.init which runs this script on startup.
            If set to False then the script will wait to be run manually.'''
        'entities': 'Adds the reaction to these entities. Defaults to MOUNTAIN and PLAINS.',
        'add_to_file': 'Adds the reaction to this file.'
    },
    compatibility = pydwarf.df_0_40
)
def vegan(df, labors=default_labors, lua_file=default_lua_file, auto_run=True, entities=default_entities, add_to_file=default_file):
    # Add the reactions
    addreaction = pydwarf.urist.getfn('pineapple.utils.addreaction')
    for reactionid, reactioncontent in vegan_reactions.iteritems():
        pydwarf.log.debug('Adding reaction %s.' % reactionid)
        response = addreaction(
            df,
            id = reactionid,
            tokens = reactioncontent,
            add_to_file = add_to_file,
            permit_entities = entities
        )
        if not response.success: return response
    
    # Add the dfhack script
    if labors and lua_file:
        pydwarf.log.debug('Adding DFHack script %s.' % lua_file)
        pydwarf.urist.getfn('pineapple.utils.addhack')(
            df,
            name = lua_file,
            content = format_lua_content(lua_content, labors),
            auto_run = auto_run
        )
    
    # All done
    return pydwarf.success()
