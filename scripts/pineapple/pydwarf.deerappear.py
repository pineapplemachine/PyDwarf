import pydwarf

@pydwarf.urist(
    name = 'pineapple.deerappear',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Changes the appearance of each deer from a brown D to yellow d.',
    arguments = {
        'creature': 'Change the creature whose appearance will be modified. (Heresy!)',
        'tile': 'Set the tile that the deer\'s appeance will be set to.',
        'color': 'Set the arguments that the deer\'s color token will be given.'
    },
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x, pydwarf.df_0_2x)
)
def deerappear(raws, creature='DEER', tile="'d'", color=['6','0','1']):
    # Find the first token that looks like [CREATURE:DEER]
    deertoken = raws.getobj('CREATURE', creature)
    if deertoken:
        # Find the first token, following [CREATURE:DEER], that looks like [CREATURE_TILE:'D']
        deertile = deertoken.getuntil(exact_value='CREATURE_TILE', args_count=1, until_exact_value='CREATURE')
        # Find the first token, following [CREATURE:DEER], that looks like [COLOR:6:0:0]
        deercolor = deertoken.getuntil(exact_value='COLOR', args_count=3, until_exact_value='CREATURE')
        if deertile and deercolor:
            # Change the token to look like [CREATURE_TILE:'d']
            deertile.args[0] = tile
            # Change the token to look like [COLOR:6:0:1]
            deercolor.args = color
            return pydwarf.success()
        else:
            return pydwarf.failure('Didn\'t find CREATURE_TILE and COLOR tokens as expected.')
    else:
        return pydwarf.failure('I couldn\'t find the deer token.')
