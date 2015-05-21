import pydwarf

@pydwarf.urist(
    name = 'pineapple.deerappear',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Changes the appearance of each deer from a brown D to yellow d.',
    compatibility = (pydwarf.df_0_40, pydwarf.df_0_3x, pydwarf.df_0_2x)
)
def deerappear(raws):
    # Find the first token that looks like [CREATURE:DEER]
    deertoken = raws.get('CREATURE:DEER')
    if deertoken:
        # Find the first token, following [CREATURE:DEER], that looks like [CREATURE_TILE:'D']
        deertile = deertoken.getuntil(exact_value='CREATURE_TILE', until_exact_value='CREATURE')
        # Find the first token, following [CREATURE:DEER], that looks like [COLOR:6:0:0]
        deercolor = deertoken.getuntil(exact_value='COLOR', until_exact_value='CREATURE')
        if deertile and deercolor and deertile.nargs == 1 and deercolor.nargs == 3:
            # Change the token to look like [CREATURE_TILE:'d']
            deertile.args[0] = "'d'"
            # Change the token to look like [COLOR:6:0:1]
            deercolor.args[2] = '1'
            return pydwarf.success()
        else:
            return pydwarf.failure('Didn\'t find CREATURE_TILE and COLOR tokens as expected.')
    else:
        return pydwarf.failure('I couldn\'t find the deer token.')
