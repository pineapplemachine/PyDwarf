import os
import json
import pydwarf
import raws

# Armoury raws are located in this directory
entities_json = pydwarf.rel(__file__, 'armouryentities.json')
armoury_dir = pydwarf.rel(__file__, 'raw/armoury')

# Armory raws are variations on vanilla names, this records them so they can be changed back.
# Without this, other mods which attempt to make changes to the same items might run into problems.
weird_armoury_names = {
    'ITEM_AMMO_ARROWS_WAR': 'ITEM_AMMO_ARROWS',
    'ITEM_ARMOR_JERKIN': 'ITEM_ARMOR_LEATHER',
    'ITEM_ARMOR_PLATE': 'ITEM_ARMOR_BREASTPLATE',
    'ITEM_SHOES_SANDALS': 'ITEM_SHOES_SANDAL',
    'ITEM_WEAPON_MACE_MORNINGSTAR': 'ITEM_WEAPON_MORNINGSTAR',
    'ITEM_WEAPON_HAMMER_MAUL': 'ITEM_WEAPON_MAUL',
    'ITEM_WEAPON_MACE_FLAIL': 'ITEM_WEAPON_FLAIL',
    'ITEM_WEAPON_PIKE_HALBERD': 'ITEM_WEAPON_HALBERD',
    'ITEM_WEAPON_PIKE_PIKE': 'ITEM_WEAPON_PIKE',
    'ITEM_WEAPON_SWORD_SCIMITAR': 'ITEM_WEAPON_SCIMITAR',
    'ITEM_WEAPON_SWORD_TRAINING': 'ITEM_WEAPON_SWORD_SHORT_TRAINING',
    'ITEM_WEAPON_WHIP_SCOURGE': 'ITEM_WEAPON_SCOURGE'
}

# These are vanilla items without obvious analogs in the armoury raws.
# Mostly just here for my own sake.
missing_armoury_names = [
    'ITEM_ARMOR_MAIL_SHIRT',
    'ITEM_ARMOR_TOGA',
    'ITEM_HELM_HELM',
    'ITEM_HELM_MASK',
    'ITEM_HELM_TURBAN',
    'ITEM_HELM_VEIL_FACE',
    'ITEM_HELM_VEIL_HEAD',
    'ITEM_SHOES_BOOTS_LOW',
    'ITEM_SHOES_CHAUSSE',
    'ITEM_WEAPON_AXE_GREAT',
    'ITEM_WEAPON_DAGGER_LARGE',
    'ITEM_WEAPON_SWORD_LONG',
    'ITEM_WEAPON_SWORD_SHORT'
]

# These are the only item types we care about.
armoury_items = [
    'AMMO',
    'ARMOR',
    'HELM',
    'GLOVES',
    'PANTS',
    'SHIELD',
    'SHOES',
    'TOOL',
    'WEAPON',
]
armoury_item_objects = ['ITEM_%s' % item for item in armoury_items]

# These are the items that each entity should have. (JSON courtesy of helper script armouryentities.py.)
with open(entities_json, 'rb') as efile: armoury_entities = json.load(efile)



@pydwarf.urist(
    name = 'stal.armoury.items',
    version = '1.0.1',
    author = ('Stalhansch', 'Sophie Kirschner'),
    description = 'Attempts to improve the balance and realism of combat.',
    arguments = {
        'remove_entity_items': '''Determines whether items that would be made unavailable to
            entities should be removed from those entities or not. If you're also using other
            mods that make changes to weapons and armour and such it may be desireable to set
            this flag to False. Otherwise, for best results, the flag should be set to True.
            Defaults to True'''
    },
    compatibility = pydwarf.df_revision_range('0.40.14', '0.40.24')
)
def armoury(df, remove_entity_items=True):
    try:
        pydwarf.log.debug('Loading armoury raws from %s.' % armoury_dir)
        armouryraws = raws.dir(root=armoury_dir, log=pydwarf.log)
    except:
        return pydwarf.failure('Unable to load armoury raws.')
        
    # Persist a list of armoury item tokens because we're going to be needing them for a few things
    armouryitemtokens = armouryraws.allobj(type_in=armoury_item_objects)
    
    # Rename items in the armoury raws in accordance with a manually compiled list of naming oddities
    for item in armouryitemtokens.all(arg_in=(0, weird_armoury_names)):
        item.args[0] = weird_armoury_names[item.args[0]]
        
    # Remove any existing items in the raws which share an id with the items about to be added
    pydwarf.log.debug('Removing obsolete items.')
    df.removeallobj(type_in=armoury_item_objects, id_in=[token.arg() for token in armouryitemtokens])
    
    # Look for files made empty as a result (of which there should be a few) and remove them
    removedfiles = []
    for file in df.files.values():
        if isinstance(file, raws.rawfile) and len(file) <= 1:
            pydwarf.log.debug('Removing emptied file %s.' % file)
            file.remove()
            removedfiles.append(file)
    
    # Get a list of entity tokens corresponding to the relevant names
    entitytokens = [df.getobj('ENTITY', entity) for entity in armoury_entities]
    
    # If remove_entity_items is set to True, remove all existing tokens which permit relevant items
    # Otherwise, just remove the ones with conflict with those about to be added
    for entitytoken in entitytokens:
        pydwarf.log.debug('Removing permission tokens from %s.' % entitytoken)
        entitytoken.removeallprop(
            value_in = armoury_items,
            arg_in = (
                None if remove_entity_items else (0, [token.args[0] for token in armouryitemtokens])
            )
        )
    
    # Now add all the armoury raw files that have items in them
    try:
        for file in armouryraws.iterfiles():
            if file.kind == 'raw' and file.name.startswith('item_'):
                pydwarf.log.debug('Adding file %s to raws.' % file)
                copy = file.copy()
                copy.loc = 'raw/objects'
                copy.name += '_armoury_stal'
                df.add(copy)
    except:
        pydwarf.log.exception('Encountered exception.')
        return pydwarf.failure('Failed to add armoury item raws.')
        
    # Add new permitted item tokens
    try:
        for entitytoken in entitytokens:
            pydwarf.log.debug('Permitting items for %s.' % entitytoken)
            for itemtype, items in armoury_entities[entitytoken.arg()].iteritems():
                for item in items:
                    entitytoken.add(
                        raws.token(
                            value = itemtype,
                            args = [weird_armoury_names.get(item[0], item[0])] + item[1:]
                        )
                    )
    except:
        pydwarf.log.exception('Encountered exception.')
        return pydwarf.failure('Failed to permit items for entities.')
            
    # And add the new reactions
    try:
        pydwarf.log.debug('Adding new reactions.')
        reactions = armouryraws['reaction_armoury'].copy()
        reactions.loc = 'raw/objects'
        reactions.name = 'reaction_armoury_stal'
        response = pydwarf.urist.getfn('pineapple.easypatch')(
            df,
            reactions,
            permit_entities = armoury_entities.keys()
        )
        if not response: return response
    except:
        pydwarf.log.exception('Encountered exception.')
        return pydwarf.failure('Failed to add new reactions.')
    
    # All done!
    return pydwarf.success()
        


@pydwarf.urist(
    name = 'stal.armoury.attacks',
    version = '1.0.0',
    author = ('Stalhansch', 'Sophie Kirschner'),
    description = '''Removes attacks from creatures. By default, as a way to improve balance in
        combat, scratch and bite attacks are removed from dwarves, humans, and elves.''',
    arguments = {
        'remove_attacks': '''Removes these attacks from species listed in remove_attacks_from.
            Defaults to scratch and bite.''',
        'remove_attacks_from': '''If set to True, specified remove_attacks are removed
            from the species in the list to improve combat balancing. If set to None those
            attacks will not be touched. Defaults to dwarves, humans, and elves.'''
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x)
)
def removeattacks(df, remove_attacks=('SCRATCH', 'BITE'), remove_attacks_from=('DWARF', 'HUMAN', 'ELF')):
    removed = 0
    for creature in df.allobj(type='CREATURE', id_in=remove_attacks_from):
        for attack in creature.allprop(exact_value='ATTACK', arg_in=((0, remove_attacks),)):
            pydwarf.log.debug('Removing attack %s from creature %s.' % (attack, creature))
            for token in attack.all(until_re_value='(?!ATTACK_).+'): token.remove()
            attack.remove()
            removed += 1
    if removed:
        return pydwarf.success('Removed %d attacks from %d creatures.' % (removed, len(remove_attacks_from)))
    else:
        return pydwarf.failure('Removed no attacks from creatures.')
