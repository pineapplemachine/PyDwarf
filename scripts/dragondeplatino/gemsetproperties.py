'''
This script looks for changes to creature tiles and colors and similar information
in files in gemset's raw/objects, then writes a more easily parseable file out
for the PyDwarf gemset script to use.
'''

import sys
import os

sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../..'))

import json
from pprint import pprint

import raws

gems = raws.dir('gemset/raw/objects')
outputpath = 'gemsetproperties.json'

# These are the propeties we care about for each object type
tileproperties = {
    'CREATURE': (
        'CREATURE_TILE',
        'ALTTILE',
    ),
    'INORGANIC': (
        'DISPLAY_COLOR',
        'TILE',
    ),
    'PLANT': (
        'PICKED_TILE',
        'PICKED_COLOR',
        'DEAD_PICKED_TILE',
        'DEAD_PICKED_COLOR',
        'SHRUB_TILE',
        'SHRUB_COLOR',
        'DEAD_SHRUB_TILE',
        'DEAD_SHRUB_COLOR',
        'TREE_TILE',
        'TREE_COLOR',
        'DEAD_TREE_TILE',
        'DEAD_TREE_COLOR',
        'SAPLING_TILE',
        'SAPLING_COLOR',
        'DEAD_SAPLING_TILE',
        'DEAD_SAPLING_COLOR',
        'GRASS_TILES',
        'GRASS_COLORS',
    ),
}

# Get those properties for each object and do some special handling to get GROWTH_PRINT tokens as well
data = {}
growths = {}
for objecttype, properties in tileproperties.iteritems():
    data[objecttype] = {}
    for objecttoken in gems.allobj(objecttype):
        data[objecttype][objecttoken.arg()] = {
            prop.value: prop.args for prop in objecttoken.allprop(value_in=properties)
        }
        if objecttype == 'PLANT':
            growths[objecttoken.arg()] = {
                growth.arg(): growth.get('GROWTH_PRINT').args for growth in objecttoken.allprop('GROWTH')
            }

# All done, output it to a file
jsonout = {
    'properties': data,
    'growths': growths
}
with open(outputpath, 'wb') as jsonfile:
    json.dump(jsonout, jsonfile, indent=4)
