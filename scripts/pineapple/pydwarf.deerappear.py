import pydwarf

@pydwarf.urist(
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = 'Changes the appearance of each deer from a brown D to yellow d.'
)
def deerappear(raws):
    # Find the first token that looks like [CREATURE:DEER]
    deertoken = raws.get('CREATURE:DEER')
    if deertoken:
        # Find the first token, following [CREATURE:DEER], that looks like [CREATURE_TILE:'D']
        deertile = deertoken.get("CREATURE_TILE:'D'")
        # Find the first token, following [CREATURE:DEER], that looks like [COLOR:6:0:0]
        deercolor = deertoken.get('COLOR:6:0:0')
        if deertile and deercolor and deertile.nargs == 1 and deercolor.nargs == 3:
            # Change the token to look like [CREATURE_TILE:'d']
            deertile.args[0] = "'d'"
            # Change the token to look like [COLOR:6:0:1]
            deercolor.args[2] = '1'
            return pydwarf.success()
        else:
            return pydwarf.failure('Appearance of deer token was not what I expected.')
    else:
        return pydwarf.failure('I couldn\'t find the deer token.')
