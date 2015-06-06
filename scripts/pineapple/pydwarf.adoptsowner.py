import pydwarf

@pydwarf.urist(
    name = 'pineapple.adoptsowner',
    version = 'alpha',
    author = 'Sophie Kirschner',
    description = '''todo''',
    arguments = {
        'add_to': '''If set to None, no ADOPTS_OWNER tokens are added. If set
            to '*', tokens are added to all creatures. If set to an iterable
            containing IDs of creatures, ADOPTS_OWNER will be added to each
            of those creatures. Defaults to None.''',
        'remove_from': '''If set to None, no ADOPTS_OWNER tokens are removed.
            If set to '*', all ADOPTS_OWNER tokens are removed. If set to an
            iterable containing IDs of creatures, ADOPTS_OWNER will be
            removed from each of those creatures. Defaults to '*'.'''
    },
    compatibility = (pydwarf.df_0_2x, pydwarf.df_0_3x, pydwarf.df_0_40)
)
def adoptsowner(df, add_to=None, remove_from='*'):
    return pydwarf.urist.getfn('pineapple.utils.objecttokens')(
        df,
        object_type = 'CREATURE',
        token = 'ADOPTS_OWNER',
        add_to = add_to,
        remove_from = remove_from
    )
