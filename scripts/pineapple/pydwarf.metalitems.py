import pydwarf



default_metals = [
    'IRON', 'GOLD', 'SILVER', 'COPPER', 'NICKEL', 'BRONZE', 'STEEL',
    'PLATINUM', 'ELECTRUM', 'TIN', 'ALUMINUM', 'NICKEL_SILVER',
    'STERLING_SILVER', 'BLACK_BRONZE', 'ROSE_GOLD', 'BISMUTH_BRONZE',
    'ADAMANTINE'
]

default_item_tokens = [
    'ITEMS_WEAPON', 'ITEMS_WEAPON_RANGED', 'ITEMS_ANVIL', 'ITEMS_AMMO',
    'ITEMS_DIGGER', 'ITEMS_ARMOR', 'ITEMS_DELICATE', 'ITEMS_SIEGE_ENGINE', 'ITEMS_QUERN'
]

item_tokens_no_anvil = list(default_item_tokens)
item_tokens_no_anvil.remove('ITEMS_ANVIL')



@pydwarf.urist(
    name = 'pineapple.metalitems',
    version = '1.0.0',
    author = 'Sophie Kirschner',
    description = 'Allows the forging of every type of metal item from the specified metals.',
    arguments = {
        'metals': 'These metals will be made to allow forging of each item specified.',
        'items': 'These are the items that the listed metals will always be allowed for.'
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def metalitems(df, metals=default_metals, items=default_item_tokens):
    # Handle each metal
    modified = 0
    for inorganictoken in df.allobj('INORGANIC'):
        if inorganictoken.args[0] in metals:
            metal = inorganictoken.args[0]
            pydwarf.log.debug('Handling metal %s...' % metal)
            itemtokens = inorganictoken.allprop(value_in=items)
            if len(itemtokens) < len(items):
                pydwarf.log.debug('Adding tokens to metal %s...' % metal)
                # Remove existing item tokens from the list (To avoid making duplicates)
                for itemtoken in itemtokens:
                    itemtoken.remove()
                # Add new ones
                templatetoken = inorganictoken.getlastprop('USE_MATERIAL_TEMPLATE')
                addaftertoken = templatetoken if templatetoken else inorganictoken
                for item in items:
                    addaftertoken.add(item)
                modified += 1
            else:
                pydwarf.log.debug('Metal %s already allows all the item types specified, skipping.' % metal)
            
    # All done
    if modified > 0:
        return pydwarf.success('Added tokens to %d metals.' % modified)
    else:
        return pydwarf.failure('No tokens were added to any metals.')
