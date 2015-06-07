import os
import json
import pydwarf
import raws

# Armoury raws are located in this directory
armourydir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'StalsArmouryPackv1_8a_4024')

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
    'ITEM_AMMO',
    'ITEM_ARMOR',
    'ITEM_HELM',
    'ITEM_GLOVES'
    'ITEM_PANTS',
    'ITEM_SHIELD',
    'ITEM_SHOES',
    'ITEM_TOOL',
    'ITEM_WEAPON',
]

# These are the items that each entity should have. (JSON courtesy of helper script armouryentities.py.)
with open(os.path.join(armourydir, '../armouryentities.json'), 'rb') as efile: armoury_entities = json.load(efile)



def additemstoraws(dfraws, armouryraws):
    pydwarf.log.debug('Building dict to index relevant items in df raws...')
    dfitems = {str(token): token for token in dfraws.all(value_in=armoury_items)}
    pydwarf.log.debug('Dict dfitems contains %d tokens.' % len(dfitems))
    
    # Add new items to raws and edit already-present ones
    for filename in armouryraws.files.keys():
        if filename.startswith('item_'):
            for armouryitem in armouryraws[filename].all(value_in=armoury_items, args_count=1):
                pydwarf.log.debug('Handling armoury item %s...' % armouryitem)
                
                # Account for names that were changed from the normal DF raws
                if armouryitem.args[0] in weird_armoury_names: armouryitem.args[0] = weird_armoury_names[armouryitem.args[0]]
                
                # Get the tokens belonging to this item
                armourytokens = armouryitem.alluntil(until_exact_value=armouryitem.value)
                # Get the current item with the same ID (if present)
                dfitem = dfitems.get(str(armouryitem))
                
                # Replace item properties
                if dfitem and armouryitem:
                    pydwarf.log.debug('Replacing properties of item %s...' % armouryitem)
                    for removeitem in dfitem.alluntil(until_re_value='ITEM_.+'): removeitem.remove()
                    dfitem.add(tokens=raws.token.copy(armourytokens))
                    del dfitems[str(armouryitem)]
                    
                # Add new item
                elif armourytokens:
                    pydwarf.log.debug('Adding new item %s...' % armouryitem)
                    if filename not in dfraws.files: dfraws.addfile(filename)
                    armouryitem.prefix = '\n\n' # Makes outputted raws a bit neater
                    dfraws[filename].add(token=armouryitem)
                    dfraws[filename].add(tokens=raws.token.copy(armourytokens))
                    
                # This really shouldn't happen, but check for it anyway
                else:
                    pydwarf.log.error('Found no tokens belonging to armoury item %s.' % armouryitem)
                    
def additemstoents(dfraws, armouryraws, remove_entity_items):
    # Screw around with which items are allowed for which entities 
    for entityname, aentity in armoury_entities.iteritems():
        dfentity = dfraws.get(exact_value='ENTITY', exact_args=[entityname])
        entityitems = {}
        if dfentity:
            pydwarf.log.debug('Handling entity %s...' % dfentity)
            
            # Maintain this dict because it makes ammo easier to add
            weapons = {}
            
            # If we're removing items, just remove all the present ones in one go before adding things back
            if remove_entity_items:
                for itemtoken in dfentity.alluntil(value_in=armoury_entities, args_count=1, until_exact_value='ENTITY'): itemtoken.remove()
                
            # Time to add the items!
            for itemtype, items in aentity.iteritems():
                if itemtype != 'AMMO':
                    for itemname in items:
                        # Account for names that were changed from the normal DF raws
                        if itemname in weird_armoury_names: itemname = weird_armoury_names[itemname]
                        # Add the token if it isn't there already
                        dftoken = None if remove_entity_items else dfentity.getuntil(exact_value=itemtype, exact_args=[itemname], until_exact_value='ENTITY')
                        if remove_entity_items or not dftoken: dftoken = dfentity.add(raws.token(value=itemtype, args=[itemname]))
                        if itemtype == 'WEAPON': weapons[itemname] = dftoken
                        
            # Now add the ammunition
            if 'AMMO' in aentity:
                for weaponname, ammos in aentity['AMMO'].iteritems():
                    weapontoken = weapons.get(weaponname)
                    if not weapontoken: weapontoken = dfentity.get(exact_value='WEAPON', exact_args=[weaponname])
                    if weapontoken:
                        ammotokens = {token.args[0]: token for token in weapontoken.alluntil(exact_value='AMMO', args_count=1, until_except_value='AMMO')}
                        for addammo in ammos:
                            if addammo not in ammotokens: weapontoken.add(raws.token(value='AMMO', args=[addammo]))
                    else:
                        pydwarf.log.error('Failed to add ammo %s to weapon %s.' % ammos, weaponname)
                    
        else:
            pydwarf.log.error('Failed to find entity %s for editing.' % entityname)
            
def addreactions(dfraws, armouryraws):
    # Add raws file containing new reactions
    armouryreactions = armouryraws['reaction_armoury']
    if armouryreactions:
        if 'stal_reaction_armoury' not in dfraws.files:
            armouryreactions.header = 'stal_reaction_armoury'
            dfraws.files['stal_reaction_armoury'] = armouryreactions
        else:
            pydwarf.log.error('DF raws already contain stal_reaction_armory.')
    else:
        pydwarf.log.error('Couldn\'t load reaction_armoury raws file for reading.')
        
def removeattacks(dfraws, remove_attacks, remove_attacks_from):
    # Removes e.g. bite and scratch attacks from e.g. dwarves, humans, and elves
    if remove_attacks is not None and remove_attacks_from is not None:
        for species in remove_attacks_from:
            creaturetoken = dfraws.get(exact_value='CREATURE', exact_args=[species])
            if creaturetoken:
                for attacktype in remove_attacks:
                    attacktokens = creaturetoken.alluntil(exact_value='ATTACK', exact_arg=((0, attacktype),), until_exact_value='CREATURE')
                    for attacktoken in attacktokens:
                        subtokens = attacktoken.alluntil(until_re_value='(?!ATTACK_).+')
                        for subtoken in subtokens: subtoken.remove()
                        attacktoken.remove()
                    pydwarf.log.debug('Removed attack %s from creature %s.' % (attacktype, species))
            else:
                pydwarf.log.error('Couldn\'t find creature %s to remove bite and scratch attacks from.' % species)



@pydwarf.urist(
    name = 'stal.armoury',
    version = '1.0.0',
    author = ('Stalhansch', 'Sophie Kirschner'),
    description = 'Attempts to improve the balance and realism of combat.',
    arguments = {
        'remove_entity_items': '''Determines whether items that would be made unavailable to
            entities should be removed from those entities or not. If you're also using other
            mods that make changes to weapons and armour and such it may be desireable to set
            this flag to False. Otherwise, for best results, the flag should be set to True.
            Defaults to True''',
        'remove_attacks': '''Removes these attacks from species listed in remove_attacks_from.
            Defaults to scratch and bite.''',
        'remove_attacks_from': '''If set to True, specified remove_attacks are removed
            from the species in the list to improve combat balancing. If set to None those
            attacks will not be touched. Defaults to dwarves, humans, and elves.'''
    },
    compatibility = pydwarf.df_revision_range('0.40.14', '0.40.24')
)
def armourypack(dfraws, remove_entity_items=True, remove_attacks=('SCRATCH', 'BITE'), remove_attacks_from=('DWARF', 'HUMAN', 'ELF')):
    try:
        armouryraws = raws.dir(path=armourydir, log=pydwarf.log)
    except:
        return pydwarf.failure('Unable to load armoury raws.')
    
    additemstoraws(dfraws, armouryraws)
    additemstoents(dfraws, armouryraws, remove_entity_items)
    addreactions(dfraws, armouryraws)
    removeattacks(dfraws, remove_attacks, remove_attacks_from)
    
    return pydwarf.success()
