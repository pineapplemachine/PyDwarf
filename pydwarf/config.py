import sys
import os
import logging
import json
import importlib
from datetime import datetime

from log import log
from version import detectversion
from urist import urist, session
from helpers import findfile



# Used in some file paths and such
datetimeformat = '%Y.%m.%d.%H.%M.%S'
timestamp = datetime.now().strftime(datetimeformat)



class config:
    def __init__(self, version=None, paths=None, dfhackver=None, input=None, output=None, backup=None, scripts=[], packages=[], verbose=False, log='logs/%s.txt' % timestamp):
        self.version = version          # Dwarf Fortress version, for handling script compatibility metadata
        self.dfhackver = dfhackver      # DFHack version
        self.input = input              # Raws are loaded from this input directory
        self.output = output            # Raws are written to this output directory
        self.backup = backup            # Raws are backed up to this directory before any changes are made
        self.paths = paths  # Files are only handled in these paths, relative to input
        self.scripts = scripts          # These scripts are run in the order that they appear
        self.packages = packages        # These packages are imported (probably because they contain PyDwarf scripts)
        self.verbose = verbose          # Log DEBUG messages to stdout if True, otherwise only INFO and above
        self.log = log                  # Log file goes here
        
    def __str__(self):
        return str(self.__dict__)
    def __repr__(self):
        return self.__str__()
        
    def __getitem__(self, attr):
        return self.__dict__[attr]
    def __setitem__(self, attr, value):
        self.__dict__[attr] = value
        
    def __iter__(self):
        return iter(self.__dict__)
    def iteritems(self):
        return self.__dict__.iteritems()
        
    def __add__(self, other):
        return config.concat(self, other)
    def __radd__(self, other):
        return config.concat(other, self)
    def __iadd__(self, item):
        self.apply(item)
        return self
    
    def __and__(self, other):
        return config.intersect(self, other)
        
    def json(self, path, *args, **kwargs):
        with open(path, 'rb') as jsonfile: return self.apply(json.load(jsonfile), *args, **kwargs)
    
    def apply(self, data, applynone=False):
        if data:
            for key, value in data.iteritems(): 
                if applynone or value is not None: self.__dict__[key] = value
        return self
        
    def copy(self):
        copy = config()
        for key, value in self: copy[key] = value
        return copy
        
    @staticmethod
    def concat(*configs):
        result = config()
        for conf in configs: result.apply(conf)
        return result
        
    @staticmethod
    def intersect(*configs):
        result = config()
        first = configs[0]
        for attr, value in first.iteritems():
            for conf in configs:
                if (conf is not first) and (attr not in conf or conf[attr] != value): break
            else:
                result[attr] = value
        return result
        
    def setup(self, logger=False):
        # Set up the pydwarf logger
        if logger: self.setuplogger()
        # Handle paths == 'auto' or ['auto']
        self.setuppaths()
        # Handle version == 'auto'
        self.setupversion()
        # Handle dfhackver == 'auto'
        self.setupdfhackver()
        # Import packages
        self.setuppackages()
        
    def setuplogger(self):
        # Set up the logger (And it should be done first thing!)
        log.setLevel(logging.DEBUG)
        # Handler for console output
        stdouthandler = logging.StreamHandler(sys.stdout)
        stdouthandler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        stdouthandler.setFormatter(logging.Formatter('%(asctime)s: %(levelname)s: %(message)s', datetimeformat))
        log.addHandler(stdouthandler)
        # Handler for log file output
        if self.log:
            logdir = os.path.dirname(self.log)
            if not os.path.exists(logdir): os.makedirs(logdir)
            logfilehandler = logging.FileHandler(self.log)
            logfilehandler.setLevel(logging.DEBUG)
            logfilehandler.setFormatter(logging.Formatter('%(asctime)s: %(filename)s[%(lineno)s]: %(levelname)s: %(message)s', datetimeformat))
            log.addHandler(logfilehandler)
        
    def setuppackages(self):
        self.importedpackages = [importlib.import_module(package) for package in self.packages]
        
    def setuppaths(self):
        if self.paths == 'auto' or self.paths == ['auto'] or self.paths == ('auto',):
            self.paths = [
                'gamelog.txt', 'errorlog.txt',
                'stderr.log', 'stdout.log',
                'raw/objects', 'raw/graphics',
                'data/init',
                'dfhack.init', 'dfhack.init-example', 'dfhack.history',
                'hack/lua', 'hack/plugins', 'hack/raw', 'hack/ruby', 'hack/scripts',
            ]
        
    def setupversion(self):
        # Handle automatic version detection
        if self.version == 'auto':
            log.debug('Attempting to automatically detect Dwarf Fortress version.')
            self.version = detectversion(paths=(self.input, self.output))
            if self.version is None:
                log.error('Unable to detect Dwarf Fortress version.')
            else:
                log.debug('Detected Dwarf Fortress version %s.' % self.version)
        elif self.version is None:
            log.warning('No Dwarf Fortress version was specified. Scripts will be run regardless of their indicated compatibility.')
        else:
            log.info('Managing Dwarf Fortress version %s.' % self.version)
        
    def setupdfhackver(self):
        if self.dfhackver == 'auto':
            log.debug('Attempting to automatically detect DFHack version.')
            
            dfhackdir = findfile(name='hack', paths=(self.input, self.output))
            if dfhackdir is None:
                log.error('Unable to detect DFHack directory.')
                return
            else:
                log.debug('Detected DFHack directory at %s.' % dfhackdir)
                
            newspath = os.path.join(dfhackdir, 'NEWS')
            if os.path.isfile(newspath):
                with open(newspath, 'rb') as news: self.dfhackver = news.readline().strip()
                
            if self.dfhackver is None:
                log.error('Unable to detect DFHack version.')
            else:
                log.debug('Detected DFHack version %s.' % self.dfhackver)
                
        elif self.dfhackver is None:
            log.warning('No DFHack version was specified.')
