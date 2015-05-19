import os
import platform
from datetime import datetime

# This is an example! You will want to change this before using PyDwarf.
if platform.system() == 'Windows':
    dfdir = 'E:/Sophie/Desktop/Files/Games/Dwarf Fortress/Dwarf Fortress/df_40_24_win'
else:
    dfdir = '/Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23'

# Backup raws to this directory before modifying.
timestamp = datetime.now().strftime('%Y.%m.%d.%H.%M.%S')
backupdir = os.path.join(dfdir, 'bak', timestamp)

# Set to False to make no backup. (Not recommended.)
backup = True

# Read raws from this directory.
rawsdir = os.path.join(dfdir, 'raw/objects')

# Optionally specify an output directory which differs from the raws input directory.
# Set to None to output to the raws directory itself.
outputdir = 'output/'

# Runs each of the scripts in scripts/ in sequential order.
# To run a script without arguments, simply put a string in the list.
# To run a script with arguments, put a tuple in the list like: ('script_name', {'arg0': 1, 'arg1': 2})
# A function can optionally be specified in place of a string, and that function will be run instead.
import scripts
runscripts = [
    'deerappear',
    'noexotic'
]
