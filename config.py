import os
import sys
import platform
import logging
from datetime import datetime
import pydwarf

class config:
    def __init__(self):
        self.log = logging.getLogger()
        self.dfversion = None
        self.rawsdir = None
        self.outputdir = None
        self.backupdir = None
        self.backup = True
        self.runscripts = []

def export():

    conf = config()

    # Will be used for assignment of some file paths
    datetimeformat = '%Y.%m.%d.%H.%M.%S'
    timestamp = datetime.now().strftime(datetimeformat)

    # To what file should logs be outputted?
    logfile = 'logs/%s.txt' % timestamp

    # Set up the logger (And do it first thing!)
    pydwarf.log.setLevel(logging.DEBUG)
    # Handler for console output
    stdouthandler = logging.StreamHandler(sys.stdout)
    stdouthandler.setLevel(logging.INFO)
    stdouthandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datetimeformat))
    pydwarf.log.addHandler(stdouthandler)
    # Handler for log file output
    logfilehandler = logging.FileHandler(logfile)
    logfilehandler.setLevel(logging.DEBUG)
    logfilehandler.setFormatter(logging.Formatter('%(asctime)s: %(filename)s[%(lineno)s]: %(levelname)s: %(message)s', datetimeformat))
    pydwarf.log.addHandler(logfilehandler)
    
    # Informs settings of where your Dwarf Fortress directory can be found.
    # This is an example! You will want to change this before using PyDwarf.
    if platform.system() == 'Windows':
        dfdir = 'E:/Sophie/Desktop/Files/Games/Dwarf Fortress/Dwarf Fortress/df_40_24_win'
    else:
        dfdir = '/Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23'
        
    # Detect Dwarf Fortress version
    conf.dfversion = getdfversion(dfdir)

    # Read raws from this directory.
    conf.rawsdir = os.path.join(dfdir, 'raw/objects')

    # Optionally specify an output directory which differs from the raws input directory.
    # Set to None to output to the raws directory itself.
    conf.outputdir = 'output/'

    # Backup raws to this directory before modifying.
    conf.backupdir = os.path.join(dfdir, 'bak', timestamp)

    # Set to False to make no backup. (Not recommended.)
    conf.backup = True

    # Runs each of the scripts in scripts/ in sequential order.
    # To run a script without arguments, simply put a string in the list.
    # To run a script with arguments, put a tuple in the list like: ('script_name', {'arg0': 1, 'arg1': 2})
    # A function can optionally be specified in place of a string, and that function will be run instead.
    import scripts
    conf.runscripts = [
        #{'name': 'pineapple.diff', 'args': {'paths': ['diff/Underhaul', 'diff/Oricalicum/objects/plant_standard.txt', 'diff/plant_standard.txt']}}
        # 'materialsplus',
        # 'microreduce',
        'transgender',
        'flybears',
        # 'stal.armoury',
        'restrictednobles',
        # 'pineapple.noexotic',
        # 'pineapple.nograzers',
        'pineapple.deerappear',
        'pineapple.flybears'
        
        # 'pineapple.noexotic',
        # {'name': 'stoneclarity', 'args': {'fuels': scripts.stoneclarity.vanilla_fuels}}
    ]

    # Return the settings namespace that the manager needs to know about. (The rest is just noise.)
    return conf
    
# Attempt to automatically determine Dwarf Fortress version
def getdfversion(dfdir):
    releasenotespath = os.path.join(dfdir, 'release notes.txt')
    with open(releasenotespath, 'rb') as releasenotes:
        for line in releasenotes.readlines():
            if line.startswith('Release notes for'):
                version = line.split()[3]
                pydwarf.log.debug('Detected Dwarf Fortress version: %s.' % version)
                return version
    pydwarf.log.warning('Failed to detect Dwarf Fortress version.')
    return None
