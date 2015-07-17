#!/usr/bin/env python
# coding: utf-8

import os
import logging
import json
import yaml
import importlib
import imp
import traceback

from logger import log, stdouthandler, logfilehandler, timestamp
from version import detectversion
from helpers import findfile



auto_paths = [
    'gamelog.txt', 'errorlog.txt',
    'stderr.log', 'stdout.log',
    'raw/objects', 'raw/graphics',
    'data/art', 'data/init', 'data/speech',
    'dfhack.init', 'dfhack.init-example', 'dfhack.history',
    'raw/onLoad.init', 'raw/onWorldLoad.init',
    'hack/lua', 'hack/plugins', 'hack/raw', 'hack/ruby', 'hack/scripts',
    'stonesense',
]



class config:
    def __init__(
        self,
        version=None, paths=None, hackversion=None, input=None, output=None, backup=None,
        scripts=[], packages=[], verbose=False, log='logs/%s.txt' % timestamp,
    ):
        self.version = version          # Dwarf Fortress version, for handling script compatibility metadata
        self.hackversion = hackversion  # DFHack version
        self.input = input              # Raws are loaded from this input directory
        self.output = output            # Raws are written to this output directory
        self.backup = backup            # Raws are backed up to this directory before any changes are made
        self.paths = paths              # Files are only handled in these paths, relative to input
        self.scripts = scripts          # These scripts are run in the order that they appear
        self.packages = packages        # These packages are imported (probably because they contain PyDwarf scripts)
        self.verbose = verbose          # Log DEBUG messages to stdout if True, otherwise only INFO and above
        self.log = log                  # Log file goes here
        
    @staticmethod
    def load(root=None, json='config.json', yaml='config.yaml', override='config.py', args=None):
        conf = config()
        
        # Load default config files with the precedence: python override > json > yaml
        if yaml:
            if root: yaml = os.path.join(root, yaml)
            if os.path.isfile(yaml): conf.yaml(yaml)
        if json:
            if root: json = os.path.join(root, json)
            if os.path.isfile(json): conf.json(json)
        if override:
            if root and override.endswith('.py'): override = os.path.join(root, override)
            try:
                conf.override(override)
            except:
                log.debug('Tried and failed to apply default override from module %s. (But that\'s okay! It\'s just a default.)' % override)
                log.debug(traceback.format_exc())
        
        # Handle --config argument
        if args and args.get('config'):
            argsconf = args['config']
            if isinstance(argsconf, basestring): argsconf = (argsconf,)
            for applyconf in argsconf:
                try:
                    if applyconf.endswith('.json'):
                        conf.json(applyconf)
                    elif applyconf.endswith('.yaml'):
                        conf.yaml(applyconf)
                    else:
                        conf.override(applyconf)
                except:
                    log.exception('Failed to load configuration from %s.' % applyconf)
                
        # Apply other command line arguments
        if args: conf.apply(args)
        
        # Handle things like automatic version detection, package importing
        conf.setup()
        
        # All done!
        return conf
        
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
        log.debug('Applying json configuration from %s.' % path)
        try:
            with open(path, 'rb') as jsonfile:
                jsondata = json.load(jsonfile)
                return self.apply(jsondata, *args, **kwargs)
        except ValueError as error:
            strerror = str(error)
            if strerror.startswith('Invalid \\escape'):
                raise ValueError('Failed to load json from %s because of a misplaced backslash at %s. Perhaps you meant to use a forward slash instead?' % (path, strerror[17:]))
            else:
                raise error
                
    def yaml(self, path, *args, **kwargs):
        log.debug('Applying yaml configuration from %s.' % path)
        with open(path, 'rb') as yamlfile:
            yamldata = yaml.load(yamlfile)
            return self.apply(yamldata, *args, **kwargs)
            
    def override(self, module, *args, **kwargs):
        log.debug('Applying python configuration from %s.' % module)
        if module.endswith('.py'):
            modulename = os.path.splitext(os.path.basename(module))[0]
            with open(module, 'U') as modulefile:
                package = imp.load_module(modulename, modulefile, module, ('.py', 'U', imp.PY_SOURCE))
        else:
            package = importlib.import_module(module)
        try:
            export = package.export
        except:
            log.exception('Failed to load override module %s because it has no export attribute.' % module)
        self.apply(export)
    
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
        
    def setup(self, logger=True):
        # Set up the pydwarf logger
        if logger: self.setuplogger()
        # Handle paths == 'auto' or ['auto']
        self.setuppaths()
        # Handle version == 'auto'
        self.setupversion()
        # Handle hackversion == 'auto'
        self.setuphackversion()
        # Import packages
        self.setuppackages()
        
    def setuplogger(self):
        # Handler for console output
        stdouthandler.setLevel(logging.DEBUG if self.verbose else logging.INFO)
        # Handler for log file output
        if self.log:
            logdir = os.path.dirname(self.log)
            if not os.path.exists(logdir): os.makedirs(logdir)
            logfilehandler.__init__(self.log) # Call the constructor given a filepath, now that we actually have one to give
            log.addHandler(logfilehandler)
        
    def setuppackages(self):
        self.importedpackages = []
        if isinstance(self.packages, basestring): self.packages = (self.packages,)
        for package in self.packages:
            try:
                self.importedpackages.append(importlib.import_module(package))
            except:
                log.exception('Failed to import package %s.' % package)
        
    def setuppaths(self):
        if self.paths == 'auto' or self.paths == ['auto'] or self.paths == ('auto',):
            self.paths = auto_paths
        
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
        
    def setuphackversion(self):
        if self.hackversion == 'auto':
            log.debug('Attempting to automatically detect DFHack version.')
            
            dfhackdir = findfile(name='hack', paths=(self.input, self.output))
            if dfhackdir is None:
                log.error('Unable to detect DFHack directory.')
                return
            else:
                log.debug('Detected DFHack directory at %s.' % dfhackdir)
                
            newspath = os.path.join(dfhackdir, 'NEWS')
            if os.path.isfile(newspath):
                with open(newspath, 'rb') as news: self.hackversion = news.readline().strip()
                
            if self.hackversion is None:
                log.error('Unable to detect DFHack version.')
            else:
                log.debug('Detected DFHack version %s.' % self.hackversion)
                
        elif self.hackversion is None:
            log.warning('No DFHack version was specified.')
