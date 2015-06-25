# Helper script for building a json file representing which armoury items are allowed for which entities

import sys
sys.path.append('../../')

import json
import raws

print('And so it begins.')

entities = raws.dir(path='StalsArmouryPackv1_8a_4024')['entity_default']

edict = {}

for entity in entities.all(exact_value='ENTITY'):
    print('Entity: %s' % entity)
    itemtypes = ('AMMO', 'DIGGER', 'TOOL', 'WEAPON', 'ARMOR', 'PANTS', 'GLOVES', 'SHOES', 'HELM', 'SHIELD')
    edict[entity.args[0]] = {}
    entitydict = edict[entity.args[0]]
    for item in entity.alluntil(value_in=itemtypes, until_exact_value='ENTITY'):
        if item.value == 'AMMO':
            if item.value not in entitydict: entitydict[item.value] = {}
            forweapon = item.get(exact_value='WEAPON', reverse=True).args[0]
            if forweapon not in entitydict[item.value]: entitydict[item.value][forweapon] = []
            entitydict[item.value][forweapon].append(item.args[0])
        else:
            if item.value not in entitydict: entitydict[item.value] = []
            entitydict[item.value].append(item.args[0])

print(edict)

with open('armouryentities.json', 'wb') as efile: json.dump(edict, efile)

print('All done!')
