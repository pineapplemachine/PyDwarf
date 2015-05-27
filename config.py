import os
import sys
import platform
import logging
import json
from datetime import datetime
import pydwarf



# Used in some file paths and such
datetimeformat = '%Y.%m.%d.%H.%M.%S'
timestamp = datetime.now().strftime(datetimeformat)



def __main__():
    
    # Set to True to load configuration from config.py
    use_json_config = True
    json_config_path = 'config.json'

    # Otherwise, this function is called for retrieving configuration
    # An example exportcustom function is provided but it shouldn't be used out-of-the-box
    custom_config_function = exportcustom
    
    # Return a configuration object that the manager needs to know about
    return getexportconfig(use_json_config, json_config_path, custom_config_function)
        


def getexportconfig(use_json_config, json_config_path, custom_config_function):
    # Initialize logs
    loggerconfig('logs/%s.txt' % timestamp)
    
    # Load pydwarf scripts
    import scripts
    
    # Load config from json file
    if use_json_config: return exportjson(json_config_path)    
    
    # Config from function
    elif custom_config_function: return custom_config_function()
    
    # No config specified
    else: raise ValueError
    
    

class config:
    def __init__(self):
        self.log = logging.getLogger()
        self.version = None # Dwarf Fortress version, for handling script compatibility metadata
        self.input = None   # Raws are loaded from this input directory
        self.output = None  # Raws are written to this output directory
        self.backup = None  # Raws are backed up to this directory before any changes are made
        self.scripts = []   # These scripts are run in the order that they appear



def exportjson(path):
    conf = config()
    
    # Load json configuration file
    with open(path, 'rb') as jsonfile:
        jsonconf = json.load(jsonfile)
        
    # Copy attributes to a config object (because why not)
    for key, value in jsonconf.iteritems():
        conf.__dict__[key] = value
        print '%s: %s %s' % (key, type(value), value)
        
    # All done!
    return conf



def exportcustom():
    conf = config()
    
    # Informs settings of where your Dwarf Fortress directory can be found.
    # This is an example! You will want to change this before using PyDwarf.
    if platform.system() == 'Windows':
        dfdir = 'E:/Sophie/Desktop/Files/Games/Dwarf Fortress/Dwarf Fortress/df_40_24_win'
    else:
        dfdir = '/Users/pineapple/Desktop/stuff/dwarfort/df_osx_40_23'
        
    # Detect Dwarf Fortress version
    conf.dfversion = getdfversion(dfdir)

    # Read raws from this directory.
    conf.input = os.path.join(dfdir, 'raw/objects')

    # Optionally specify an output directory which differs from the raws input directory.
    # Set to None to output to the same directory as specified by input.
    conf.output = 'output/'

    # Backup raws to this directory before modifying. Set to None to make no backups. (Not recommended.)
    conf.backup = os.path.join(dfdir, 'bak', timestamp)

    # Runs each of the scripts in scripts/ in sequential order.
    # To run a script without arguments, simply put a string in the list.
    # To run a script with arguments, put a tuple in the list like: ('script_name', {'arg0': 1, 'arg1': 2})
    # A function can optionally be specified in place of a string, and that function will be run instead.
    conf.scripts = [
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
    ]

    # Return the settings namespace that the manager needs to know about. (The rest is just noise.)
    return conf
    
    

def loggerconfig(path='logs/log.txt'):
    # Set up the logger (And you should do it first thing!)
    pydwarf.log.setLevel(logging.DEBUG)
    # Handler for console output
    stdouthandler = logging.StreamHandler(sys.stdout)
    stdouthandler.setLevel(logging.INFO)
    stdouthandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datetimeformat))
    pydwarf.log.addHandler(stdouthandler)
    # Handler for log file output
    logfilehandler = logging.FileHandler(path)
    logfilehandler.setLevel(logging.DEBUG)
    logfilehandler.setFormatter(logging.Formatter('%(asctime)s: %(filename)s[%(lineno)s]: %(levelname)s: %(message)s', datetimeformat))
    pydwarf.log.addHandler(logfilehandler)
    
    
    
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



export = __main__()
