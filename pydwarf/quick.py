def quick(raws, root=None, **kwargs):
    se = session.session()
    if root is not None: kwargs['root'] = root
    args = {
        'input': 'df',
        'paths': 'auto',
        'version': 'auto',
        'hackversion': 'auto',
        'output': 'output/',
        'backup': None,
        'packages': 'scripts',
        'verbose': True,
        'log': '',
    }
    args.update(kwargs)
    se.load(raws, args=args)
    return se

def df(*args, **kwargs):
    se = quick(*args, **kwargs)
    return se.df



import session
