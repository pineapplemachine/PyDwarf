import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
import json
import importlib
from datetime import datetime
import pydwarf



# Used in some file paths and such
datetimeformat = '%Y.%m.%d.%H.%M.%S'
timestamp = datetime.now().strftime(datetimeformat)



class config:
    def __init__(self, version=None, input=None, output=None, backup=None, scripts=[], packages=[], verbose=False, log='logs/%s.txt' % timestamp):
        self.version = version      # Dwarf Fortress version, for handling script compatibility metadata
        self.input = input          # Raws are loaded from this input directory
        self.output = output        # Raws are written to this output directory
        self.backup = backup        # Raws are backed up to this directory before any changes are made
        self.scripts = scripts      # These scripts are run in the order that they appear
        self.packages = packages    # These packages are imported (probably because they contain PyDwarf scripts)
        self.verbose = verbose      # Log DEBUG messages to stdout if True, otherwise only INFO and above
        self.log = log              # Log file goes here
        
    def json(self, path, *args, **kwargs):
        with open(path, 'rb') as jsonfile: return self.apply(json.load(jsonfile), *args, **kwargs)
    
    def apply(self, data, applynone=False):
        if data:
            for key, value in data.iteritems(): 
                if applynone or value is not None: self.__dict__[key] = value
        return self
        
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return self.__str__()
        
    def setup(self):
        # Set up the pydwarf logger
        self.setuplogger()
        # Handle version == 'auto'
        self.setupversion()
        # Import packages
        self.setuppackages()
        
    def setuplogger(self):
        # Set up the logger (And you should do it first thing!)
        pydwarf.log.setLevel(logging.DEBUG)
        # Handler for console output
        stdouthandler = logging.StreamHandler(sys.stdout)
        stdouthandler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        stdouthandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datetimeformat))
        pydwarf.log.addHandler(stdouthandler)
        # Handler for log file output
        logfilehandler = logging.FileHandler(self.log)
        logfilehandler.setLevel(logging.DEBUG)
        logfilehandler.setFormatter(logging.Formatter('%(asctime)s: %(filename)s[%(lineno)s]: %(levelname)s: %(message)s', datetimeformat))
        pydwarf.log.addHandler(logfilehandler)
        
    def setuppackages(self):
        self.importedpackages = [importlib.import_module(package) for package in self.packages]
        
    def setupversion(self):
        # Handle automatic version detection
        if self.version == 'auto':
            pydwarf.log.info('Attempting to automatically detect Dwarf Fortress version.')
            self.version = pydwarf.detectversion(paths=(self.input, self.output), log=pydwarf.log)
            if self.version == None:
                pydwarf.log.info('Unable to detect Dwarf Fortress version.')
            else:
                pydwarf.log.info('Detected Dwarf Fortress version %s.' % self.version)
        elif conf.version is None:
            pydwarf.log.warning('No Dwarf Fortress version was specified. Scripts will be run regardless of their indicated compatibility.')
        else:
            pydwarf.log.info('Managing Dwarf Fortress version %s.' % self.version)
        pydwarf.urist.session.dfversion = self.version
