import os
import platform
    
if platform.system() == 'Windows':
    dfdir = 'E:/Sophie/Desktop/Files/Games/Dwarf Fortress/Dwarf Fortress/df_40_24_win'
    outdir = 'E:/Sophie/Desktop/pydwarf'
else:
    dfdir = '/Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23'
    outdir = '/Users/pineapple/Desktop/pydwarf'
    
export = {
    
    'input': dfdir,
    'output': os.path.join(outdir, 'output'),
    'backup': os.path.join(outdir, 'backup'),
    
    'paths': 'auto',
    
    'version': 'auto',
    'hackversion': 'auto',
    
    'packages': [
        'scripts'
    ],
    
    'scripts': [
        # Run a script by full name.
        'pineapple.noexotic',
        'putnam.materialsplus',
        'dragondeplatino.gemset.full',
        'smeeprocket.transgender',
        'witty.restrictednobles',
        # Run a script with arguments.
        {
            'name': 'pineapple.deerappear',
            'args': {'tile': "'d'", 'color': [6, 0, 1]}
        },
        # Run a script by partial name. (Automatically expands to pineapple.boneflux.)
        'boneflux',
        # Run all scripts under the umiman.smallthings namespace.
        'umiman.smallthings.*',
    ]
}
