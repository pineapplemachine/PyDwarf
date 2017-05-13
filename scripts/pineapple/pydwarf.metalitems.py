import pydwarf
import raws



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
    title = 'Forge More Metal Items',
    version = '1.0.2',
    author = 'Sophie Kirschner',
    description = 'Allows the forging of every type of metal item from the specified metals.',
    arguments = {
        'metals': 'These metals will be made to allow forging of each item specified.',
        'items': 'These are the items that the listed metals will always be allowed for.'
    },
    compatibility = (pydwarf.df_0_3x, pydwarf.df_0_40)
)
def metalitems(df, metals=default_metals, items=default_item_tokens):
    # Turn the item names into a list of tokens
    itemtokens = [raws.token(value=item) for item in items]
    
    # Apply to each metal
    affected = df.allobj(type='INORGANIC', id_in=metals).each(
        lambda token: (
            # Remove existing tokens first to prevent duplicates when adding
            token.removeallprop(value_in=items),
            # And now add the specified tokens
            token.addprop(raws.helpers.copytokens(itemtokens))
        )
    )
    
    # All done!
    if affected:
        return pydwarf.success('Affected %d metals.' % len(affected))
    else:
        return pydwarf.failure('Affected no metals.')
