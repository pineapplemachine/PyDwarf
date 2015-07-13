def getoption(version, *options):
    '''Internal: Used by objects functions to get an option corresponding to some Dwarf Fortress version.'''
    if version:
        if isinstance(version, basestring): # For strings
            pass
        elif 'config' in version.__dict__ and 'version' in version.config.__dict__: # For dirs
            version = version.config.version
        elif 'version' in version.__dict__: # For configs
            version = version.version
        else:
            version = str(version)
        if version and version.startswith('0.2'):
            return options[1]
    return options[0]
    
def objectsdict(headersdict):
    '''Internal: Used to build a dict mapping objects to their headers from a dict mapping headers to their possible objects.'''
    objdict = {}
    for header, objects in headersdict.iteritems():
        for obj in objects: objdict[obj] = header
    return objdict



headers_base = {
    'BODY': [
        'BODY',
    ],
    'CREATURE': [
        'CREATURE',
    ],
    'ENTITY': [
        'ENTITY',
    ],
    'GRAPHICS': [
        'TILE_PAGE', 'CREATURE_GRAPHICS',
    ],
    'ITEM': [
        'ITEM_WEAPON', 'ITEM_TOY', 'ITEM_TOOL', 'ITEM_INSTRUMENT',
        'ITEM_TRAPCOMP', 'ITEM_ARMOR', 'ITEM_AMMO', 'ITEM_SIEGEAMMO',
        'ITEM_GLOVES', 'ITEM_SHOES', 'ITEM_SHIELD', 'ITEM_HELM',
        'ITEM_PANTS', 'ITEM_FOOD',
    ],
    'LANGUAGE': [
        'WORD', 'SYMBOL', 'TRANSLATION',
    ],
    'REACTION': [
        'REACTION',
    ],
    'TISSUE_TEMPLATE': [
        'TISSUE_TEMPLATE',
    ],
}

headers_23 = {
    'DESCRIPTOR': [
        'COLOR', 'SHAPE'
    ],
    'MATGLOSS': [
        'MATGLOSS_GEM', 'MATGLOSS_PLANT', 'MATGLOSS_STONE', 'MATGLOSS_WOOD'
    ],
}
headers_23.update(headers_base)

headers_31 = {
    'BODY_DETAIL_PLAN': [
        'BODY_DETAIL_PLAN'
    ],
    'BUILDING': [
        'BUILDING_WORKSHOP', 'BUILDING_FURNACE'
    ],
    'CREATURE_VARIATION': [
        'CREATURE_VARIATION'
    ],
    'DESCRIPTOR_COLOR': [
        'COLOR'
    ],
    'DESCRIPTOR_PATTERN': [
        'COLOR_PATTERN'
    ],
    'DESCRIPTOR_SHAPE': [
        'SHAPE'
    ],
    'INORGANIC': [
        'INORGANIC'
    ],
    'INTERACTION': [
        'INTERACTION'
    ],
    'MATERIAL_TEMPLATE': [
        'MATERIAL_TEMPLATE'
    ],
    'PLANT': [
        'PLANT'
    ],
}
headers_31.update(headers_base)

objects_23 = objectsdict(headers_23)
objects_31 = objectsdict(headers_31)



def headers(version=None):
    '''Get a list of valid object types as given by the OBJECT:TYPE tokens which appear
    at the beginning of raws files.'''
    return getoption(version, headers_31, headers_23).keys()
def objects(version=None):
    '''Get a list of valid object types as given by the TYPE:ID tokens which denote the
    beginning of an object definition.'''
    return getoption(version, objects_31, objects_23).keys()
    
def headerdict(version=None):
    '''Get the header dict corresponding to some version. The dict maps headers as keys
    to lists of corresponding object types. For example, BUILDING to BUILDING_WORKSHOP
    and BUILDING_FURNACE.'''
    return getoption(version, headers_31, headers_23)
def objectdict(version=None):
    '''Get the object dict corresponding to some version. The dict maps object types as
    keys to their corresponding header. For example, BUILDING_WORKSHOP to BUILDING.'''
    return getoption(version, objects_31, objects_23)
    
def headerforobject(type, version=None):
    '''Returns the header for a particular object type given a version.'''
    return objectdict(version)[type]
def objectsforheader(header, version=None):
    '''Returns the object types corresponding to a particular header given a version.'''
    return headerdict(version)[header]
