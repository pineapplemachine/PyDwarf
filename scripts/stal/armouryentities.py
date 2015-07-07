# Helper script for building a json file representing which armoury items are allowed for which entities

import sys
sys.path.append('../../')

import json
import raws

print('And so it begins.')

armouryraws = raws.dir(root='raw/armoury')

itemtypes = ('AMMO', 'DIGGER', 'TOOL', 'WEAPON', 'ARMOR', 'PANTS', 'GLOVES', 'SHOES', 'HELM', 'SHIELD')

edict = {}

for entity in armouryraws.allobj('ENTITY'):
    print('Entity: %s' % entity)
    edict[entity.args[0]] = {}
    entitydict = edict[entity.args[0]]
    for item in entity.allprop(value_in=itemtypes):
        if item.value not in entitydict: entitydict[item.value] = []
        entitydict[item.value].append(item.args)

print(edict)

with open('armouryentities.json', 'wb') as efile: json.dump(edict, efile, indent=4)

print('All done!')
