import os
import platform

if False:
    # This is an example! These settings will not actually be applied while the above line reads 'if False:'.
    
    if platform.system() == 'Windows':
        dfdir = 'E:/Sophie/Desktop/Files/Games/Dwarf Fortress/Dwarf Fortress/df_40_24_win'
    else:
        dfdir = '/Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23'
        
    export = {
        'input': os.path.join(dfdir, 'vanillaraw/objects'),
        'output': 'output',
        'backup': 'backup',
        'paths': 'auto',
        'version': 'auto',
        'hackversion': 'auto',
        'scripts': [
            {
                'name': 'pineapple.deerappear',
                'args': {'tile': "'d'", 'color': [6, 0, 1]}
            },
            {
                'name': 'pineapple.noexotic',
                'match': {'version': 'alpha'}
            },
            'pineapple.nograzers',
            'putnam.materialsplus',
            'smeeprocket.transgender',
            'witty.restrictednobles'
        ],
        'packages': [
            'scripts'
        ]
    }

else:
    
    export = {}

