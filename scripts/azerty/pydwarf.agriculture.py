import pydwarf
import raws



rawsdir = pydwarf.rel(__file__, 'raw/agriculture')

default_entities = '*'



# Helper function for adding files from the raw/agriculture directory
def addfile(df, filename):
    with open('%s/%s' % (rawsdir, filename), 'rb') as rawfile:
        df.add(raws.rawfile(
            path='raw/objects/%s' % filename,
            file=rawfile
        ))
    return pydwarf.success('Added file "%s".' % filename)



@pydwarf.urist(
    name = 'azerty.agriculture.castorbean',
    title = 'Castorbean',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds the castorbean or castor-oil-plant, a flowering
        plant from which castor oil may be extracted.'''
)
def castorbean(df):
    return addfile(df, 'plant_castorbean_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.madder',
    title = 'Madder',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds common madder or dyer's madder, a plant of the Rubia
        genus, whose roots are a source of red dye.'''
)
def madder(df):
    return addfile(df, 'plant_madder_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.opiumpoppy',
    title = 'Opium Poppy',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds the opium poppy, which yields poppy seeds that can
        be processed to produce poppyseed oil.'''
)
def opiumpoppy(df):
    return addfile(df, 'plant_opium_poppy_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.rapeseed',
    title = 'Rapeseed',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds rapeseed, a yellow flowering plant, from which
        rapeseed oil may be extracted.'''
)
def rapeseed(df):
    return addfile(df, 'plant_rapeseed_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.sesame',
    title = 'Sesame',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds sesame, a plant whose seeds from which sesame oil
        may be produced.'''
)
def sesame(df):
    return addfile(df, 'plant_sesame_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.sugarcane',
    title = 'Sugarcane',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds sugarcane, a tall grass from which sugar may be
        extracted and rum brewed.'''
)
def sugarcane(df):
    return addfile(df, 'plant_sugarcane_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.whitemustard',
    title = 'White Mustard',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds white mustard, a plant producing mustard seeds that
        oil may be extracted from.'''
)
def whitemustard(df):
    return addfile(df, 'plant_white_mustard_azerty.txt')



@pydwarf.urist(
    name = 'azerty.agriculture.okra',
    title = 'Okra',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds okra, known also as ladies' fingers or gumbo, a plant
        from which okra oil may be extracted.'''
)
def okra(df):
    return addfile(df, 'plant_okra_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.sunflower',
    title = 'Sunflower',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds sunflowers, a plant that may be used to produce
        sunflower oil.'''
)
def sunflower(df):
    return addfile(df, 'plant_sunflower_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.yellowsafflower',
    title = 'Yellow Safflower',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds yellow safflower, a plant which yields both safflower
        oil and yellow safflower dye.'''
)
def yellowsafflower(df):
    return addfile(df, 'plant_yellow_safflower_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.redsafflower',
    title = 'Red Safflower',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds yellow safflower, a plant which yields both safflower
        oil and red safflower dye.'''
)
def redsafflower(df):
    return addfile(df, 'plant_red_safflower_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.weld',
    title = 'Dyer\'s Rocket',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds weld, known also as dyer's rocket, a plant from which
        yellow dye may be extracted.'''
)
def weld(df):
    return addfile(df, 'plant_weld_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.woad',
    title = 'Dyer\'s Woad',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds woad or glastum, a flowering plant from whose leaves
        blue dye may be produced.'''
)
def woad(df):
    return addfile(df, 'plant_woad_azerty.txt')



@pydwarf.urist(
    name = 'azerty.agriculture.oilpalm',
    title = 'Oil Palm',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds oil palm or elaeis, a tree from which palm oil may
        be extracted.'''
)
def oilpalm(df):
    return addfile(df, 'plant_oil_palm_azerty.txt')

@pydwarf.urist(
    name = 'azerty.agriculture.brazilwood',
    title = 'Brazilwood',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds brazilwood, known also as the pernambuco tree, which
        yields a red dye known as brazilin.'''
)
def brazilwood(df):
    return addfile(df, 'plant_brazilwood_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.hennatree',
    title = 'Henna',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds henna, a tree which yields a red-brown dye used
        commonly in body art.'''
)
def hennatree(df):
    return addfile(df, 'plant_henna_tree_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.indigotree',
    title = 'Indigo Tree',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds the indigo tree, or true indigo, a plant whose leaves
        may be processed to obtain indigo dye.'''
)
def indigotree(df):
    return addfile(df, 'plant_indigo_tree_azerty.txt')
    
@pydwarf.urist(
    name = 'azerty.agriculture.juniper',
    title = 'Common Juniper',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds the common juniper, a coniferous tree from which brown
        dye may be extracted and from whose berries gin may be brewed.'''
)
def juniper(df):
    return addfile(df, 'plant_common_juniper_azerty.txt')



@pydwarf.urist(
    name = 'azerty.agriculture.catechudye',
    title = 'Catechu Dye from Acacias',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies the acacia to yield brown catechu dye.'''
)
def catechudye(df):
    acacia = df.getobj('PLANT:ACACIA')
    acacia.addafter('''
        [USE_MATERIAL_TEMPLATE:MILL:PLANT_POWDER_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:catechu dye]
            [STATE_COLOR:ALL_SOLID:BROWN]
            [DISPLAY_COLOR:4:0:1]
            [MATERIAL_VALUE:20]
            [POWDER_DYE:RED]
            [PREFIX:NONE]
        [MILL:LOCAL_PLANT_MAT:MILL]
    ''')
    acacia.getprop('USE_MATERIAL_TEMPLATE:WOOD:WOOD_TEMPLATE').addafter('''
        [MATERIAL_REACTION_PRODUCT:MILL_PLANT_PART_POWDER:LOCAL_PLANT_MAT:POWDER]
        [STOCKPILE_PLANT_GROWTH]
    ''')
    return pydwarf.success('Added catechu dye product to acacia tree.')



@pydwarf.urist(
    name = 'azerty.agriculture.copraoil',
    title = 'Copra Oil from Coconuts',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies coconut palms' coconuts to yield copra oil.''',
)
def copraoil(df):
    palm = df.getobj('PLANT:PALM')
    palm.addafter('''
        [USE_MATERIAL_TEMPLATE:OIL:PLANT_OIL_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:frozen copra oil]
            [STATE_NAME_ADJ:LIQUID:copra oil]
            [STATE_NAME_ADJ:GAS:boiling copra oil]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
            [EDIBLE_COOKED]
        [USE_MATERIAL_TEMPLATE:SOAP:PLANT_SOAP_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:copra oil soap]
            [STATE_NAME_ADJ:LIQUID:melted copra oil soap]
            [STATE_NAME_ADJ:GAS:n/a]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
    ''')
    palm.getprop('USE_MATERIAL_TEMPLATE:NUT:FRUIT_TEMPLATE').addafter('''
        [MATERIAL_REACTION_PRODUCT:PRESS_LIQUID_MAT:LOCAL_PLANT_MAT:OIL]
        [STOCKPILE_GLOB_PRESSED]
    ''')
    return pydwarf.success('Added copra oil product to coconut palms.')



@pydwarf.urist(
    name = 'azerty.agriculture.sugarbeets',
    title = 'Sugar and Syrup from Beets',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies beets to yield sugar.''',
)
def sugarbeets(df):
    beet = df.getobj('PLANT:BEET')
    beet.addafter('''
        [USE_MATERIAL_TEMPLATE:MILL:PLANT_POWDER_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:sugar]
            [STATE_COLOR:ALL_SOLID:WHITE]
            [DISPLAY_COLOR:6:0:0]
            [MATERIAL_VALUE:20]
            [EDIBLE_VERMIN]
            [EDIBLE_RAW]
            [EDIBLE_COOKED]
        [MILL:LOCAL_PLANT_MAT:MILL]
        [USE_MATERIAL_TEMPLATE:EXTRACT:PLANT_EXTRACT_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:frozen beet syrup]
            [STATE_NAME_ADJ:LIQUID:beet syrup]
            [STATE_NAME_ADJ:GAS:boiling beet syrup]
            [MATERIAL_VALUE:20]
            [DISPLAY_COLOR:6:0:0]
            [EDIBLE_RAW]
            [EDIBLE_COOKED]
            [EXTRACT_STORAGE:BARREL]
            [PREFIX:NONE]
        [EXTRACT_BARREL:LOCAL_PLANT_MAT:EXTRACT]
    ''')
    return pydwarf.success('Added sugar and syrup products to beet plants.')



@pydwarf.urist(
    name = 'azerty.agriculture.peanutoil',
    title = 'Peanut Oil',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies peanuts such that peanut oil may be extracted
        from them.''',
)
def peanutoil(df):
    peanut = df.getobj('PLANT:PEANUT')
    peanut.addafter('''
        [USE_MATERIAL_TEMPLATE:OIL:PLANT_OIL_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:frozen peanut oil]
            [STATE_NAME_ADJ:LIQUID:peanut oil]
            [STATE_NAME_ADJ:GAS:boiling peanut oil]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
            [EDIBLE_COOKED]
        [USE_MATERIAL_TEMPLATE:SOAP:PLANT_SOAP_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:peanut oil soap]
            [STATE_NAME_ADJ:LIQUID:melted peanut oil soap]
            [STATE_NAME_ADJ:GAS:n/a]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
    ''')
    peanut.getprop('USE_MATERIAL_TEMPLATE:SEED:SEED_TEMPLATE').addafter('''
        [MATERIAL_REACTION_PRODUCT:PRESS_LIQUID_MAT:LOCAL_PLANT_MAT:OIL]
        [PREFIX:NONE]
        [STOCKPILE_GLOB_PASTE]
        [STOCKPILE_GLOB_PRESSED]
    ''')
    return pydwarf.success('Added oil product to peanut plants.')



@pydwarf.urist(
    name = 'azerty.agriculture.soybeanoil',
    title = 'Peanut Oil',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies soybeans to yield soybean oil.''',
)
def soybeanoil(df):
    soy = df.getobj('PLANT:SOYBEAN')
    soy.addafter('''
        [USE_MATERIAL_TEMPLATE:OIL:PLANT_OIL_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:frozen soybean oil]
            [STATE_NAME_ADJ:LIQUID:soybean oil]
            [STATE_NAME_ADJ:GAS:boiling soybean oil]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
            [EDIBLE_COOKED]
        [USE_MATERIAL_TEMPLATE:SOAP:PLANT_SOAP_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:soybean oil soap]
            [STATE_NAME_ADJ:LIQUID:melted soybean oil soap]
            [STATE_NAME_ADJ:GAS:n/a]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
    ''')
    # TODO: What's with the "seasame seed" state name adjectives here?
    soy.getprop('USE_MATERIAL_TEMPLATE:SEED:SEED_TEMPLATE').addafter('''
        [STATE_NAME_ADJ:ALL_SOLID:soybean seed]
        [STATE_NAME_ADJ:SOLID_PASTE:soybean seed paste]
        [STATE_NAME_ADJ:SOLID_PRESSED:soybean seed press cake]
        [MATERIAL_REACTION_PRODUCT:PRESS_LIQUID_MAT:LOCAL_PLANT_MAT:OIL]
        [STOCKPILE_GLOB_PASTE]
        [STOCKPILE_GLOB_PRESSED]
    ''')
    return pydwarf.success('Added oil product to soybean plants.')



@pydwarf.urist(
    name = 'azerty.agriculture.macadamiaoil',
    title = 'Macadamia Oil',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies macadamias' nuts to yield macadamia oil.''',
)
def macadamiaoil(df):
    peanut = df.getobj('PLANT:MACADAMIA')
    peanut.addafter('''
        [USE_MATERIAL_TEMPLATE:OIL:PLANT_OIL_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:frozen macadamia oil]
            [STATE_NAME_ADJ:LIQUID:macadamia oil]
            [STATE_NAME_ADJ:GAS:boiling macadamia oil]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
            [EDIBLE_COOKED]
        [USE_MATERIAL_TEMPLATE:SOAP:PLANT_SOAP_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:macadamia oil soap]
            [STATE_NAME_ADJ:LIQUID:melted macadamia oil soap]
            [STATE_NAME_ADJ:GAS:n/a]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
    ''')
    peanut.getprop('USE_MATERIAL_TEMPLATE:SEED:SEED_TEMPLATE').addafter('''
        [MATERIAL_REACTION_PRODUCT:PRESS_LIQUID_MAT:LOCAL_PLANT_MAT:OIL]
        [STOCKPILE_GLOB_PRESSED]
    ''')
    return pydwarf.success('Added oil product to macadamia trees.')



@pydwarf.urist(
    name = 'azerty.agriculture.walnutoil',
    title = 'Walnut Oil',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Modifies walnuts to yield walnut oil.''',
)
def macadamiaoil(df):
    peanut = df.getobj('PLANT:WALNUT')
    peanut.addafter('''
        [USE_MATERIAL_TEMPLATE:OIL:PLANT_OIL_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:frozen walnut oil]
            [STATE_NAME_ADJ:LIQUID:walnut oil]
            [STATE_NAME_ADJ:GAS:boiling walnut oil]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
            [EDIBLE_COOKED]
        [USE_MATERIAL_TEMPLATE:SOAP:PLANT_SOAP_TEMPLATE]
            [STATE_NAME_ADJ:ALL_SOLID:walnut oil soap]
            [STATE_NAME_ADJ:LIQUID:melted walnut oil soap]
            [STATE_NAME_ADJ:GAS:n/a]
            [PREFIX:NONE]
            [MATERIAL_VALUE:5]
    ''')
    peanut.getprop('USE_MATERIAL_TEMPLATE:SEED:SEED_TEMPLATE').addafter('''
        [MATERIAL_REACTION_PRODUCT:PRESS_LIQUID_MAT:LOCAL_PLANT_MAT:OIL]
        [STOCKPILE_GLOB_PASTE]
        [STOCKPILE_GLOB_PRESSED]
    ''')
    return pydwarf.success('Added oil product to walnut trees.')



@pydwarf.urist(
    name = 'azerty.agriculture.plantpowder',
    title = 'Mill Powder from Wood and Plants',
    version = '1.0.0',
    author = 'Azerty',
    description = '''Adds reactions to mill powder from logs and from plants.
        These reactions may be used, for example, to extract dye or oil from
        plants added or modified by other azerty.agriculture scripts.''',
    arguments = {
        'entities': '''The entities which should be permitted this reaction.
            Defaults to all entities.'''
    },
)
def plantpowder(df, entities=default_entities):
    return pydwarf.urist.getfn('pineapple.easypatch')(
        df,
        files = [rawsdir + '/plant_reaction_other_azerty.txt'],
        loc = 'raw/objects',
        permit_entities = entities
    )
