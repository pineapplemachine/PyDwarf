import os
import sys
import platform
import logging
from datetime import datetime
import pydwarf

def getsettings():

    # Will be used for assignment of some file paths
    datetimeformat = '%Y.%m.%d.%H.%M.%S'
    timestamp = datetime.now().strftime(datetimeformat)

    # To what file should logs be outputted?
    logfile = 'logs/%s.txt' % timestamp

    # Set up the logger (And do it first thing!)
    log = logging.getLogger()
    log.setLevel(logging.DEBUG)
    pydwarf.log = log
    # Handler for console output
    stdouthandler = logging.StreamHandler(sys.stdout)
    stdouthandler.setLevel(logging.INFO)
    stdouthandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datetimeformat))
    log.addHandler(stdouthandler)
    # Handler for log file output
    logfilehandler = logging.FileHandler(logfile)
    logfilehandler.setLevel(logging.DEBUG)
    logfilehandler.setFormatter(logging.Formatter('%(asctime)s: %(filename)s[%(lineno)s]: %(levelname)s: %(message)s', datetimeformat))
    log.addHandler(logfilehandler)

    def managersettings(): pass # Create a dummy function to be used as a namespace for PyDwarf manager settings

    # Informs settings of where your Dwarf Fortress directory can be found.
    # This is an example! You will want to change this before using PyDwarf.
    if platform.system() == 'Windows':
        dfdir = 'E:/Sophie/Desktop/Files/Games/Dwarf Fortress/Dwarf Fortress/df_40_24_win'
    else:
        dfdir = '/Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23'
        
    # Detect Dwarf Fortress version
    managersettings.dfversion = getdfversion(dfdir)

    # Read raws from this directory.
    managersettings.rawsdir = os.path.join(dfdir, 'raw/objects')

    # Optionally specify an output directory which differs from the raws input directory.
    # Set to None to output to the raws directory itself.
    managersettings.outputdir = 'output/'

    # Backup raws to this directory before modifying.
    managersettings.backupdir = os.path.join(dfdir, 'bak', timestamp)

    # Set to False to make no backup. (Not recommended.)
    managersettings.backup = True

    # Runs each of the scripts in scripts/ in sequential order.
    # To run a script without arguments, simply put a string in the list.
    # To run a script with arguments, put a tuple in the list like: ('script_name', {'arg0': 1, 'arg1': 2})
    # A function can optionally be specified in place of a string, and that function will be run instead.
    import scripts
    managersettings.runscripts = [
        'deerappear',
        'noexotic',
        {'name': 'stoneclarity', 'args': {'fuels': scripts.stoneclarity.vanilla_fuels}}
    ]

    # Return the settings namespace that the manager needs to know about. (The rest is just noise.)
    return managersettings
    
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
    
exportsettings = getsettings()
